import datetime
import matplotlib.pyplot as plt
import numpy as np
import worldometer_scrapping
import math
import pandas as pd
import time

from Data_organization import deliver_data
from Data_organization import get_static
from Data_organization import get_data_dicts
from model_tools import calculate_beta
from plot_learning_curve import plot_learning_curve




from joblib import dump,load
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.utils import shuffle
from sklearn.model_selection import learning_curve
import sklearn.metrics as met
from sklearn.model_selection import ShuffleSplit





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
polynomial_order = 5
print_scores = 0
download_option=0



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
        
        poly = PolynomialFeatures(i,interaction_only=True)
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



def data_fetch():

    dictionary=deliver_data()
    firsttime=1
    for i in dictionary:
        
        if firsttime==1:
            X=dictionary[i]
            Y=pd.DataFrame(calculate_beta(X))
            firsttime=0
            
        else:
            tempX=dictionary[i]
            tempY=pd.DataFrame(calculate_beta(tempX))

            X=pd.concat([X,tempX])
            Y=pd.concat([Y,tempY])

    X.to_csv('X.csv',index=False)
    Y.to_csv('Y.csv',index=False)

    return X,Y



#Trains the model
def model():

    global thresh
    global download_option

    if download_option==1:
        trueX,trueY=data_fetch()
    else:
        trueX=pd.read_csv('X.csv')
        trueY=pd.read_csv('Y.csv')
        

    
    X,Y=trueX,trueY
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
    

#Learning curves
##    train_sizes=list(range(1,627,15))
##    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
##    plot_learning_curve(Ridge(alpha=a),'Learning Curves',X,Y,cv=50)


    
#Model training and predictions    
    reg = Ridge(alpha=a)
    reg.fit(X_train,Y_train)

    

    
    Y_test_pred = reg.predict(X_test)
    Y_CV_pred = reg.predict(X_CV)
    Y_train_pred=reg.predict(X_train)
    
    dump(reg,'R_model.joblib')
    
    print("\nTraining set fitting score:",met.r2_score(Y_train,Y_train_pred),"\nCV set fitting score",
          met.r2_score(Y_CV,Y_CV_pred),"\nTest set fitting score", met.r2_score(Y_test,Y_test_pred))

##    print(reg.coef_)
##    print(trueX.columns.values)
    plt.show()

        


    time.sleep(1)

    
##    S  = plt.scatter(X_train[:,indx],Y_train,color='red', s=1,marker = 'x',linewidths=None)
##    plt.scatter(X_test[:,indx],Y_test_pred,color = 'black', s=1)
##    plt.scatter(X_test[:,indx],Y_test,color = 'teal', s=1)
##
##
##
##
##    plt.show()



    return 0



#Function that predicts beta given new data X
def predict(X,country,scenario=False):

    if len(X)>3:
        scenario=True

    static=get_static()
    static_values=pd.Series(static[country])


    X=pd.Series(X)
    if not scenario:
        _,measures = get_data_dicts()
        measure_values=pd.Series(measures[country].iloc[-1])
        X = pd.concat([X,measure_values,static_values],ignore_index=True,join='outer',axis=0)
    
    else:
        X = pd.concat([X,static_values],ignore_index=True,join='outer',axis=0)


    X=X.to_numpy().reshape(1,-1)   
    
    reg = load('R_model.joblib')
    min_max_scaler = load('scaler.joblib')
    poly = load('poly.joblib')

    
    if polynomial_features_check == 1:
        
        X = poly.transform(X)

    if scaling_check==1:
        
        X =min_max_scaler.transform(X)


    new_beta = reg.predict(X)

    
    return new_beta




##settings()
##while(True):
##    model()
