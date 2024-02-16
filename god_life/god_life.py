#from ast import Try
#from pickle import NONE
#import re
#from sqlite3 import Row
#from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

#크롬 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우저 생성
browser = webdriver.Chrome(options=chrome_options)




#소설 클래스
class Novel:
    def __init__ (self,title,view,recommend,episode,date):
        self.title=title
        self.view=view
        self.recommend=recommend
        self.episode=episode
        self.date=date


#크롤링
def Crawling():
    title=browser.find_element(By.CSS_SELECTOR, "body > div:nth-child(49) > div.epnew-wrapper.s_inv > div.epnew-novel-info > div.ep-info-line.epnew-novel-title").text
    view=browser.find_element(By.CSS_SELECTOR,"body > div:nth-child(49) > div.epnew-wrapper.s_inv > div.epnew-novel-info > div.ep-info-line.info-count1 > div.counter-line-a > p:nth-child(1) > span:nth-child(2)").text
    recommend=browser.find_element(By.CSS_SELECTOR,"body > div:nth-child(49) > div.epnew-wrapper.s_inv > div.epnew-novel-info > div.ep-info-line.info-count1 > div.counter-line-a > p:nth-child(2) > span:nth-child(2)").text
    try:#연재주기없을때
        episode=browser.find_element(By.XPATH,"/html/body/div[8]/div[1]/div[2]/div[5]/div[2]/div[1]/p[3]/span[2]").text
    except:#연재주기있을때
        episode=browser.find_element(By.XPATH,"/html/body/div[8]/div[1]/div[2]/div[6]/div[2]/div[1]/p[3]/span[2]").text
    
    try:
        date=browser.find_element(By.CSS_SELECTOR,"#episode_list > table > tbody > tr:nth-child(1) > td.font12 > div > font > span:nth-child(2) > b").text
    except:#아직첫화가안올라옴
        date="아직없음"
    
    b=Novel(title,view,recommend,episode,date)
    return(b)



f = open("data.csv", "w",newline="")
writer = csv.writer(f)
start=["번호","제목","조회수","화수","집필날짜"]
writer.writerow(start)

Number=0    #소설의 실질적개수
a=[]        #소설들어갈 리스트
out=0       #아웃제(프로그램종료 10)


for page in range(20,22,1):
    
    #웹페이지 접속
    url='https://novelpia.com/novel/'+str(page);
    browser.get(url)
    
    
    #소설정보 크롤링
    #print(str(page)+"번 시작")
    time.sleep(5)
    
    
    #try문
    try:
        a.append(Crawling())
        out=0
    
    #소설 없음확인
    except:
        if(browser.find_element(By.CSS_SELECTOR,"#alert_modal > div > div > div.modal-body.pd-20 > p").text=="잘못된 소설 번호 입니다."):
            out=out+1
        
            if (out==10):
                print("끝")
                break
            else:
                print(str(out)+"아웃")
                continue
        else:   
            #print(str(page)+"번없음")
            continue
    
    
    Number=Number+1
    print(a[Number-1].title, a[Number-1].view, a[Number-1].recommend, a[Number-1].episode, a[Number-1].date)
    data=[str(Number)+"번소설",a[Number-1].title, a[Number-1].view, a[Number-1].recommend, a[Number-1].episode[0:-2], a[Number-1].date]
    writer.writerow(data)

f.close()

    