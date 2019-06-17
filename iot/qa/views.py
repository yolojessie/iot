from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.http.response import HttpResponse
import pandas as pd
import numpy as np
from numpy.linalg import norm
import random

import pickle

#wordcloud
import jieba
import jieba.analyse
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import json
import os
from account.models import User
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler
# 前處理
jieba.set_dictionary('dict.txt.big') #輸入繁體字典
Idf_vector = []
termindex = []
all_terms = []
termindexLen = 0
def preprocess(item):  ##定義前處理的function
    terms = [t for t in jieba.cut_for_search(item)]  ## 把全切分模式打開，可以比對的詞彙比較多
    all_terms.extend(terms)  ## 收集所有出現過的字
    return terms

def terms_to_vector(terms):  ## 定義把terms轉換成向量的function
    vector = np.zeros_like(termindex, dtype=np.float32)  ## 建立一條與termsindex等長、但值全部為零的向量
    for term in terms:
        if term in termindex: 
            idx = termindex.index(term)  ## 測試時如果有字沒有在索引中，需要保護
            vector[idx] += 1  ## 計算term frequency
    vector = vector * Idf_vector  ## 如果兩個vector的型別都是np.array，把兩條vector相乘，就會自動把向量中的每一個元素成在一起，建立出一條新的向量
    return vector   

def toint(num):
        return int(num)
     

df_QA = pd.read_json('qa/Gossiping.json', encoding='utf8')# ProcessedData
df_QA = df_QA[:1000]
temp_df = df_QA['tweets']
temp_df[temp_df==''] = 0
df_QA['tweets'] = temp_df
#10以下綠色以上黃色100以上爆 X是10以上噓XX是100以上
temp_df[temp_df=='X1'] = -10
temp_df[temp_df=='X2'] = -20
temp_df[temp_df=='X3'] = -30
temp_df[temp_df=='X4'] = -40
temp_df[temp_df=='X5'] = -50
temp_df[temp_df=='X6'] = -60
temp_df[temp_df=='X7'] = -70
temp_df[temp_df=='X8'] = -80
temp_df[temp_df=='X9'] = -90
temp_df[temp_df=='XX'] = -100
temp_df[temp_df=='爆'] = 100
df_QA['tweets'] = temp_df   
df_QA['tweets'] = df_QA['tweets'].apply(toint)
df_question = df_QA[['title', 'url', 'tweets']].copy()  ## 不要更動到原始的DataFrame
df_question.drop_duplicates(inplace=True)  ## 丟掉重複的資料
df_question['processed'] = df_question['title'].apply(preprocess)
print('preprocess...done')
termindex = list(set(all_terms))  ## 用set轉型可以將list中重複的部分拿掉
termindexLen = len(termindex)
Doc_Length = len(df_question)  ## 計算出共有幾篇文章
for term in termindex:  ## 對index中的詞彙跑回圈
    num_of_doc_contains_term = 0  ## 計算有機篇文章出現過這個詞彙
    for terms in df_question['processed']:
        if term in terms:
            num_of_doc_contains_term += 1
    idf = np.log(Doc_Length/num_of_doc_contains_term)  ## 計算該詞彙的IDF值
    Idf_vector.append(idf)

df_question['vector'] = df_question['processed'].apply(terms_to_vector)  ## 將上面定義的f
print('idf...done')
df_vector = df_question
 
    
    
def qa(request):
    keyword = request.user.keyword
    tweets = None
    if keyword:
        tweets = predict_tweets(keyword)  
    labels,values = hotKeyword(df_vector)
    context = {'answer':'', 'keyword':keyword, 'tweets':tweets
               , 'labels':labels, 'values':values}
    template = 'qa/qa.html'
   
    return render(request, template, context)

@login_required
def answer(request): 
    context = {}
    # 把檔案讀出來
    # 我們這次只會使用到title跟url這兩個欄位 
    df_ans = retrieve(str(request.GET['q']))
    print('retrieve...done')
    result = []
    tweets = None
    for q in df_ans[['title','url']].values:
        result.append({'title':q[0],'url':q[1]})
    print('result message...done')  
    keyword = request.user.keyword
    
    if keyword:
        tweets = predict_tweets(keyword) 
    labels,values = hotKeyword(df_vector) 
    context.update({'aswer':result, 'keyword':keyword, 'tweets':tweets
                    , 'labels':labels, 'values':values})
    
    return render(request, 'qa/qa.html',context)

def cloud(request):
    all_terms_cloud = []
    with open('qa/stops.txt', 'r', encoding='utf8') as f:  
        stops = f.read().split('\n') 
    stops.append('問卦')
    stops.append('https')
    stops.append('jpg')
    for n in range(100):
        stops.append(str(n))
    stops.append('\n')
    stops.append('\n\n')
    stops.append('\nRe')
    stops.append('新聞')
    # 把檔案讀出來
    df_QA = pd.read_json('qa/Gossiping.json', encoding='utf8')# ProcessedData
    # 我們這次只會使用到title跟url這兩個欄位
    df_question = df_QA[['title', 'content']].copy()  ## 不要更動到原始的DataFrame
    df_question.drop_duplicates(inplace=True)  ## 丟掉重複的資料
    
    def preprocess_extract(item):  ##定義前處理的function
        terms = [t for t in jieba.analyse.extract_tags(item, topK=20) if t not in stops]  ## 把全切分模式打開，可以比對的詞彙比較多
        all_terms_cloud.extend(terms)  ## 收集所有出現過的字
        return terms
    df_question['processed'] = df_question['title'].apply(preprocess_extract)
    cloud_pct = plt.imread('cloud.jpg')
    wordcloud = WordCloud(background_color='white',
                              mask=cloud_pct,
                              font_path="qa/simsun.ttf")  ##做中文時務必加上字形檔
    wordcloud.generate_from_frequencies(frequencies=Counter(all_terms_cloud))
    
