from flask import request,Blueprint,session
from server import db,cur
import pymysql
import json
import time

studaily=Blueprint('studaily',__name__)

@studaily.route('/user')
def user():
    name=session.get('name')
    classname=session.get('class')
    nowday=time.strftime("%Y-%m-%d",time.gmtime())
    result={'name':name,'class':classname,'nowday':nowday}
    return json.dumps(result)

@studaily.route('/con')
def con():
    name=session.get('name')
    classname=session.get('class')
    nowday=request.args.get('date')
    result={'name':name,'class':classname,'nowday':nowday}
    return json.dumps(result)

@studaily.route('/addstudaily')
def addstudaily():
    uid=session.get('uid')
    # classid=session.get('classid')
    cur.execute("select phone from users where uid=%s",(uid))
    phone=cur.fetchone()['phone']
    name = session.get('name')
    motto = request.args.get('motto')
    con = request.args.get('con')
    heart = request.args.get('heart')
    suggest = request.args.get('suggest')
    date = request.args.get('date')
    cur.execute("insert into studaily (uid,name,motto,con,heart,suggest,date,phone) values (%s,%s,%s,%s,%s,%s,%s,%s)",(uid,name,motto,con,heart,suggest,date,phone))
    db.commit()
    return 'ok'

@studaily.route('/selectdaily')
def selectdaily():
    rid=session.get('rid')
    uid = session.get('uid')
    if rid=='1':
        cur.execute("select name,date from studaily where uid=%s",(uid))
        result = cur.fetchall()
        for item in result:
            # 把时间对象转化为字符串
            if isinstance(item['date'],object):
                item['date']=item['date'].strftime("%Y-%m-%d")
        return json.dumps(result)
    elif rid=='2':
        cur.execute("select phone from users where uid=%s",(uid))
        phone=cur.fetchone()['phone']
        cur.execute("select class from teacher where phone=%s",(phone))
        classname=cur.fetchone()['class']
        cur.execute("select id from classes where name=%s", (classname))
        id = cur.fetchone()['id']
        db1 = pymysql.connect(host="localhost",
                              user="root",
                              password="wo1176765282",
                              db="lzm",
                              charset="utf8")
        cur1 = db1.cursor()
        cur1.execute('select phone from studentes where calssid=%s',(id))
        allphone=cur1.fetchall()
        print(allphone)
        cur1.executemany('select uid from users where phone=%s',(allphone))
        alluid=cur1.fetchall()
        db1.close()
        cur.executemany('select * from studaily where uid=%s',(alluid))
        result=cur.fetchall()
        for item in result:
            if isinstance(item['date'], object):
                item['date'] = item['date'].strftime("%Y-%m-%d")
        return json.dumps(result)
    else:
        cur.execute("select * from studaily")
        result = cur.fetchall()
        for item in result:
            # 把时间对象转化为字符串
            if isinstance(item['date'], object):
                item['date'] = item['date'].strftime("%Y-%m-%d")
        return json.dumps(result)

@studaily.route('/studailycon')
def studailycon():
    date=request.args.get('date')
    cur.execute("select con,heart,suggest,motto from studaily where date=%s",(date))
    result = cur.fetchall()
    return json.dumps(result)