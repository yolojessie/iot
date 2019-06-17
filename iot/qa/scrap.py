# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 22:23:02 2019

@author: student
"""
from django.http.response import HttpResponse
import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrapPTT(request):
    def GetContent(URL):
        myR=rs.get(URL)
        mySoup=BeautifulSoup(myR.text,'lxml')
        try:
            myContent=mySoup.select('#main-content')[0].text
        except:
            myContent="404 - Not Found."
            #print("404 - Not Found."+URL)
        return myContent
    
    def GetLastPage(mysoup):
        global basicURL
        class_btn=soup.select('.btn')
        lastURL=basicURL+class_btn[len(class_btn)-3].attrs.get('href')
        return lastURL
    
    def GetParaph(mysoup):
        global jData
        global basicURL
        global today
        global chances
        flag=0
        for entry in mysoup.select('.r-ent'):
            tweets=entry.select('.nrec')[0].text
            title=entry.select('.title')[0].text
            
            date=entry.select('.date')[0].text.strip()
            author=entry.select('.author')[0].text
            if "刪除" in title:
                url=""
                content=""
            else:
                url=basicURL+entry.select('.title')[0].select('a')[0].attrs.get('href')
                content=GetContent(url)
            #print(date)
            if chances > 0:
                if date!=today:
                    chances-=1
                    continue
                else:
                    chances=10
            else:
                flag=1
                break
            jData.append({"tweets":tweets,"title":title,"date":date,"author":author,"url":url,"content":content})
        return flag
    
    

    url="https://www.ptt.cc/ask/over18"
    payload={'from': '/bbs/Gossiping/index.html',
            'yes': 'yes'}
    rs=requests.session()
    r=rs.post(url,data=payload)
    r=rs.get('https://www.ptt.cc/bbs/Gossiping/index.html')
    soup=BeautifulSoup(r.text,'lxml')
    basicURL='https://www.ptt.cc'
    jData=[]
    chances=10
    flag_stop=0
    date = datetime.datetime.now()
    today=str(date.month)+"/"+str(date.day)
  
    while(1):
        if(flag_stop):
            break
        flag_stop=GetParaph(soup)
        lURL=GetLastPage(soup)
        #print(lURL)
        r=rs.get(lURL)
        soup=BeautifulSoup(r.text,'lxml')
        
    
    with open('Gossiping.json', 'w') as outfile:
        json.dump(jData, outfile)
        
    return HttpResponse(True)