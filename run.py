#!/usr/bin/python
import sqlite3
import hashlib
import sys
import time
from datetime import datetime

def unixstamp2strtime(unixstamp):
    '''
        convert unixstamp to time for string

    '''
    strtime=datetime.fromtimestamp(unixstamp).strftime('%Y-%m-%d %H:%M:%S')
    return strtime

def md5str(origin_str):
    '''
        convert string to md5 digest
    '''
    return str(hashlib.md5(origin_str).hexdigest())

def controller(db_name):
    conn = sqlite3.connect(db_name)
    chatlist = conn.execute("select * from sqlite_sequence")
    #print "totally "+len(chatlist)+" sessions"

#get chat session done

#conn.execute("")
    i=0
    for row in chatlist:
        #print str(i)+":"+row[0]
        i=i+1
#	conn.close
    print str(i)
    conn.close()

def printhelp():
    print "usage: "+sys.argv[0]+" db_name"

if len(sys.argv) == 2 :
        controller(sys.argv[1]);
else:
    printhelp();
