from flask import request,Blueprint,session
from server import db,cur
import json
import random
import time
startExam=Blueprint('startExam',__name__)
@startExam.route('/sel')
def sel():
    fid = session.get('fid') or 32
    allquestion=[]
    seleone=[]
    selemore=[]
    judge=[]
    getquestion(fid,"单选题",seleone)
    getquestion(fid,"多选题",selemore)
    getquestion(fid,"判断题",judge)
    allquestion=tuple(seleone+selemore+judge)
    cur.execute("select * from question where id in"+str(allquestion))
    result=cur.fetchall()
    return json.dumps(result)

# 获取题目id
def getquestion(fid,name,question):
    cur.execute("select * from questiontype where name=%s",(name))
    onenid = cur.fetchone()['nid']
    cur.execute("select id from question where fid=%s and nid=%s", (fid, onenid))
    oneid = cur.fetchall()
    onearr = []
    for i in oneid:
        onearr.append(i['id'])
    arr = []
    while len(question) < 4:
        i = random.randint(0, len(onearr) - 1)
        if i not in arr:
            arr.append(i)
            question.append(onearr[i])
    return question

@startExam.route('/time1')
def time1():
    fid=session.get('fid') or 32
    cur.execute("select * from exam1 where fid=%s",(str(fid)))
    time=cur.fetchone()['alltime']
    return str(time)

@startExam.route('/addPoint')
def addPoint():
    id=session.get('uid') or 10
    data=request.args.get('data')
    data=json.loads(data)
    myanswer=''
    aid = ''
    for item in data:
        if isinstance(item['myanswer'],list):
            a=''
            for i in item['myanswer']:
                a+=str(i)+'|'
            a=a[:-1]
            item['myanswer']=a
        myanswer+=str(item['myanswer'])+'/n'
        aid+=str(item['id'])+'/n'
    myanswer=myanswer[:-2]
    aid=aid[:-2]
    point=data[len(data)-1]['point']
    nowdate=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    cur.execute("insert into point (stuid,point,myanswer,aid,nowdate) values (%s,%s,%s,%s,%s)",(id,point,myanswer,aid,nowdate))
    db.commit()
    return 'ok'

@startExam.route('/look')
def look():
    id = session.get('uid') or 10
    cur.execute("select * from point where stuid=%s",(id))
    result=cur.fetchall()
    for item in result:
        if isinstance(item['nowdate'], object):
            item['nowdate']=item['nowdate'].strftime("%Y-%m-%d %H:%M")
    return json.dumps(result)

@startExam.route('/relook')
def relook():
    aid=json.loads(request.args.get('aid'))
    cur.execute("select * from question where id in "+str(tuple(aid)))
    result=cur.fetchall()
    return json.dumps(result)

