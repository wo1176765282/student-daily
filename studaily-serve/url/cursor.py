from flask import request,Blueprint,make_response,send_from_directory,current_app
from server import db,cur
import json
import time
import os
from werkzeug import secure_filename
import xlrd
selectcursor1=Blueprint('selectcursor1',__name__)

#定义获得文件格式
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ,'xlsx'])

basedir = os.path.abspath(os.path.dirname(__file__))
# 定义一个函数来判断文件名后缀，确保用户上传文件的文件名是安全的
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''课程下载及上传'''
@selectcursor1.route("/download")
def download():
    res = make_response(send_from_directory('download','cursor.xlsx',as_attachment = True))
    res.headers["content-disposition"]="attachment;filename=cursor.xlsx"
    return res

@selectcursor1.route("/upload",methods=['POST'])
def upload():
    # 定义文件存储路径
    UPLOAD_FOLDER = 'upload/cursor/'
    # 配置上传的文件所储存的位置
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            fname = secure_filename(f.filename)
            suf = fname.rsplit('.', 1)[1]     #截取文件后缀名
            now = int(time.time())
            newfile = str(now)+'.'+suf
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],newfile))
            book=xlrd.open_workbook('upload/cursor/'+newfile)  #文件名以及路径，如果路径或者文件名有中文给前面加一个r拜师原生字符。
            #print(book.sheets())  #读取所有的表    是一个对象
            sheet = book.sheet_by_index(0)   #定义一个对象
            for i in range(1,sheet.nrows):
                con = sheet.row_values(i)
                filedata(con)
            return 'ok'
        else:
            return "error"

@selectcursor1.route("/addonecursor")
def addonecursor():
    data = request.args.get('data')
    data=json.loads(data)
    filedata(data)
    return "ok"

def filedata(con):
    cur.execute("insert into `cursor` (cname) values (%s)", (con[0]))
    cid = db.insert_id()
    step = con[1].split("\n")
    part = con[2].split("\n")
    for index in range(len(step)):
        arr = []
        arr.append((step[index], part[index], cid))
        cur.executemany("insert into `dircursor` (step,part,cid) values (%s,%s,%s)", (arr))
        db.commit()

@selectcursor1.route('/selectcursor')
def selectcursor():
    cur.execute("select * from `cursor`")
    result = cur.fetchall()
    return json.dumps(result)

@selectcursor1.route('/selectonecursor')
def selectonecursor():
    cid = request.args.get('cid')
    cname = request.args.get('cname')
    cur.execute("select GROUP_CONCAT(step) from `cursor` inner join dircursor where `cursor`.cid=%s and dircursor.cid=%s group by cname",(cid,cid))
    step = cur.fetchone()['GROUP_CONCAT(step)']
    step = step.split(",")
    cur.execute("select part from `cursor` inner join dircursor where `cursor`.cid=%s and dircursor.cid=%s",(cid, cid))
    part = cur.fetchall()
    result = []
    for i in range(len(step)):
        obj={'cname':cname}
        obj['step']=step[i]
        obj['part'] = part[i]['part']
        result.append(obj)
    # result[0]['cname']=cname
    return json.dumps(result)

@selectcursor1.route('/del')
def del1():
    data=json.loads(request.args.get('datas'))
    cid=request.args.get('cid')
    print(data)
    cur.execute("delete from dircursor where cid=%s and step=%s",(cid,data['step']))
    db.commit()
    return 'ok'

@selectcursor1.route('/editonecursor')
def editonecursor():
    data = request.args.get('data')
    data = json.loads(data)
    print(data)
    cid=request.args.get('id')
    cur.execute("update `cursor` set cname=%s where cid=%s",(data[0],cid))
    cur.execute("delete from dircursor  where cid=%s", ( cid))
    step = data[1].split("\n")
    part = data[2].split("\n")
    for index in range(len(step)):
        arr = []
        arr.append((step[index], part[index], cid))
        cur.executemany("insert into `dircursor` (step,part,cid) values (%s,%s,%s)", (arr))
    db.commit()
    return 'ok'
