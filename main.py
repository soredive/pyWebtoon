# -*- coding: utf-8 -*-

from urllib.request import *
from urllib.parse import *
from bs4 import BeautifulSoup
import os


def ExtNaverWebtoonImg(webtoonUrl):
	html = urlopen(webtoonUrl)
	bsObj = BeautifulSoup(html,'html.parser') 
	return [el.get('src') for el in bsObj.find_all('img') if el.get('src')]

def SaveSrcImgTo(imgList, szFolder):
	try:
		os.mkdir(szFolder)
	except FileExistsError:
		pass
	for img in imgList:
		path = os.path.normpath(szFolder + '\\' + os.path.basename(img))
		req = Request(img)
		req.add_header('Referer',url)
		data = urlopen(req).read()
		with open(path,'wb') as fp:
			fp.write(data)



##--Useage--##

url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=666671&no=1&weekday=sun'

imgList = ExtNaverWebtoonImg(url) #이미지 주소 리스트 얻기
toonCut  = filter(lambda x:x.startswith('http://imgcomic.naver.net'),imgList) #웹툰컷 이외의 이미지 필터링
SaveSrcImgTo(toonCut,'.\\downloadimg') 
