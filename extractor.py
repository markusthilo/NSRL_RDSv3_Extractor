#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Markus Thilo'
__version__ = '0.0.1_2023-04-20'
__license__ = 'GPL-3'
__email__ = 'markus.thilo@gmail.com'
__status__ = 'Testing'
__description__ = 'Little helper to get hashes for X-Ways'

from sqlite3 import connect as SqliteConnect
from tkinter import Tk, StringVar, PhotoImage
from tkinter.ttk import Frame, LabelFrame, Entry, Button
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo
from sys import argv
from argparse import ArgumentParser, FileType

class RDS:
	'Read RDSv3'

	def __init__(self, f):
		'Open database'
		self.db = SqliteConnect(f)
		self.cursor = self.db.cursor()

	def fetchall(self, table, field):
		'Generator to fetch all data from one field of one table'
		self.cursor.execute(f'SELECT "{field}" FROM "{table}";')
		for row in self.cursor.fetchall():
			yield row[0]

	def close(self):
		'Close database'
		self.db.close()

class Worker:
	'Main class'

	def __init__(self, dbfile, outfile, table='FILE', field='md5'):
		'Work'
		db = RDS(dbfile)
		print(field.upper(), file=outfile)
		for line in db.fetchall(table, field):
			print(line, file=outfile)
		outfile.close()
		db.close()

class GUI(Tk):
	'Graphical User Interface'

	def __init__(self, icon_base64):
		'Define the app window'
		super().__init__()
		self.title(f'NSRL_RDSv3_Extractor v{__version__}')
		self.resizable(0, 0)
		self.iconphoto(False, PhotoImage(data = icon_base64))
		frame = Frame(self)
		frame.pack(padx=10, pady=10, fill='both', expand=True)
		self.table_str = StringVar(value='FILE')
		label_frame = LabelFrame(frame, text='TABLE')
		label_frame.pack(padx=10, pady=10, fill='both', expand=True)
		Entry(label_frame, textvariable=self.table_str, width=60).pack(padx=10, pady=10)
		self.field_str = StringVar(value='md5')
		label_frame = LabelFrame(frame, text='FIELD')
		label_frame.pack(padx=10, pady=10, fill='both', expand=True)
		Entry(label_frame, textvariable=self.field_str, width=60).pack(padx=10, pady=10)
		frame = Frame(self)
		frame.pack(padx=10, pady=10, fill='both', expand=True)
		Button(frame, text='Start/Select DB', command=self.start).pack(padx=10, pady=10, side='left')
		Button(frame, text='Quit', command=self.destroy).pack(padx=10, pady=10, side='right')

	def start(self):
		'Get destination'
		db = askopenfilename(
			title				=	'Select SQLite database file to read',
			filetypes			=	(('SQLite', '*.db'), ('All files', '*.*'))
		)
		if db == '':
			self.nothing_to_do()
			return
		out = asksaveasfile(
			title				=	'File to write list/field values',
			filetypes			=	(('Text', '*.txt'), ('All files', '*.*')),
			defaultextension	=	'.txt'
		)
		if not out:
			self.nothing_to_do()
			return
		Worker(db, out, table=self.table_str.get(), field=self.field_str.get())
		showinfo(
			title				=	'NSRL_RDSv3_Extractor',
			message				=	'All done'
		)

	def nothing_to_do(self):
		'Show message'
		showinfo(
			title				=	'NSRL_RDSv3_Extractor',
			message				=	'Nothing to do'
		)

if __name__ == '__main__':	# start here if called as application
	if len(argv) > 1:	# handle cmd line when called with arguments
		argparser = ArgumentParser(description=__description__)
		argparser.add_argument('-o', '--out', type=FileType('w'), required=True,
			help='Output file to write hash list', metavar='FILE'
		)
		argparser.add_argument('-t', '--table', type=str, default='FILE',
			help='Table of database to read (default: FILE)', metavar='STRING'
		)
		argparser.add_argument('-f', '--field', type=str, default='md5',
			help='Field of database to read (default: md5)', metavar='STRING'
		)
		argparser.add_argument('db', nargs=1, type=str,
			help='Database/SQLite file to read', metavar='FILE'
		)
		args = argparser.parse_args()
		Worker(args.db[0], args.out, table=args.table, field=args.field)
	else:	# tk gui when no argument is given
		GUI('''
			iVBORw0KGgoAAAANSUhEUgAAADAAAAAwAgMAAAAqbBEUAAAADFBMVEVhYmwAAAAFDWYFDWeT3ml2
AAAAAXRSTlMAQObYZgAAAMpJREFUKM+lkUEKwjAQRaOSlYoeROgFhHbpsosILoRewQN04c3MJcSt
R4gLoYum32QmSQsWVJxFmEfz//xMhfippFiHbopOCsX9CsDVlNTP4AEM+RvccEiwd1UGsB5UNEhf
dOY1jyNpjB+kJgzQ7lDLmgFnkTQYumHo5gGVrfs41fOUXuCgINAMOx7q8thKbgg6Ieb3QrY81JBN
ADTeMgLVCORDyBhMvzeAF6rpnlmEZ5NiGxP45Y8maMPxTYLmQwK+Z+J/v0TFv/UC/Y7U5VSOZTAA
AAAASUVORK5CYII='''
		).mainloop()

