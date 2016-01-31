# -*- coding: utf-8 -*-
import time, re ,math
from urllib.request import *
from urllib.parse import *
from urllib.error import *


class NaverWebtoonCommentScraper:
	def __init__(self, commentUrl, reqPageUnit = None): 
		self.html = urlopen(commentUrl).read().decode()
		self.url = commentUrl
		self.commentHost = 'http://comic.naver.com/comments/list_comment.nhn'
		tup_ToExt = ('lkey','ticket','objectId','pageSize')	
		self.keys = {}
		for key in tup_ToExt:
			reExp = "{}\s*:\s*(.*)".format(key)
			find = re.search(reExp,self.html)
			self.keys[key] = find.group(1).strip(" '\r\n\t")
		if reqPageUnit: self.keys['pageSize'] = reqPageUnit

	def GetCommentPage(self, nPage):
		formdata = 'ticket={}&object_id={}&_ts={}&lkey={}&page_size={}&page_no={}&sort=newest'\
		.format(self.keys['ticket'],self.keys['objectId'],int(time.time()*1000),self.keys['lkey'],self.keys['pageSize'],nPage)
		req = Request(self.commentHost,formdata.encode())
		req.add_header('Referer',self.url)
		return urlopen(req).read()
	
	def GetCommentsTotalPageCount(self):
		return math.ceil(eval(self.GetCommentPage(1))['total_count'] / int(self.keys['pageSize']))

	def GetCommentsTable(self, reqPgAsSeq, retry=2):  #range(1, 10 + 1) or {1,4,6,10,....} [2,3]
		ret = []; faultPage = {}
		if retry < 0: 
			faultPage[reqPgAsSeq[0]]=self.GetCommentPage(reqPgAsSeq[0])
			print('Page get fault ',reqPgAsSeq[0])
			return ret, faultPage
		for nPage in reqPgAsSeq:
			try:
				cmtObj = eval(self.GetCommentPage(nPage))
			except :
				print('retrying comment Page{} req...remained retry num({}):'.format(nPage, retry))
				time.sleep(0.5)
				subret, subfaultPage = self.GetCommentsTable(range(nPage,nPage+1), retry - 1)
				ret+=subret
				faultPage.update(subfaultPage)
			else:
				ret.append(cmtObj['comment_list'])

		return ret, faultPage
	
	def GetCommentsTableFields(self):
		return tuple(eval(self.GetCommentPage(1))['comment_list'][0].keys())

#Lib Useage

from NaverWebtoonImgScraper import *

wtScrp = NaverWebtoonImgScraper('http://comic.naver.com/webtoon/detail.nhn?titleId=666671&no=1&weekday=sun')
cmtUrl = wtScrp.GetCommentUrl()

cmtScrp = NaverWebtoonCommentScraper(cmtUrl,100) #args: naver webtoon comments url, req Page num, default==15
cPage = cmtScrp.GetCommentsTotalPageCount()

print('totalPage: ',cPage)

cmtTbl, faultPage = cmtScrp.GetCommentsTable(range(1, cPage + 1)) #returns resultTable and fault pages

print('Total Tuples:', len(cmtTbl))
print('faultPages:', faultPage)

