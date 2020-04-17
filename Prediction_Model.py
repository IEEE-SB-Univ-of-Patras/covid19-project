import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
import worldometer_scrapping
from sklearn.utils import shuffle
import math
import sklearn.metrics as met
from joblib import dump,load




######################################
import warnings
warnings.filterwarnings("ignore")
######################################


############Settings########
polynomial_features_check=1
print_data_check = 0
regularization_check = 1
scaling_check = 1
shuffle_check = 1
polynomial_order = 25
print_scores = 0




number_of_elements=2

R0 = 2.45  
days_of_infectivity = 10
recovery_rate = 1 / days_of_infectivity
transmission_rate = R0 * recovery_rate  
indx=0
a=1
thresh=0



#Settings using global variables that are used in the rest of the functions
def settings():
    global polynomial_features_check
    global print_data_check
    global regularization_check
    global scaling_check
    global shuffle_check
    global print_scores
    global polynomial_order 


    
    print("Current settings:\nPolynomial Features ",polynomial_features_check,
          " Regularization ",regularization_check," Scaling the data",scaling_check,
          " Shuffiling the data ",shuffle_check," Printing the data ", print_data_check)
    print("Do you want to change the current settings?(Y/n)")
    settings_change = input()

    if settings_change=='Y':
        print("Polynomial Features(0 No polynomial features are added/1 polynomial features",
              "up to the most efficient order are added)")
        polynomial_features_check = int(input())

        if polynomial_features_check==1:
            print("Do you want to print the scores of each case?(Yes=1/No=0)")
            print_scores = int(input())

            print("Up to what order polynomials would you like to get?(integer, default is 25)")
            polynomial_order = int(input())
        
        print("Regularization(0 No regularization checking is done and alpha takes the value of 1",
              "/1 The best value for alpha is calculated and used")
        regularization_check = int(input())

        print("Scaling the data(0 no scaling is done/1 data are scaled from 0 to 1)")
        scaling_check = int(input())

        print("Shuffling the data(0 no shuffling is done/1 the data are shuffled)")
        shuffling_check = int(input())

        print("Print the data(0 no printig is done/1 prints the data)")
        print_data_check = int(input())

    return 0

#Prints data
def print_data(data,results):
    for i in range(len(data)):
        print(data[i],results[i])

    return 0


#Shuffles, Scales and divides data
def data_manipulation(X,Y):

    global thresh
    global scaling_check
    global shuffle_check
    
    if shuffle_check==1:
        X,Y =shuffle(X,Y)

    if scaling_check==1:
        min_max_scaler = MinMaxScaler()
        min_max_scaler.fit(X)

        
        X_temp = min_max_scaler.transform(X)
        dump(min_max_scaler,'scaler.joblib')
    else:
        X_temp=X
        
    X_train=X_temp[:-2*thresh]
    Y_train=Y[:-2*thresh]

    X_CV=X_temp[-2*thresh:-thresh]
    Y_CV=Y[-2*thresh:-thresh]

    X_test=X_temp[-thresh:]
    Y_test=Y[-thresh:]



    return X_train,X_CV,X_test,Y_train,Y_CV,Y_test



#Finds the best order polynomial to make extra features with
def polynomial_checking(X,Y,order_limit=25,print_scores=0):


    global indx
    indx=1
    global thresh
    
    
    
    max_score=-math.inf
    power=1

    
    
    for i in range(1,order_limit):
        X_temp=X
        
        poly = PolynomialFeatures(i)
        X_temp = poly.fit_transform(X)
        

        X_train=X_temp[:-2*thresh]
        Y_train=Y[:-2*thresh]

        X_CV=X_temp[-2*thresh:-thresh]
        Y_CV=Y[-2*thresh:-thresh]

        X_test=X_temp[-thresh:]
        Y_test=Y[-thresh:]

        

        
        
        reg = Ridge()  
        reg.fit(X_train,Y_train)
        Y_pred=reg.predict(X_CV)

        
        score = met.r2_score(Y_CV,Y_pred)

        if print_scores==1:
            print(i,score)
        if score>max_score+0.0001:
            power = i
            max_score = score
    print("\nChosen polynomial order is:",power)
    poly = PolynomialFeatures(power)
    poly.fit(X)
    X_scaled= poly.transform(X)
    dump(poly,'poly.joblib')            
    return X_scaled


