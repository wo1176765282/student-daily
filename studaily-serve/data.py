from flask import Flask,render_template,request,make_response,redirect,session,send_from_directory,url_for
from server import db,cur
from Code import code
# from flask_session import Session
import pymysql
import hashlib
import json
import random
# import base64


from url.user import user
from url.role import role
from url.cursor import selectcursor1
from url.classes import classes
from url.teacher import teacher
from url.student import student
from url.studaily import studaily

from exam.entry import entry
from exam.questiontype import questiontype
from exam.look import look
from exam.startExam import startExam
from exam.arrange import arrange


app = Flask(__name__,instance_relative_config=True)
app.register_blueprint(user,url_prefix='/ajax/user')
app.register_blueprint(role,url_prefix='/ajax/role')
app.register_blueprint(selectcursor1,url_prefix='/ajax/selectcursor1')
app.register_blueprint(classes,url_prefix='/ajax/classes')
app.register_blueprint(teacher,url_prefix='/ajax/teacher')
app.register_blueprint(student,url_prefix='/ajax/student')
app.register_blueprint(studaily,url_prefix='/ajax/studaily')
app.register_blueprint(entry,url_prefix='/ajax/entry')
app.register_blueprint(questiontype,url_prefix='/ajax/questiontype')
app.register_blueprint(look,url_prefix='/ajax/look')
app.register_blueprint(startExam,url_prefix='/ajax/startExam')
app.register_blueprint(arrange,url_prefix='/ajax/arrange')


app.secret_key = b'123456'

# app.permanent = True   # 默认三十天过期
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hour=2)   # 设置生命周期
# app.config['SESSION_TYPE']='filesystem'
# app.config['SESSION_FILE_DIR']='/home/zry/PycharmProjects/vuetable/venv/aaa'
# Session(app)
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('/error.html'),404
#     return 'error'
#     return redirect('/login')
@app.before_request
def before_request():
    if request.path!="/checkdata" and request.path.find("/static")==-1 and request.path.find("/verification"):
        if session.get("login")!="yes":
            if request.path!="/login":
                return redirect("/login")
@app.route("/")
def index1():
    if session.get("login")=="yes":
        res = make_response(render_template('index.html'))
        return res
    else:
        return redirect("/login")


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registe')
def registe():
    return render_template('registe.html')


# 验证码
@app.route('/verification')
def verification():
    codeobj = code()
    bt=codeobj.output()
    res=make_response(bt)
    session["str1"] = codeobj.str.lower()
    res.headers['Content-type'] = 'image/png'
    return res

# 测试方法！！！
'''
@app.route("/settest")
def settest():
    res = make_response("sdsadsds")
    res.headers['Content-type'] = 'image/png'
    res.headers["accept-ranges"]="bytes"
    res.headers["set-cookie"]="aa=bb"
    session["str1"]="aaa"
    return res
@app.route("/test")
def test():
    print(session.get("str1"))
    return session.get("str1")
'''

# 登陆
@app.route('/checkdata',methods=['POST'])
def checkdata():
    cod = request.form['code'].lower()
    str1 = session.get("str1")
    if cod!=str1:
        return redirect("/login")
    phone = request.form['username']
    upass = request.form['password']
    # sys = request.form['sys']
    md5 = hashlib.md5()
    md5.update(upass.encode())
    upass = md5.hexdigest()
    print(uname,upass)
    cur.execute("select * from users where uname=%s and upass=%s",(phone,upass))
    result = cur.fetchone()
    print(result)
    if result:
        if result['rid']==1:
            cur.execute("select classid from studentes where phone=%s",(phone))
            classid=cur.fetchone()['classid']
            cur.execute("select * from classes where id=%s", (classid))
            data = cur.fetchone()
            classname=data['name']
            fid = data['fid']
        elif result['rid']==2:
            cur.execute("select class from teacher where phone=%s",(phone))
            classname=cur.fetchone()['class']
            cur.execute("select * from classes where name=%s", (classname))
            data = cur.fetchone()
            classid = data['id']
            fid = data['fid']
        else:
            classname=''
            classid=''
            fid=''
        if result:
            session['fid'] = fid
            session['class'] = classname
            session['classid'] = classid
            session['rid']=result['rid']
            session['uid'] = result['uid']
            session['login'] = "yes"
            session['name'] = result['name']
            # if sys=='0':
            return redirect('/')
            # else:
            #     return redirect('/exam')
    return redirect('/login')

# 查看左侧栏菜单
@app.route("/ajax/uname")
def uname():
    if session.get("login") == "yes":
        uname=session.get("name")
        return uname
    else:
        return ""
# 退出
@app.route("/ajax/logout")
def logout():
    session.pop('login',None)
    session.pop('class', None)
    session.pop('classid', None)
    session.pop('rid', None)
    session.pop('name', None)
    session.pop('uid', None)
    return redirect('/login')

@app.route("/ajax/selectroot")
def selectroot():
    cur.execute("select * from role")
    result = cur.fetchall()
    return json.dumps(result)

@app.route("/ajax/menu")
def menu():
    rid = session.get("rid")
    cur.execute("select power from role where rid=%s",(rid))
    if int(rid)>1:
        rid=0
        print(rid)
    result = cur.fetchone()['power']+'|'+str(rid)
    # result="1|2|3|4|5|6|7|8|0"
    return result

'''
@app.route("/daily")
def daily():
    role=1
    if role==1:
        category=request.args.get('category')
        classes=request.args.get('classes')
        time=request.args.get('time')
        categorycon=""
        timecon="and date_format(logs.time,'%Y-%m-%d')='"+time+"'" if time else ""
        if category:
            categorycon="and logs,phone in (select phone from stu where classid in (select id from classes where fid in ("+category+")))"
        if classes and not category:
            categorycon="and logs.phone in (select phone from stu where classid="+classes+")"
            sql="select logs.*,stu.name as sname.classes,name as XXX from logs left join stu on logs left join stu on logs.phone=stu.phone left join classes on stu.classid=class.id where 1=1"
            categorycon+" "+timecon


def pages(total,pageNum):
    if request.url.find("?")<0:
        url=request.url+"?page="
    else:
        url=request.url[0:request.url.rfind("=")+1]
    pageNums=math.ceil(total/pageNum)
    currentpage=int(request.args.get("page") or 0)
    pagestr=""
    pagestr+="共%s页"%(pageNums)
    pagestr+="<a href='%s'>首页</a>"%(url+"0")
    last=currentpage-1 if currentpage-1>0 else 0
    pagestr+="<a href='%s'>上一页</a>"%(url+str(last))
    start=currentpage-2 if currentpage-2>0 else 0
    end=start+4 if start+4<pageNum else pageNum-1
    for item in range(start,end+1):
        if currentpage==item:
            pagestr += "<a href='%s' style='color=red'>%s</a>" % (url + str(item)), item + 1
        else:
            pagestr += "<a href='%s'>%s</a>" % (url + str(item)),item+1

    next=currentpage+1 if currentpage+1<pageNums else pageNums-1
    pagestr += "<a href='%s'>下一页</a>" % (url+str(next))
    pagestr += "<a href='%s'>尾页</a>" % (url +str(pageNums -1))
    limit="limit"+str(currentpage*pageNum)+","+str(pageNum)
    return {'pagestr':pagestr,'limit':limit}
'''
if __name__ == '__main__':
    app.run()


