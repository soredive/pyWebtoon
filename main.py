# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os,urllib

url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=666671&no=1&weekday=sun'

def ExtNaverWebtoonImg(webtoonUrl):
    html = urlopen(webtoonUrl)
    bsObj = BeautifulSoup(html,'html.parser') 
    return [el.get('src') for el in bsObj.find_all('img') if el.get('src')]

def SaveSrcImgTo(imgList, szFolder): 
    for img in imgList:
        try:
            urlretrieve(img, szFolder + os.path.basename(img)) #링크 파일 다운로드 
        except urllib.error.HTTPError as err:
            print('ErrCode:',err.code, img)
            
jpgSrc = ExtNaverWebtoonImg(url) #이미지 주소 리스트 얻기
SaveSrcImgTo(jpgSrc,'.\\')
