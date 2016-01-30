# -*- coding: utf-8 -*-
import os, csv
import sqlite3


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

		


