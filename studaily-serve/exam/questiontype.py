from flask import request,Blueprint,make_response,send_from_directory,current_app
from server import db,cur
import json
questiontype=Blueprint('questiontype',__name__)
@questiontype.route('/sele')
def sele():
    cur.execute("select * from questiontype")
    result=cur.fetchall()
    return json.dumps(result)


@questiontype.route('/add')
def add():
    # nid=request.args.get('nid')
    name = request.args.get('name')
    cur.execute("insert into questiontype (name) values (%s)",(name))
    db.commit()
    cur.execute("select * from questiontype")
    result = cur.fetchall()
    return json.dumps(result)

@questiontype.route('/edit')
def edit():
    id = request.args.get('id')
    nid=request.args.get('nid')
    name = request.args.get('name')
    print(id,nid,name)
    cur.execute("update questiontype set nid=%s,name=%s where id=%s",(nid,name,id))
    db.commit()
    cur.execute("select * from questiontype")
    result = cur.fetchall()
    return json.dumps(result)

@questiontype.route('/del')
def dele():
    id = request.args.get('id')
    cur.execute("delete from questiontype where id=%s",(id))
    db.commit()
    cur.execute("select * from questiontype")
    result = cur.fetchall()
    return json.dumps(result)