#     plt.figure(figsize=(15,15))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     plt.show()
    wordcloud.to_file('static/qa/img/month_terms.jpg')
    return redirect('qa/qahtml')
    
    
    
def cosine_similarity(vector1, vector2):  ## 定義cosine相似度的計算公式
    score = np.dot(vector1, vector2)  / (norm(vector1) * norm(vector2))
    return score


def preprocessSentence(item):  ##定義前處理的function
    terms = [t for t in jieba.cut_for_search(item)]  ## 把全切分模式打開，可以比對的詞彙比較多
    return terms



def retrieve(testing_sentence, return_num=3):  ## 定義出檢索引擎
    testing_vector = terms_to_vector(preprocessSentence(testing_sentence))  ## 把剛剛的前處理、轉換成向量的function，應用在使用者輸入的問題上
    score_dict = {}  ## 準備把每一個問題對應到使用者問題的cosine分數記錄下來
    df_vector_sorted = df_vector.sort_index(ascending=True)
    for idx, vec in enumerate(df_vector_sorted['vector']):  ## 計算每一個問題與使用者問題的cosine分數
        score = cosine_similarity(testing_vector, vec)
        score_dict[idx] = score
    idxs = np.array(sorted(score_dict.items(), key=lambda x:x[1], reverse=True))[:return_num, 0]  ##排序出最相關的前N個問題的row index
#     print(df_vector[:5])
#     print(df_vector_sorted[:5])
#     print(df_vector_sorted.loc[0,['vector']][0])
#     for i in idxs:
#         print(i)
#         print(score_dict[i])
#     print('cosine:')
#     print(cosine_similarity(df_vector_sorted.loc[348,['vector']][0],testing_vector))
#     print(df_vector_sorted.loc[idxs, ['title', 'url','processed']])
    return df_vector_sorted.loc[idxs, ['title', 'url']]

@login_required
def saveKeyword(request):
    '''
    TODO:把這個function做成ajax
    '''
    user = request.user
    keyword = request.GET['keyword']
    users = User.objects.filter(fullName=user.fullName)
    for user in users:
        user.keyword = keyword
        user.save()
    tweets = predict_tweets(keyword)
    labels,values = hotKeyword(df_vector) 
    context = {'answer':'', 'keyword':keyword, 'tweets':tweets
               , 'labels':labels, 'values':values}
    template = 'qa/qa.html'

    return render(request, template, context)



def train_model(request):
    scaler = MinMaxScaler()
    scaler.fit(df_vector['tweets'].values.reshape(-1,1))
    y_train = scaler.transform(df_vector['tweets'].values.reshape(-1,1))
    temp = df_vector['vector'].copy()
    def tolist(ndarray):
        return list(ndarray)
    temp = temp.apply(tolist)
    temp = list(temp.values)
    x = np.array(temp)
    xgr = XGBRegressor(n_estimators=300, learning_rate=0.01, gamma=0, subsample=0.85,
                            colsample_bytree=0.8, max_depth=20, min_child_weight = 11,n_jobs = 4)
    X_train, X_test, y_train, y_test = train_test_split(x, y_train, test_size=0.2, random_state=42)
    xgr.fit(X_train, y_train,eval_set=[(X_train, y_train), (X_test, y_test)], early_stopping_rounds=200)
    print('open file..\n')
    trainedReggresor = open('qa/xgbmodel.pickle', 'wb')
    print('done\n')
    print('xgbmodel pickle...')
    pickle.dump(xgr, trainedReggresor)
    trainedReggresor.close()
    print('done')
    
    print('open file..\n')
    trainscaler = open('qa/scaler.pickle', 'wb')
    print('done\n')
    print('scaler pickle...')
    pickle.dump(scaler, trainscaler)
    trainscaler.close()
    print('done')
    return redirect('qa/qa.html')


def predict_tweets(keyword):
    path = 'qa/'
    with open(path+'xgbmodel.pickle', 'rb') as f:
        trainedReggresor = pickle.load(f)
    with open(path+'scaler.pickle', 'rb') as f:
        trainedscaler = pickle.load(f)
    terms = [t for t in jieba.analyse.extract_tags(keyword, topK=10)]
    question = terms_to_vector(terms)
    question = question.reshape(1,termindexLen)
    tweets = trainedReggresor.predict(question).reshape(-1,1)
    tweets = trainedscaler.inverse_transform(tweets)
    tweets = int(tweets)

    return tweets
    
    
    
def hotKeyword(df_vector):
    with open('qa/stops.txt', 'r', encoding='utf8') as f:  
        stops = f.read().split('\n') 
    stops.append('\n')
    stops.append('\t')
    df_QA_sort = df_vector.sort_values(by=['tweets'],ascending=False)
    df_QA_sort = df_QA_sort[:100]
    top100vectors = list(df_QA_sort['processed'].values)
    top100terms = []
    for item in top100vectors:
        for i in item:  
            if i not in stops: 
                top100terms.append(i)
    count = Counter(top100terms).most_common(10)
    labels = {}
    values = []
    for c in count:
        labels.update({str(c[0]):str(c[0])})
        values.append(c[1])
    return labels,values
    
    
    
    
    
    
    