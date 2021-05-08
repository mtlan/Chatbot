import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
#from sklearn import metrics
#import csv

# age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = "","","","","","","","","","","","",""
def svm_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    data = pd.read_csv("E:/project/AI/New/HeartDisease.csv")
    
    train = data.drop('target', axis = 1)
    target = data.target
    
    X_train, X_test, y_train, y_test = train_test_split( train, target, test_size = 0.3, random_state = 109 )
    
    clf = svm.SVC( kernel = 'linear' )
    clf.fit(X_train, y_train)
    
    NewData = [[38,1,2,138,175,0,1,173,0,0,2,4,2], [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]

    result = clf.predict(NewData)[1]
    # print result
    
    # # nếu dữ liệu khớp trong dataset thì trả về 1 và ngược lại
    return result
    
