from flask import request,Blueprint
from server import db,cur
import json
import hashlib
user=Blueprint('user',__name__)


# 添加用户
@user.route('/add',methods=['POST'])
def add():
    name = request.form['name']
    upass = request.form['pass']
    phone = request.form['phone']
    rid = request.form['rid']
    md5 = hashlib.md5()
    md5.update(upass.encode())
    upass = md5.hexdigest()
    cur.execute("insert into users(name,uname,upass,phone,rid)values (%s,%s,%s,%s,%s)", (name, phone, upass, phone,rid))
    db.commit()
    return 'ok'


# 查询所有用户
@user.route("/searchuser")
def searchuser():
    cur.execute("select * from users,role where users.rid=role.rid")
    result = cur.fetchall()
    return json.dumps(result)

@user.route("/del")
def del1():
    id=request.args.get("id")
    cur.execute("delete from users where uid=%s",(id))
    db.commit()
    cur.execute("select * from users,role where users.rid=role.rid")
    data = cur.fetchall()
    return json.dumps(data)