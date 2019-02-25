from flask import request,Blueprint
from server import db,cur
import json
role=Blueprint('role',__name__)
@role.route("/selectitems")
def selectitems():
    rid = request.cookies.get("rid")
    cur.execute("select power from role where rid=%s",(rid))
    result = cur.fetchone()['power']
    return 'ok'

@role.route("/addrole")
def addrole():
    rname = request.args.get("rname")
    power = request.args.get("power")
    cur.execute("insert into role (rname,power)values (%s,%s)",(rname,power))
    db.commit()
    return "ok"

@role.route("/delroot")
def delroot():
    rid = request.args.get("rid")
    cur.execute("delete from role where rid=%s",(rid))
    db.commit()
    cur.execute("select * from role")
    result = cur.fetchall()
    return json.dumps(result)


@role.route("/editrole")
def editrole():
    rid=request.args.get("rid")
    cur.execute("select power from role where rid=%s",(rid))
    result = cur.fetchone()['power']
    return result

@role.route("/updaterole")
def updaterole():
    rid = request.args.get("rid")
    rname = request.args.get("rname")
    power = request.args.get("power")
    cur.execute("update role set rname=%s,power=%s where rid=%s",(rname,power,rid))
    db.commit()
    return "ok"