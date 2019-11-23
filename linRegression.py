import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
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
    #x = np.delete(data, 0, 1)
    #print(y)
    #print(X)
    time1 = time.time()
    print("Starting model build...")
    #print(X.head(400))
    #print(y.head(400))
    #print(X.iloc[2321, :])
    
    reg = LinearRegression().fit(X, y)
    print(reg.predict([X.iloc[2321, :]]))
    time2electricboogaloo = time.time()
    print("Finished model, Time: ", time2electricboogaloo - time)
    print(reg.coef_)
    
    #print(reg.predict(np.array([[13, 10, 3]])))
        
        
if __name__ == "__main__":
    main()