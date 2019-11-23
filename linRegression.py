import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import pandas
import time
import os

def main():
    #f = open("proc_cars.csv")
    cwd = os.getcwd()
    data = pandas.read_csv(cwd + "/car_data/proc_cars.csv")
    data = data.drop(columns = ['Unnamed: 0'])
    #print(dummyData)
    
    #print(dummyData.loc[dummyData['DAYTIMERUNLIGHTS'] == 0.0]['DAYTIMERUNLIGHTS'].count)
    #print(data)
    #print(titles)
    y = data['MSRP']
    X = data.drop(columns = ['MSRP'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    #x = np.delete(data, 0, 1)
    #print(y)
    #print(X)
    time1 = time.time()
    print("Starting model build...")
    #print(X.head(400))
    #print(y.head(400))
    #print(X.iloc[2321, :])
    print("building model.")

    #reg = LinearRegression().fit(X_train, y_train)
    #svm = SVR(kernel = 'poly',gamma='scale', C=100).fit(X_train, y_train)
    ridge = Ridge().fit(X_train, y_train)
    print("Model built")

    error = []
    for i in range(0, X_test.shape[0]):
        #x = reg.predict([X_test.iloc[i, :]])
        x = ridge.predict([X_test.iloc[i, :]])
        #x = svm.predict([X_test.iloc[i, :]])
        val = y_test.iloc[i]
        #print(x)
        #print(val)
        #print(abs((x-val)/val))
        error.append(abs(x-val)/val)
    
    
    print(np.max(error))
    print(np.min(error))
    print(np.mean(error))

    time2electricboogaloo = time.time()
    #print("Finished model, Time:%d" % (time2electricboogaloo - time))
    print("Finished model")
    print(ridge.score(X_test,y_test))
    params = ridge.get_params()
    print(params)
    #print(reg.coef_)
    #print(ridge.coef_)
    #print(reg.predict(np.array([[13, 10, 3]])))
        
        
if __name__ == "__main__":
    main()