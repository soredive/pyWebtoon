# -*- coding: utf-8 -*-

from urllib.request import *
from urllib.parse import *
from bs4 import BeautifulSoup
import os, re


class NaverWebtoonImgScraper:
	def __init__(self, webtoonUrl):
		self.webtoonUrl = webtoonUrl
		self.html = urlopen(webtoonUrl).read().decode()
	
	def ExtWebtoonImgList(self):
		bsObj = BeautifulSoup(self.html,'html.parser') 
		return [el.get('src') for el in bsObj.find_all('img') if el.get('src')]
	
	def SaveSrcImgTo(self, imgList, szFolder):
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
	
	def GetCommentUrl(self):
		urlprs = urlparse(self.webtoonUrl)
		url_reExp = "naver\.comic\.sNCommentUrl\s*=\s*'(.*?)'"
		find = re.search(url_reExp, self.html)
		return urlprs.netloc + find.group(1)



