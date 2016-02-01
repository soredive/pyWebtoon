# -*- coding: utf-8 -*-

from urllib.request import *
from urllib.parse import *
from bs4 import BeautifulSoup
import os, re


class NaverWebtoonImgScraper:
	def __init__(self, webtoonUrl):
		self.webtoonUrl = webtoonUrl
		self.html = urlopen(webtoonUrl).read().decode()
		self.bsObj = BeautifulSoup(self.html,'html.parser')
	def GetWebtoonTitle(self):
		metaTag = self.bsObj.find_all('meta',{'property':'og:title'})
		return metaTag[0].get('content')
	
	def ExtWebtoonImgList(self):
		return [el.get('src') for el in self.bsObj.find_all('img') if el.get('src')]
	
	def SaveSrcImgTo(self, imgList, szFolder):
		try:
			os.mkdir(szFolder)
		except FileExistsError:
			pass
		for img in imgList:
			path = os.path.normpath(szFolder + '/' + os.path.basename(img))
			req = Request(img)
			req.add_header('Referer',self.webtoonUrl)
			data = urlopen(req).read()
			with open(path,'wb') as fp:
				fp.write(data)
	
	def GetCommentUrl(self):
		urlprs = urlparse(self.webtoonUrl)
		url_reExp = "naver\.comic\.sNCommentUrl\s*=\s*'(.*?)'"
		find = re.search(url_reExp, self.html)
		return urlunparse((urlprs.scheme,urlprs.netloc,find.group(1),'','',''))

#Lib Useage
'''
url = "http://comic.naver.com/webtoon/detail.nhn?titleId=666671&no=1&weekday=sun"

wtScrp = NaverWebtoonImgScraper(url)

title = wtScrp.GetWebtoonTitle()
print(title)

webtoonCommentUrl = wtScrp.GetCommentUrl()
print('Comment Url: ',webtoonCommentUrl)


imgList = wtScrp.ExtWebtoonImgList()
wtScrp.SaveSrcImgTo(imgList,'.'+os.sep+'webtoonimg')

'''

