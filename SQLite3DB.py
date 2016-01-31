# -*- coding: utf-8 -*-
import os, csv
import sqlite3


class SQLite3DB:
	def __init__(self, dbName):
		self.db = sqlite3.connect(dbName)
		self.cursor = self.db.cursor()
		self.dbName = dbName

	def SetDBFromDicTable(self, list_dictbl, tblName):
		fields = tuple(list_dictbl[0][0].keys())
		self.cursor.execute('drop table if exists ' + tblName)
		self.cursor.execute('create table ' + tblName + repr(fields))	
		insList = []
		for cmtList in list_dictbl:
			for dic in cmtList:
				if len(dic) < len(fields):
					missingAttrbs = set(fields) - set(dic.keys())
					for attr in missingAttrbs:
						dic[attr] = 'Undefined'
				insList.append(tuple(dic.values()))
		self.cursor.executemany('insert into ' + tblName + ' values(' + ('?,'*len(fields))[:-1] + ')', insList)
		self.db.commit()
		print(self.cursor.rowcount)

	def GetQueryFromDB(self, qry, toCsvFile = None):
		curQry = self.cursor.execute(qry)
		fields = [fld[0] for fld in curQry.description]
		dret = [tuple(fields)] + list(curQry)
		
		if toCsvFile:
			with open(toCsvFile,'w',newline='') as fp:
				csvWriter = csv.writer(fp)
				for row in dret:
					try:
						csvWriter.writerow(row)
					except:
						print(row[0])
						with open(toCsvFile, 'a', encoding='utf-8', newline = '') as tmp:
							tmpWriter = csv.writer(tmp)
							tmpWriter.writerow(row)
		return dret;


#Lib Useage
'''

con ='■◎♬◑≠◑±◑♪¥♬◑'
#con = 'abcd'		

db = SQLite3DB('test.db')
TBL_NAME = 'test'
TEST_QRY = 'SELECT * FROM ' +TBL_NAME


table =\
 [[
 {'id':'ez05****','ip':'49.143.xxx.206','contents': con,'regtime':'2016-01-31T17:54:28.0+0900' , 'impresive':0,'awesome':0},
 {'id':'ez34****','ip':'49.143.xxx.212','contents': con,'regtime':'2016-01-31T17:54:28.0+0900' , 'impresive':0,'awesome':0},
 {'id':'ez34****','ip':'49.143.xxx.212','contents': con,'regtime':'2016-01-31T17:54:28.0+0900' , 'impresive':0,'awesome':0},
 {'id':'ez34****','ip':'49.143.xxx.212','contents': con,'regtime':'2016-01-31T17:54:28.0+0900' , 'impresive':0,'awesome':0},
 {'id':'ez34****','ip':'49.143.xxx.212','contents': con,'regtime':'2016-01-31T17:54:28.0+0900' , 'impresive':0,'awesome':0}
 ]]


db.SetDBFromDicTable(table, TBL_NAME)

db.GetQueryFromDB(TEST_QRY, 'testqry.csv')

os.startfile('testqry.csv')
'''
