# -*- coding: utf-8 -*-
import os, csv
import sqlite3


class SQLite3DB:
	def __init__(self, dbName):
		self.db = sqlite3.connect(dbName)
		self.cursor = self.db.cursor()
		self.dbName = dbName

	def SetDBFromTable(self, list_table, tblName): #필드 포함 하여 전달
		field, *tup = list_table
		self.cursor.execute('drop table if exists ' + tblName)
		self.cursor.execute('create table ' + tblName + repr(tuple(field)))
		self.cursor.executemany('insert into ' + tblName + ' values(' + ('?,'*len(field))[:-1] + ')', tup)
		self.db.commit()
		return len(tup)	

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
						print('encoding Err at write to CSV',row[0])
						with open(toCsvFile, 'a', encoding='utf-8', newline = '') as tmp:
							tmpWriter = csv.writer(tmp)
							tmpWriter.writerow(row)
		return dret;


#Lib Useage
'''

#con ='■◎♬◑≠◑±◑♪¥♬◑'
con = 'abcd'		

db = SQLite3DB('test.db')
TBL_NAME = 'test'
TEST_QRY = 'SELECT * FROM ' +TBL_NAME


table =\
 [
 ['id','ip','contents','date','good','bad'],
 ['ez05****','49.143.xxx.206',con,'2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212',con,'2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212',con,'2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212',con,'2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212',con,'2016-01-31T17:54:28.0+0900' , 0, 0]
 ]


db.SetDBFromTable(table, TBL_NAME)

db.GetQueryFromDB(TEST_QRY, 'testqry.csv')

os.startfile('testqry.csv')

'''