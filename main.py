# -*- coding: utf-8 -*-


from NaverWebtoonCommentScraper import *
from NaverWebtoonImgScraper import *
from SQLite3DB import *



#Examples

#-Example Args	
#--WebToon URLs
url1 = 'http://comic.naver.com/ncomment/ncomment.nhn?titleId=666671&no=1&levelName=WEBTOON#' #1회차 
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



cmt = NaverWebtoonCommentScraper(url1,100) #args: naver webtoon comments url, req Page num, default==15


cmtfld = cmt.GetCommentsTableFields() #for Create DB

cPage = cmt.GetCommentsTotalPageCount()

print('totalPage: ',cPage)

cmtTbl, faultPage = cmt.GetCommentsTable(range(68, 70)) #returns resultTable and fault pages


print('Total Tuples:', len(cmtTbl))
print('faultPages:', faultPage)

#--SetData to DB and using Query
DBObj = SQLite3DB(dbName)


DBObj.SetDBFromTable(cmtfld, cmtTbl, tblName)  #


query = DBObj.GetQueryFromDB(qryusual,saveTo) #Get Qeury Table And Save To CSV File for Excel


os.startfile(saveTo)
