from django.shortcuts import render, redirect
from ml.models import Survive
from ml.forms import SurviveForm
from django.contrib.auth.decorators import login_required
# from django.http.response import HttpResponse
from sklearn import preprocessing 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import random

import pickle

@login_required
def ml(request):
    context = {}
    template = 'ml/ml.html'
    user = request.user
    surviveForm = SurviveForm(user=user)
    survives = Survive.objects.all()
    countS = Survive.objects.filter(survive=1).count()
    countD = Survive.objects.filter(survive=0).count()
    context.update({'survives':survives, 'countS':countS, 'countD':countD})
    print(countS, countD)
    context.update({'surviveForm':surviveForm})
    
    return render(request, template, context)



def train(request):
    #path = 'C:/Users/帥哥/webapps/git/iot/iot/ml/'
    path = 'ml/'
    print('readcsv...')
    train = pd.read_csv(path+"train.csv")
    test = pd.read_csv(path+"test.csv")
    print('done\n')
    print('preprocess...')
    data = train.append(test)
    data.reset_index(inplace=True, drop=True)
    data['Family_Size'] = data['Parch'] + data['SibSp']
    data['Title1'] = data['Name'].str.split(", ", expand=True)[1]
    data['Title1'] = data['Title1'].str.split(".", expand=True)[0]
    data['Title2'] = data['Title1'].replace(['Mlle','Mme','Ms','Dr','Major','Lady','the Countess','Jonkheer','Col','Rev','Capt','Sir','Don','Dona'],
         ['Miss','Mrs','Miss','Mr','Mr','Mrs','Mrs','Mr','Mr','Mr','Mr','Mr','Mr','Mrs'])
    data['Ticket_info'] = data['Ticket'].apply(lambda x : x.replace(".","").replace("/","").strip().split(' ')[0] if not x.isdigit() else 'X')
    data['Embarked'] = data['Embarked'].fillna('S')
    data['Fare'] = data['Fare'].fillna(data['Fare'].mean())
    data["Cabin"] = data['Cabin'].apply(lambda x : str(x)[0] if not pd.isnull(x) else 'NoCabin')
    
    data['Sex'] = data['Sex'].astype('category').cat.codes
    data['Embarked'] = data['Embarked'].astype('category').cat.codes
    data['Pclass'] = data['Pclass'].astype('category').cat.codes
    data['Title1'] = data['Title1'].astype('category').cat.codes
    data['Title2'] = data['Title2'].astype('category').cat.codes
    data['Cabin'] = data['Cabin'].astype('category').cat.codes
    data['Ticket_info'] = data['Ticket_info'].astype('category').cat.codes
    
    dataAgeNull = data[data["Age"].isnull()]
    dataAgeNotNull = data[data["Age"].notnull()]
    remove_outlier = dataAgeNotNull[(np.abs(dataAgeNotNull["Fare"]-dataAgeNotNull["Fare"].mean())>(4*dataAgeNotNull["Fare"].std()))|
                          (np.abs(dataAgeNotNull["Family_Size"]-dataAgeNotNull["Family_Size"].mean())>(4*dataAgeNotNull["Family_Size"].std()))                     
                         ]
    rfModel_age = RandomForestRegressor(n_estimators=2000,random_state=42)
    ageColumns = ['Embarked', 'Fare', 'Pclass', 'Sex', 'Family_Size', 'Title1', 'Title2','Cabin','Ticket_info']
    rfModel_age.fit(remove_outlier[ageColumns], remove_outlier["Age"])
    
    ageNullValues = rfModel_age.predict(X= dataAgeNull[ageColumns])
    dataAgeNull.loc[:,"Age"] = ageNullValues
    data = dataAgeNull.append(dataAgeNotNull)
    data.reset_index(inplace=True, drop=True)
    print('done\n')
    print('split...')
    dataTrain = data[pd.notnull(data['Survived'])].sort_values(by=["PassengerId"])
    dataTest = data[~pd.notnull(data['Survived'])].sort_values(by=["PassengerId"])
    
    dataTrain = dataTrain[['Survived', 'Age', 'Embarked', 'Fare',  'Pclass', 'Sex', 'Family_Size', 'Title2','Ticket_info','Cabin']]
    dataTest = dataTest[['Age', 'Embarked', 'Fare', 'Pclass', 'Sex', 'Family_Size', 'Title2','Ticket_info','Cabin']]
    print('done\n')
    print('classify...')
    rf = RandomForestClassifier(criterion='gini', 
                             n_estimators=1000,
                             min_samples_split=12,
                             min_samples_leaf=1,
                             oob_score=True,
                             random_state=1,
                             n_jobs=-1) 

    rf.fit(dataTrain.iloc[:, 1:], dataTrain.iloc[:, 0])
    print(rf)
    print("%.4f" % rf.oob_score_)
    
    trainedClassifier = open('model.pickle', 'wb')
    print('done\n')
    print('pickle...')
    pickle.dump(rf, trainedClassifier)
    trainedClassifier.close()
    print('done')
    return redirect('main:main')
    
@login_required    
def isSurvive(request):
    '''
    TODO :Recieve the ajax data(age,carbin,ticket... ) to classifier if he/she can survive and return 1 or 0 
    '''
    template = 'ml/ml.html'
    user = request.user
    Ticket_info_temp = random.randint(1, 36)
    context = {}
    surviveForm = SurviveForm(request.POST, user=user)
    if not surviveForm.is_valid():
        context.update({'surviveForm':surviveForm})
        return render(request, template, context)
    
    survive = surviveForm.save(commit=False)
    #path = 'C:/Users/帥哥/webapps/git/iot/iot/ml/'
    path = 'ml/'
    with open(path+'model.pickle', 'rb') as f:
        trainedClassifier = pickle.load(f)
        
    isSurvived = trainedClassifier.predict([[survive.Age, survive.Embarked, survive.Fare, survive.Pclass, survive.Sex, survive.Family_Size, survive.Title2, Ticket_info_temp, survive.Cabin]])
    
    
    survive.Ticket_info = Ticket_info_temp
    survive.user = user
    survive.survive = isSurvived
    survive.save()
    
    survives = Survive.objects.all()
    context.update({'survives':survives})
    context.update({'surviveForm':SurviveForm(user=user)})
    context.update({'isSurvived':isSurvived})
    
    return render(request, template, context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    