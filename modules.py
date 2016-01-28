import os, time, re ,math
import sqlite3
from urllib.request import *
from urllib.parse import *
from urllib.error import *


class NaverWebtoonCommentScraper:
	def __init__(self, commentUrl):
		self.html = urlopen(commentUrl).read().decode()
		self.url = commentUrl
		self.commentHost = 'http://comic.naver.com/comments/list_comment.nhn'
		tup_ToExt = ('lkey','ticket','objectId','pageSize')	
		self.keys = {}
		for key in tup_ToExt:
			reExp = "{}\s*:\s*(.*)".format(key)
			find = re.search(reExp,self.html)
			self.keys[key] = find.group(1).strip(" '\r\n\t")

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



class SQLite3DB:
	def __init__(self, dbName):
		self.db = sqlite3.connect(dbName)
		self.cursor = self.db.cursor()
		self.dbName = dbName

	def SetDBFromTable(self, tup_fields, list_tbl, tblName):
		fields = repr(tup_fields)
		self.cursor.execute('drop table if exists ' + tblName)
		self.db.commit()
		self.cursor.execute('create table ' + tblName + fields)
		self.db.commit()
		for cmtList in list_tbl:
			for tup in cmtList:
				insExp = 'insert into ' + tblName + ' values' + repr(tuple(tup.values()))
				try:
					self.cursor.execute(insExp)
				except sqlite3.OperationalError as err:
					missingKeys = set(tup_fields) - set(tup.keys())
					for mskey in missingKeys:
						tup[mskey] = 'NULL'
					insExp = 'insert into ' + tblName + ' values' + repr(tuple(tup.values()))
					self.cursor.execute(insExp)
		self.db.commit()

	def GetQueryFromDB(self, qry, toCsvFile = None):
		curQry = self.cursor.execute(qry)
		fields = (fld[0] for fld in curQry.description)
		dret = [tuple(fields)]
		
		for row in curQry:
			dret.append(row)

		if toCsvFile: 
			fp = open(toCsvFile,'w')
			for ret in dret:
				csvret = []
				for val in ret:
					if isinstance(val, str):
						val = val.replace('"',"'")
						csvret.append((val,'"{}"'.format(val))[',' in val])
					elif isinstance(val, int) or isinstance(val, float):
						csvret.append('"{:,.0f}"'.format(val))
					else:
						csvret.append(val)
				try:
					print(','.join(csvret), file=fp)
				except UnicodeEncodeError:
					print(','.join(csvret).encode(), file=fp)
			fp.close()
		return dret;

#Examples

#-Example Args	
#--WebToon URLs
url1 = 'http://comic.naver.com/ncomment/ncomment.nhn?titleId=666671&no=6&levelName=WEBTOON#' #6회차 
url2 = 'http://comic.naver.com/ncomment/ncomment.nhn?titleId=666671&no=2&levelName=WEBTOON#' #2회차

#--DB Querys
dbName = 'webtooncomments.db'
tblName = 'cmttbl'
saveTo = 'test.csv'
qry1 = 'select * from ' + tblName 
qry2 = 'select * from ' + tblName + ' limit 1,100'

qry_myCmt = 'select * from ' + tblName + ' where writer_nickname="이민서"'
qryusual = 'select writer_id as 아이디,  writer_ip as 아이피, contents as 내용, registered_ymdt as 등록일시, up_count as 조아용, down_count as 시러욧 from ' + tblName

#-Lib Useage
#--GetData for DB

cmt = NaverWebtoonCommentScraper(url1) #args: naver webtoon comments url, 

cmtfld = cmt.GetCommentsTableFields() #for Create DB

cPage = cmt.GetCommentsTotalPageCount()

print('totalPage: ',cPage)

cmtTbl, faultPage = cmt.GetCommentsTable(range(1, cPage+1)) #returns resultTable and fault pages


print('Total Tuples:', len(cmtTbl))
print('faultPages:', faultPage)

#--SetData to DB and using Query
DBObj = SQLite3DB(dbName)


DBObj.SetDBFromTable(cmtfld, cmtTbl, tblName)  #


query = DBObj.GetQueryFromDB(qryusual,saveTo) #Get Qeury Table And Save To CSV File for Excel


os.startfile(saveTo)
