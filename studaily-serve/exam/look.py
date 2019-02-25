from flask import request,Blueprint
from server import db,cur
import json


look=Blueprint('look',__name__)
@look.route('/sele')
def sele():
    cur.execute("select * from question,`cursor`,questiontype where question.fid=`cursor`.cid and question.nid=questiontype.nid limit 0,10")
    result=cur.fetchall()
    return json.dumps(result)

@look.route('/total')
def total():
    cur.execute("select count(*) from question")
    result = cur.fetchone()['count(*)']
    return str(result)

@look.route('/page')
def page():
    page=request.args.get('page')
    cur.execute("select * from question,`cursor`,questiontype where question.fid=`cursor`.cid and question.nid=questiontype.nid limit %s,10",((int(page)-1)*10))
    result = cur.fetchall()
    return json.dumps(result)