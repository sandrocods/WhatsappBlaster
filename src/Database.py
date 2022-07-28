##
# Author  : Sandroputraa
# Name    : Database Helper - WhatsApp Blaster
# Build   : 28-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

import sqlite3


class Database:
    def __init__(self, db):
        try:
            self.db = db
            self.conn = sqlite3.connect(db, check_same_thread=False)
            self.c = self.conn.cursor()
            print("Database connected ✅ ...")
        except sqlite3.Error as e:
            print(e)

    def check_connection(self):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.c = self.conn.cursor()
            print("Database connected ✅ ...")
        except sqlite3.Error as e:
            print(e)

    def insert(self, table, fields, values):
        try:
            self.c.execute("INSERT INTO " + table + " (" + fields + ") VALUES (" + values + ")")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def update(self, table, fields, values, where):
        try:
            self.c.execute("UPDATE " + table + " SET " + fields + " = " + values + " WHERE name_schedule ='" + where + "'")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)