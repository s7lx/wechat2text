#!/usr/bin/python
# encoding: utf-8

import sqlite3
import hashlib
import sys
import time
import io
import re
from datetime import datetime

def read_file(fn):
    '''read file '''
    fp=open(fn,"r")
    h=fp.read()
    fp.close
    return h

def write_file(fn,content):
    '''read file '''
    fp=io.open(fn,"w")
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


def countlen(db_handle,sql):
    sql_local="select count(*) from "+sql
    cur_count=db_handle.execute(sql_local)
    count=0
    for row in cur_count:
        count=row[0]
    return count

def message_location(content):
    '''
    resolve location message
    '''
    re_str_x="<location.*? x=\"(.*?)\" "
    x=re.compile(re_str_x,re.DOTALL).findall(content)

    re_str_y="<location.*? y=\"(.*?)\" "
    y=re.compile(re_str_y,re.DOTALL).findall(content)

    re_str_poi="<location.*? label=\"(.*?)\" "
    poi=re.compile(re_str_poi,re.DOTALL).findall(content)

    #http://www.google.cn/maps/@35.2135204,104.0196158,15z
    ret_str=poi[0]+u"(http://www.google.com/maps/@"+x[0]+u","+y[0]+u",15z)\n"

    return ret_str
    

def resolve_message(content_type,content):
    '''
        resolve content Type

        Type 48: Location
        Type 49: share link
        Type 
    '''
    if content_type== 48 : #type is map
        resultcontent = message_location(content)
    else:
        resultcontent = content
    return resultcontent


def build_session(username,time,content_type,content,des):
    '''
        construct  message 
        format 1:   time -- me -- \n message
        format 2:   username -- time  \n message
    '''
    if username.endswith("@chatroom",0) :
        chatroom_mode=True
    else:
        chatroom_mode=False
    #check chatroom_mode

    if chatroom_mode :
        user= "" #chatroom mode
    else: 
        user =username #single chat mode

    file_buf=""
    if des :
        #format 2
        if chatroom_mode:
            file_buf = file_buf + unixstamp2strtime(time) + "\n"  #chat mode
        else:
            file_buf = file_buf + user + u": " + unixstamp2strtime(time) + "\n" #single mode
    else :
        #format 1
        file_buf = file_buf + unixstamp2strtime(time) + u"  我：" + "\n"

    #resolve it

    file_buf = file_buf + resolve_message(content_type,content) + "\n"

    file_buf = file_buf+"\n"


    return file_buf

def output_data(db_handle,username):
    '''
    TODO: 
    '''
    print "Chat with "+username
    
    chat_db="Chat_"+md5str(username)

    sql="select CreateTime,Type,Message,Des from "+chat_db+" order by CreateTime "
    chat_log = db_handle.execute(sql)

    db_len=countlen(db_handle,chat_db)
    print "Total :"+str(db_len) + " messages"+ "\n\n"

    #prepare head of session

    content="Total :"+str(db_len) + " messages"+ "\n\n"
    
    i=0
    for row in chat_log :
        i=i+1
        content = content + build_session(username,row[0],row[1],row[2],row[3])
        if i %1000 ==0:
            print str(i)+" messages ( Total : "+str(db_len)+")"
    
    write_file(username+".txt",content)

    return

def controller(db_handle,username="ALLCHAT"):
    '''
        main function

    '''
    #count chat list
    chatlistcount = db_handle.execute("select name from sqlite_sequence where name like \"Chat_%\"")

    print "Total: "+str(countlen(db_handle,"sqlite_sequence where name like \"Chat_%\""))+" sessions"

    #get chat list from table(Session list )
    cur = db_handle.execute("select username from friend_meta order by lastUpdate desc")


    #excute read data (from db) and write file (text)
    if username == "ALLCHAT":

        for user in cur :
            output_data(db_handle,user[0])

    else :
        output_data(db_handle,username)

    return

def printhelp():
    print "usage: "+sys.argv[0]+" db_file_name [table_name]"
    return

#entry point function 
if len(sys.argv) >1 :
    conn=sqlite3.connect(sys.argv[1])
    if len(sys.argv) == 3 :
        controller(conn, sys.argv[2])
    else:
        controller(conn)

    conn.close()

else:
    printhelp();
