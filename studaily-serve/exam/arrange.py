from flask import request,Blueprint
from server import db,cur
import json


arrange=Blueprint('arrange',__name__)
@arrange.route('/addarrange')
def addarrange():
    cid=request.args.get('cid')
    alltime=request.args.get('alltime')
    cur.execute("insert into exam1 (fid,alltime) values (%s,%s)",(cid,alltime))
    db.commit()
    return 'ok'

@arrange.route('/sele')
def sele():
    cur.execute('select * from exam1,`cursor` where exam1.fid=`cursor`.cid')
    result=cur.fetchall()
    print(result)
    return json.dumps(result)