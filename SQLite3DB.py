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
		self.db.commit()
		self.cursor.execute('create table ' + tblName + repr(fields))
		self.db.commit()
		for cmtList in list_dictbl:
			for tup in cmtList:
				insExp = 'insert into ' + tblName + ' values' + repr(tuple(tup.values()))
				try:
					self.cursor.execute(insExp)
				except sqlite3.OperationalError as err:
					missingKeys = set(fields) - set(tup.keys())
					for mskey in missingKeys:
						tup[mskey] = 'NULL'	
					print(len(missingKeys))
					newTup = map(lambda x: x.replace('"',r'\"') if isinstance(x,str) else x , tup.values())
					newTup = map(lambda x: x.replace("'",r"\'") if isinstance(x,str) else x , newTup)
					newTup = map(lambda x: x.encode('utf-8').decode('utf-8','ignore') if isinstance(x,str) else x, newTup)
					insExp = 'insert into ' + tblName + ' values' + repr(tuple(newTup))
					try:
						self.cursor.execute(insExp)
					except:
						print(insExp.encode())
		self.db.commit()
				

	def GetQueryFromDB(self, qry, toCsvFile = None):
		curQry = self.cursor.execute(qry)
		fields = (fld[0] for fld in curQry.description)
		dret = [tuple(fields)] + list(curQry)
		
		if toCsvFile:
			with open(toCsvFile,'w',newline='') as fp:
				csvWriter = csv.writer(fp)
				for row in dret:
					try:
						csvWriter.writerow(row)
					except:
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
