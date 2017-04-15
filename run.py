#!/usr/bin/python
# encoding: utf-8

import sqlite3
import hashlib
import sys
import time
from datetime import datetime

def read_file(fn):
    '''read file '''
    fp=open(fn,"r")
    h=fp.read()
    fp.close
    return h

def write_file(fn,content):
    '''read file '''
    fp=open(fn,"wb")
    h=fp.write(content)
    fp.close
    return h

def unixstamp2strtime(unixstamp):
    '''
        convert unixstamp to time for string

    '''
    return datetime.fromtimestamp(unixstamp).strftime('%Y-%m-%d %H:%M:%S')


def md5str(origin_str):
    '''
        convert string to md5 digest
    '''
    return str(hashlib.md5(origin_str).hexdigest())


def countlen(cursor):
    i=0
    for row in cursor
        i=i+1
    return i

def resolve_message(content_type,content_type):
    '''
        todo:
    '''
    result=content
    return result


def build_session(file_buf,username,time,content_type,content,des):
    '''
        build one piece of message to text
        format 1:   time -- me -- \n message
        format 2:   username -- time  \n message
    '''
    user =username #single chat session

    if des :
        #format 2
        file_buf = file_buf + user + unixstamp2strtime(time) + "\n"
    else :
        #format 1
        file_buf = file_buf + unixstamp2strtime(time) + "我：" + "\n"

    #resolve it
    file_buf = file_buf + resolve_message(content_type,content) + "\n"

    file_buf = file_buf+"\n"
    return

def output_data(db_handle,username):
    '''
    TODO:
    '''
    chat_db="Chat_"+md5str(username)
    sql="select CreateTime,Type,Message,Des from "+chat_db+" order by MesLocalID "

    chat_log = db_handle.execute(sql)

    #prepare head of session
    content="Total :"+str(countlen(chat_log)) + "messages"+ "\n\n"

    for row in chat_log
        build_session(content,username,row[0],row[1],row[2],row[3])

    write_file(username,content)
    return

def controller(db_handle):
    #count chat list
    chatlistcount = db_handle.execute("select name from sqlite_sequence where name like \"Chat_%\"")
    print "Total: "+str(countlen(chatlistcount))+" sessions"

    #get chat list from table(Session list )
    cur = db_handle.execute("select username from friend_meta order by lastUpdate desc")

    #excute read data (from db) and write file (text)
    for username in cur
        output(db_handle,username[0])

    return

def printhelp():
    print "usage: "+sys.argv[0]+" db_file_name [table_name]"
    return

#main function
if len(sys.argv) >1 :
    conn=sqlite3.connect(sys.argv[1])
    controller(conn)
    conn.close()

else:
    printhelp();
