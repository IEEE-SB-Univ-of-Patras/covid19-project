import datetime
import matplotlib.pyplot as plt
import numpy as np
##from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
import worldometer_scrapping
from sklearn.utils import shuffle
import math





R0 = 2.45  # Basic Reproductive Rate, number of transmissions/infected person in a 100% susceptible population.
days_of_infectivity = 10  # period during which the infected remain infectious
recovery_rate = 1 / days_of_infectivity
transmission_rate = R0 * recovery_rate  

def model():



##Getting the data from worldometer_scrapping (same code as SIR_prediction        
    data = worldometer_scrapping.mine_data(scope = 'world')

    n = data["demographics"]["population"]

    total_list = data["cases"]  # The list that contains total confirmed cases day by day.
    deaths_list = data["deaths"]  # The list of total deaths day by day.
    R_list = data["recovered"]  # Contains the total non-active (removed/recovered) cases day by day.
    I_list = data["active"]  # Contains the total active cases (infected/infectious) day by day.
    S_list = []  # Contains the susceptible population numbers (not infected, not removed).
    for i, val in enumerate(total_list):
        S_list.append(n - val)  # Total p


#Finding the length of our data (indicies might represent days later)
    m=len(S_list)
#Finding the 20% mark to split our data into training and testing sets
    thresh=int(0.2*m)
    
#Initializing the X and Y arrays. X array represents all the data we are gathering
#and Y represents the values of β. We initialize both of them with zero initial conditions
#(X array originially contains S, I, R in that order so initializing S is done by equalizing it
#to the world's population
    X=np.array([n ,0,0])
    Y=np.array(0)

#Concatenating the rest of the data
    for i in range(len(S_list)):

#Vertically stacking the S,I,R values from the lists we got from worldometer_scrapping
        X=np.vstack([X,[S_list[i],I_list[i],R_list[i]]])

#Condition for the first day of the pandemic        
        if i==0:
            b=transmission_rate
#Calculating the rest according to the formula we derived from the SIR model
        else:
            b=(S_list[i-1]-S_list[i])*n/(S_list[i-1]*I_list[i-1])
#Adding the β values to our result vector Y, note that there are real values not estimates            
        Y=np.vstack([Y,[b]])



#We could test shuffling the data for better results
##    X = shuffle(X)


#Scaling our data. We need to scale them into smaller values because the difference
#between S,I and R is usually approximating the world's population
    min_max_scaler = MinMaxScaler(feature_range=(0,0.5))
    X_scaled = min_max_scaler.fit_transform(X)


#At this point we could try and find out the best order of polynomial equation to use
#with linear regression
##    max_score=-math.inf
##    power=0
    
##    for i in range(1,25):
##        X_temp=X_scaled
##        
##        poly = PolynomialFeatures(i)
##        X_temp = poly.fit_transform(X_scaled)
##        
##
##        X_train=X_temp[:-thresh]
##        X_test=X_temp[-thresh:]
##
##        
##        
##
##        Y_train=Y[:-thresh]
##        Y_test=Y[-thresh:]
##
##          
##        reg =linear_model.Ridge(alpha=1).fit(X_train,Y_train)
##        score = reg.score(X_test,Y_test)
##        print(score,max_score)
##        if score>max_score:
##            power = i
##            max_score = score

        
##    print(power,max_score)


#Creating more features representing the polynomials of our existing data
    poly = PolynomialFeatures(2)
    X_scaled= poly.fit_transform(X_scaled)
    

#Dividing the data into training and testing sets
    X_train=X_scaled[:-thresh]
    X_test=X_scaled[-thresh:]

    
    Y_train=Y[:-thresh]
    Y_test=Y[-thresh:]


#creating our model    
    reg = linear_model.Ridge()

#Could be used to find the best possible regularization parameter, didn't seem to give
#better results
##    reg = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))

#Fitting the training set into the model so we get our estimator  
    reg.fit(X_train,Y_train)
#Printing the scores on training and testing sets (not sure how the are caluclated)    
    print(reg.score(X_train,Y_train), reg.score(X_test,Y_test))

#Giving the predictions for the test set
    Y_pred = reg.predict(X_test)




#Plotting the estimated β value according to each of the values S,I,R
    plt.subplot(2,2,1)

#Plots for S
#Plotting the training data (real values)
    S  = plt.scatter(X_train[:,1],Y_train,color='red', s=1,marker = 'x',linewidths=None)
#Plotting the predicted values for the test set
    plt.scatter(X_test[:,1],Y_pred,color = 'black', s=1)
#Plotting the real values for the test set for comparison
    plt.scatter(X_test[:,1],Y_test,color = 'teal', s=1)

#Same pattern for I
    plt.subplot(2,2,2)
    I = plt.scatter(X_train[:,2],Y_train,color='blue', s=1,marker = 'x',linewidths=None)
    plt.scatter(X_test[:,2],Y_pred,color = 'black', s=1)
    plt.scatter(X_test[:,2],Y_test,color = 'teal', s=1)


#Same pattern for R
    plt.subplot(2,2,3)
    R = plt.scatter(X_train[:,3],Y_train,color='green', s=1,marker = 'x',linewidths=None)
    plt.scatter(X_test[:,3],Y_pred,color = 'black', s=1)
    plt.scatter(X_test[:,3],Y_test,color = 'teal', s=1)


##    plt.legend((S,I,R),('S','I','R'), loc='upper right')
    plt.show()

    return 0


model()
