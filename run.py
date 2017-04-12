#!/usr/bin/python
import sqlite3
import hashlib
import sys
import time
from datetime import datetime

def unixstamp2strtime(unixstamp)
'''
    convert unixstamp to time for string
'''
    return datetime.fromtimestamp(unixstamp).strftime('%Y-%m-%d %H:%M:%S')


def md5str(origin_str)
'''
    convert string to md5 digest
'''
    return str(hashlib.md5(origin_str).hexdigest())

def controller(db_name)
conn = sqlite3.connect(db_name)
chatlist = conn.execute("select * from sqlite_sequence")
print "totally "+len(chatlist) "session"

#get chat session done

#conn.execute("")
#for row in cursor:
#	row[0]
#	conn.close
conn.close()

def printhelp()
    print "usage: "+sys.argv[0]+" db_name"

if len(sys.argc) == 2 :
        controller(sys.argv[1]);
else
    printhelp();
