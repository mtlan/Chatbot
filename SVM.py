import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
#from sklearn import metrics
#import csv

# age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = "","","","","","","","","","","","",""
def svm_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # import dữ liệu
    data = pd.read_csv("E:/project/AI/New/HeartDisease.csv")
    
    train = data.drop('target', axis = 1)
    target = data.target
    
    # Tạo train/test set
    # Chia dữ liệu và test theo tỉ lệ 70-30
    X_train, X_test, y_train, y_test = train_test_split( train, target, test_size = 0.3, random_state = 109 )
    
    # Tạo bộ phân loại SVM tuyến tính
    clf = svm.SVC( kernel = 'linear' )
    # Train a Linear SVM classifier
    clf.fit(X_train, y_train)
    
    NewData = [[38,1,2,138,175,0,1,173,0,0,2,4,2], [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]

    result = clf.predict(NewData)[1]
    # print result
    
    # # nếu dữ liệu khớp trong dataset thì trả về 1 và ngược lại
    return result
    
