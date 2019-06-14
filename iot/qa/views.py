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
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import json
import os
from account.models import User
# 前處理
jieba.set_dictionary('dict.txt.big') #輸入繁體字典
Idf_vector = []
termindex = []
all_terms = []
df_QA = pd.read_json('Gossiping.json', encoding='utf8')# ProcessedData
df_question = df_QA[['title', 'url']].copy()  ## 不要更動到原始的DataFrame
df_question.drop_duplicates(inplace=True)  ## 丟掉重複的資料
def preprocess(item):  ##定義前處理的function
    terms = [t for t in jieba.cut(item, cut_all=True)]  ## 把全切分模式打開，可以比對的詞彙比較多
    all_terms.extend(terms)  ## 收集所有出現過的字
    return terms
df_question['processed'] = df_question['title'].apply(preprocess)
print('preprocess...done')
termindex = list(set(all_terms))  ## 用set轉型可以將list中重複的部分拿掉
Doc_Length = len(df_question)  ## 計算出共有幾篇文章
Idf_vector = []  ## 初始化IDF向量
for term in termindex:  ## 對index中的詞彙跑回圈
    num_of_doc_contains_term = 0  ## 計算有機篇文章出現過這個詞彙
    for terms in df_question['processed']:
        if term in terms:
            num_of_doc_contains_term += 1
    idf = np.log(Doc_Length/num_of_doc_contains_term)  ## 計算該詞彙的IDF值
    Idf_vector.append(idf)
def terms_to_vector(terms):  ## 定義把terms轉換成向量的function
    vector = np.zeros_like(termindex, dtype=np.float32)  ## 建立一條與termsindex等長、但值全部為零的向量
    for term in terms:
        if term in termindex: 
            idx = termindex.index(term)  ## 測試時如果有字沒有在索引中，需要保護
            vector[idx] += 1  ## 計算term frequency
    vector = vector * Idf_vector  ## 如果兩個vector的型別都是np.array，把兩條vector相乘，就會自動把向量中的每一個元素成在一起，建立出一條新的向量
    return vector    
df_question['vector'] = df_question['processed'].apply(terms_to_vector)  ## 將上面定義的f
print('idf...done')
    
    
    
def qa(request):
    keyword = request.user.keyword
    context = {'answer':'', 'keyword':keyword}
    template = 'qa/qa.html'
    cwd = os.getcwd()
    print(cwd)
    return render(request, template, context)

@login_required
def answer(request): 
    context = {}
    # 把檔案讀出來
    # 我們這次只會使用到title跟url這兩個欄位 
    df_ans = retrieve(str(request.GET['q']))
    print('retrieve...done')
    result = ''
    question = ''
    for q in df_ans['title']:
        question += q + '\n'
        question += str(df_ans[df_ans['title']==q]['url'].values[0]) + '\n'
    result += question
    print('result message...done')    
    context.update({'aswer':result, 'keyword':request.user.keyword})
    
    return render(request, 'qa/qa.html',context)

def cloud(request):
    all_terms_cloud = []
    with open('stops.txt', 'r', encoding='utf8') as f:  
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
    df_QA = pd.read_json('Gossiping.json', encoding='utf8')# ProcessedData
    # 我們這次只會使用到title跟url這兩個欄位
    df_question = df_QA[['title', 'content']].copy()  ## 不要更動到原始的DataFrame
    df_question.drop_duplicates(inplace=True)  ## 丟掉重複的資料
    
    def preprocess(item):  ##定義前處理的function
        terms = [t for t in jieba.cut(item, cut_all=True) if t not in stops]  ## 把全切分模式打開，可以比對的詞彙比較多
        all_terms_cloud.extend(terms)  ## 收集所有出現過的字
        return terms
    df_question['processed'] = df_question['title'].apply(preprocess)
    cloud_pct = plt.imread('cloud.jpg')
    wordcloud = WordCloud(background_color='white',
                              mask=cloud_pct,
                              font_path="simsun.ttf")  ##做中文時務必加上字形檔
    wordcloud.generate_from_frequencies(frequencies=Counter(all_terms_cloud))
    
#     plt.figure(figsize=(15,15))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     plt.show()
    wordcloud.to_file('month_terms.jpg')

    
    
    
def cosine_similarity(vector1, vector2):  ## 定義cosine相似度的計算公式
    score = np.dot(vector1, vector2)  / (norm(vector1) * norm(vector2))
    return score


def preprocessSentence(item):  ##定義前處理的function
    terms = [t for t in jieba.cut(item, cut_all=True)]  ## 把全切分模式打開，可以比對的詞彙比較多
    return terms



def retrieve(testing_sentence, return_num=3):  ## 定義出檢索引擎
    testing_vector = terms_to_vector(preprocessSentence(testing_sentence))  ## 把剛剛的前處理、轉換成向量的function，應用在使用者輸入的問題上
    score_dict = {}  ## 準備把每一個問題對應到使用者問題的cosine分數記錄下來
    for idx, vec in enumerate(df_question['vector']):  ## 計算每一個問題與使用者問題的cosine分數
        score = cosine_similarity(testing_vector, vec)
        score_dict[idx] = score
    idxs = np.array(sorted(score_dict.items(), key=lambda x:x[1], reverse=True))[:return_num, 0]  ##排序出最相關的前N個問題的row index
    return df_question.loc[idxs, ['title', 'url']]

@login_required
def saveKeyword(request):
    '''
    TODO:把這個function做成ajax
    '''
    user = request.user
    keyword = request.GET['keyword']
    user.keyword = keyword
    user.save()
    
    context = {'answer':'', 'keyword':keyword}
    template = 'qa/qa.html'
    return render(request, template, context)
