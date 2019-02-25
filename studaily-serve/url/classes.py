from flask import request,Blueprint,make_response,send_from_directory,current_app
from server import db,cur
import pymysql
import json
import time
import os
from werkzeug import secure_filename
import xlrd
classes=Blueprint('classes',__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ,'xlsx'])
basedir = os.path.abspath(os.path.dirname(__file__))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''班级信息下载及上传'''
@classes.route("/download1")
def download1():
    res = make_response(send_from_directory('download','classes.xlsx',as_attachment = True))
    res.headers["content-disposition"]="attachment;filename=classes.xlsx"
    return res

@classes.route("/upload1",methods=['POST'])
def upload1():
    UPLOAD_FOLDER = 'upload/classes/'
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
            book=xlrd.open_workbook('upload/classes/'+newfile)
            sheet = book.sheet_by_index(0)   #定义一个对象
            arr=[]
            for i in range(1,sheet.nrows):
                con = sheet.row_values(i)
                if isinstance(con[0],float):
                    con[0]=int(con[0])
                con[2] = xlrd.xldate_as_datetime(con[2], 0).strftime("%Y-%m-%d %H:%M:%S")
                con[3] = xlrd.xldate_as_datetime(con[3], 0).strftime("%Y-%m-%d %H:%M:%S")
                con[1] = c[con[1]]
                arr.append(con)
            cur.executemany("insert into classes (name,fid,start,end) values (%s,%s,%s,%s)", (arr))
            db.commit()
            return 'ok'
        else:
            return "error"


@classes.route("/addone")
def addone():
    name=request.args.get('name')
    f=request.args.get('f')
    start=request.args.get('start')
    end=request.args.get('end')
    cur.execute("select cid from `cursor` where cname=%s",(f))
    cid=cur.fetchone()['cid']
    cur.execute("insert into classes (name,start,end,fid) values (%s,%s,%s,%s)",(name,start,end,cid))
    db.commit()
    return "ok"

@classes.route("/selectclasses")
def selectclasses():
    cur.execute("select name,start,end from classes")
    result = cur.fetchall()
    for item in result:
        # 把时间对象转化为字符串
        if isinstance(item['start'],object):
            item['start']=item['start'].strftime("%Y-%m-%d")
        if isinstance(item['end'],object):
            item['end']=item['end'].strftime("%Y-%m-%d")
    return json.dumps(result)

@classes.route("/del")
def del1():
    name=request.args.get('name')
    cur.execute("delete from classes where name=%s",(name))
    db.commit()
    return 'ok'