# -*- coding: utf-8 -*-


from NaverWebtoonCommentScraper import *
from NaverWebtoonImgScraper import *
from SQLite3DB import *

from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

database = 'sqlWebtoonComment.db'
savefile = 'query.csv'

def SaveWebToonToFolder(wtUrl, saveTo):
	wtCut = NaverWebtoonImgScraper(wtUrl)
	cutList = filter(lambda x: x.startswith('http://imgcomic.naver.net/'),wtCut.ExtWebtoonImgList())
	title = wtCut.GetWebtoonTitle()
	wtCut.SaveSrcImgTo(cutList, saveTo+'\\'+title)

def CheckWebToonUrlValid(wtUrl):
	pattern_sub = 'comic\.naver\.com\/webtoon\/detail\.nhn\?titleId=\d+&no=\d+&weekday=\w+'
	pattern_main = 'comic\.naver\.com\/webtoon\/list\.nhn\?titleId=\w+&\weekday=\w'
	if re.search(pattern_main, wtUrl):
		mainPage = urlopen(wtUrl)
		mainHtml = mainPage.read().decode()
		bs = BeautifulSoup(mainHtml,"html.parser")
		subInsts = bs.find_all('a')
		for inst in subInsts:
			href = inst.get('href')
			if re.search('\/webtoon\/detail\.nhn\?titleId=\d+&no=\d+&weekday=\w+', href):
				prs = urlparse(wtUrl)
				return urlunparse((prs.scheme, prs.netloc,href,'','',''))
	elif re.search(pattern_sub, wtUrl):
		return wtUrl
	else:
		return None

def GetChapterRange():
	chapterNums = list(map(int,re.findall('\d+',ent2.get())))
	if len(chapterNums) < 2 : chapterNums.append(1)
	chapterNums.sort()
	return chapterNums[0], chapterNums[-1]+1

def StoreWebToonCommentToDB(cmtUrl, tblName, dbName):
	wtCmt = NaverWebtoonCommentScraper(cmtUrl,100)
	cmtfld = wtCmt.GetCommentsTableFields() #for Create DB
	cPage = wtCmt.GetCommentsTotalPageCount()
	cmtTbl, faultPage = cmt.GetCommentsTable(range(1, cPage+1)) #returns resultTable and fault pages
	DBObj = SQLite3DB(dbName)
	DBObj.SetDBFromTable(cmtfld, cmtTbl, tblName)  #
	return len(cmtTbl) ,faultPage

def GetQueryFromDB(qry ,dbName):
	DBObj = SQLite3DB(dbName)
	DBObj.GetQueryFromDB(qry, savefile) 





def On_Btn1Click():
	webtoonurl = CheckWebToonUrlValid(ent1.get())
	if webtoonurl:
		saveTopath =  filedialog.askdirectory(title = 'SaveTo')
		start, end = GetChapterRange()
		for i, chap in enumerate(range(start, end)):
			chapUrl = re.sub('no=\d+','no={}'.format(chap),webtoonurl)
			SaveWebToonToFolder(chapUrl, saveTopath)
			print('downloading... {}of{}'.format(i+1, end - start))
	else:
		messagebox.showerror('wrong url',webtoonurl)






hWnd = Tk()
hWnd.geometry('500x500+300+400')


Label(text = 'Naver webtoon URL').pack(anchor = 'nw')

ent1 = Entry(hWnd)
ent1.pack(anchor ='nw')

Label(text = 'DownLoad chapter Range(ex:1~9, ~149)').pack(anchor = 'nw')

ent2 = Entry(hWnd)
ent2.pack(anchor ='nw')

btn1 = Button(hWnd, text = 'GetWebtoon',command = On_Btn1Click)
btn1.pack(anchor = 'nw')




hWnd.mainloop()




'''
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
'''