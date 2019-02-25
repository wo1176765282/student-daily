from flask import request,Blueprint,make_response,send_from_directory,current_app
from server import db,cur
import pymysql
import json
import time
import os
import hashlib
from werkzeug import secure_filename
import xlrd
# import pandas
teacher=Blueprint('teacher',__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ,'xlsx'])
basedir = os.path.abspath(os.path.dirname(__file__))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''班级信息下载及上传'''
@teacher.route("/download1")
def download1():
    res = make_response(send_from_directory('download','teach.xlsx',as_attachment = True))
    res.headers["content-disposition"]="attachment;filename=teach.xlsx"
    return res

@teacher.route("/upload1",methods=['POST'])
def upload1():
    UPLOAD_FOLDER = 'upload/teacher/'
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        db1 = pymysql.connect(host="localhost",
                              user="root",
                              password="wo1176765282",
                              db="lzm",
                              charset="utf8")
        cur1 = db1.cursor()
        cur1.execute("select cname,cid from `cursor`")
        c = dict(cur1.fetchall())
        db1.close()
        f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            fname = secure_filename(f.filename)
            suf = fname.rsplit('.', 1)[1]     #截取文件后缀名
            now = int(time.time())
            newfile = str(now)+'.'+suf
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],newfile))
            book=xlrd.open_workbook('upload/teacher/'+newfile)
            sheet = book.sheet_by_index(0)   #定义一个对象
            arr=[]
            user=[]
            for i in range(1,sheet.nrows):
                con = sheet.row_values(i)
                if isinstance(con[1],float):
                    con[1]=str(int(con[1]))
                if isinstance(con[3],float):
                    con[3]=int(con[3])
                con[2]=c[con[2]]
                arr.append(con)

                name=con[0]
                phone=con[1]
                md5=hashlib.md5()
                md5.update(b'111111')
                up=md5.hexdigest()
                arr1=[name,phone,up,phone,2]
                user.append(arr1)
            cur.executemany("insert into teacher (name,phone,fid,class) values (%s,%s,%s,%s)",(arr))
            cur.executemany("insert into users (name,uname,upass,phone,rid) values (%s,%s,%s,%s,%s)",(user))
            db.commit()
            return 'ok'
        else:
            return "error"


@teacher.route("/addone")
def addone():
    name=request.args.get('name')
    f=request.args.get('f')
    phone=request.args.get('phone')
    classes=request.args.get('classes')
    md5 = hashlib.md5()
    md5.update(b'111111')
    up = md5.hexdigest()
    cur.execute("select cid from `cursor` where cname=%s",(f))
    fid=cur.fetchone()['cid']
    cur.execute("insert into teacher (name,phone,class,fid) values (%s,%s,%s,%s)",(name,phone,classes,fid))
    cur.execute("insert into users (name,uname,upass,phone,rid) values (%s,%s,%s,%s,%s)",(name,phone,up,phone,2))
    db.commit()
    return "ok"

@teacher.route("/selectteacher")
def selectclasses():
    cur.execute("select name,phone,fid,class from teacher")
    result = cur.fetchall()
    db1 = pymysql.connect(host="localhost",
                          user="root",
                          password="wo1176765282",
                          db="lzm",
                          charset="utf8")
    cur1 = db1.cursor()
    cur1.execute("select cid,cname from `cursor`")
    c = dict(cur1.fetchall())
    db1.close()
    print(result)
    print(c)
    for item in result:
        item['fid']=c[item['fid']]
    return json.dumps(result)

@teacher.route("/del")
def del1():
    phone=request.args.get('phone')
    cur.execute("delete from teacher where phone=%s",(phone))
    cur.execute("delete from users where phone=%s", (phone))
    db.commit()
    return 'ok'