#Finds the best regularization parameter
def regularization_parameter(X,Y):



    reg = RidgeCV(alphas = list(np.arange(0.02,1,0.02)))
    model = reg.fit(X,Y)

    print("Best regularization parameter:",model.alpha_)
    return model.alpha_


#Trains the model
def model():

    global thresh

    data = worldometer_scrapping.mine_data(scope = 'Greece')

    n = data["demographics"]["population"]

    total_list = data["cases"]  
    deaths_list = data["deaths"]  
    R_list = data["recovered"] 
    I_list = data["active"]  
    S_list = []  
    for i, val in enumerate(total_list):
        S_list.append(n - val)  



    X=np.array([0]*number_of_elements)
    Y=np.array(0)
    

    
    for i in range(len(S_list)):

        if I_list[i]==0:
            continue

        else:
            
            X=np.vstack([X,[I_list[i],R_list[i]]])
                
            
                
            if I_list[i-1]==0:
                b=transmission_rate
            else:
                b=(S_list[i-1]-S_list[i])*n/(S_list[i-1]*I_list[i-1]+1)
                if b>=0.245:
                    b=0.245
            Y=np.vstack([Y,[b]])

    

    print(X)
    m=len(Y)
    thresh=int(0.15*m)




#Polynomial checking    
    if polynomial_features_check == 1:
        X= polynomial_checking(X,Y,polynomial_order,print_scores)



#Scaling, shuffling and division of data    
    X_train,X_CV,X_test,Y_train,Y_CV,Y_test= data_manipulation(X,Y)

    



#Printing the data
    if print_data_check==1:
        print("Whole Data\n")
        print_data(X,Y)
        print("\nTraining Data\n")
        print_data(X_train,Y_train)
        print("\nCV Data\n")
        print_data(X_CV,Y_CV)
        print("\nTesting Data\n")
        print_data(X_test,Y_test)



#Regularization parameter checking
    if regularization_check==1:
        a = regularization_parameter(X_CV,Y_CV)   
    else: a=0
    





#Model training and predictions    
    reg = Ridge(alpha=a)
    reg.fit(X_train,Y_train)

    Y_test_pred = reg.predict(X_test)
    Y_CV_pred = reg.predict(X_CV)
    Y_train_pred=reg.predict(X_train)
    
    dump(reg,'R_model.joblib')
    
    print("\nTraining set fitting score:",met.r2_score(Y_train,Y_train_pred),"\nCV set fitting score",
          met.r2_score(Y_CV,Y_CV_pred),"\nTest set fitting score", met.r2_score(Y_test,Y_test_pred))


    

    S  = plt.scatter(X_train[:,indx],Y_train,color='red', s=1,marker = 'x',linewidths=None)
    plt.scatter(X_test[:,indx],Y_test_pred,color = 'black', s=1)
    plt.scatter(X_test[:,indx],Y_test,color = 'teal', s=1)




    plt.show()



    return 0



#Function that predicts beta given new data X
def predict(X):
    X=X.reshape(1,-1)
    
    reg = load('R_model.joblib')
    min_max_scaler = load('scaler.joblib')
    poly = load('poly.joblib')

    
    if polynomial_features_check == 1:
        
        X = poly.transform(X)

    if scaling_check==1:
        
        X =min_max_scaler.transform(X)


    new_beta = reg.predict(X)

    
    return new_beta




settings()
model()
num=np.array([2192,359])
prediction= predict(num)
print(prediction)
