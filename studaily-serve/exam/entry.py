from flask import request,Blueprint,make_response,send_from_directory,current_app
from server import db,cur
import time
import os
from werkzeug import secure_filename
import xlrd
entry=Blueprint('entry',__name__)
@entry.route('/addjudge')
def addjudge():
    con=request.args.get('con')
    answer=request.args.get('answer')
    nid = 3
    point = request.args.get('point') or 3
    cname = request.args.get('cname')
    cur.execute("select cid from `cursor` where cname=%s", (cname))
    fid = cur.fetchone()['cid']
    cur.execute("insert into question (fid,con,answer,point,nid) values (%s,%s,%s,%s,%s)",(fid, con, answer, point, nid))
    db.commit()
    return 'ok'

@entry.route('/addchoice')
def addchoice():
    con = request.args.get('con')
    answer = request.args.get('answer')
    option = request.args.get('option')
    nid=1
    point=request.args.get('point') or 5
    cname=request.args.get('cname')
    cur.execute("select cid from `cursor` where cname=%s",(cname))
    fid=cur.fetchone()['cid']
    cur.execute("insert into question (fid,con,answer,`option`,point,nid) values (%s,%s,%s,%s,%s,%s)", (fid,con, answer,option,point,nid))
    db.commit()
    return 'ok'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ,'xlsx'])
basedir = os.path.abspath(os.path.dirname(__file__))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@entry.route("/download")
def download():
    res = make_response(send_from_directory('download','exam.xlsx',as_attachment = True))
    res.headers["content-disposition"]="attachment;filename=exam.xlsx"
    return res


@entry.route("/upload",methods=['POST'])
def upload():
    UPLOAD_FOLDER = 'upload/exam/'
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
        if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            fname = secure_filename(f.filename)
            suf = fname.rsplit('.', 1)[1]     #截取文件后缀名
            now = int(time.time())
            newfile = str(now)+'.'+suf
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],newfile))
            book=xlrd.open_workbook('upload/exam/'+newfile)
            sheet = book.sheet_by_index(0)   #定义一个对象
            question=[]
            for i in range(1,sheet.nrows):
                arr=[]
                con = sheet.row_values(i)
                cur.execute("select cid from `cursor` where cname=%s",(con[0]))
                fid=cur.fetchone()['cid']
                cur.execute("select nid from questiontype where name=%s", (con[1]))
                nid=cur.fetchone()['nid']
                sel=con[3].split('|')
                if nid==1:
                    answer=sel.index(str(int(con[4])))
                elif nid==2:
                    answer=''
                    ans = con[4].split('|')
                    for i in range(len(sel)):
                        for j in range(len(ans)):
                            if sel[i] == ans[j]:
                                a=str(i)+'|'
                                answer+=a
                    answer=answer[0:-1]
                elif nid==3:
                    con[3]=None
                    if con[4]=='错':
                        answer=0
                    elif con[4]=='对':
                        answer=1
                arr+=[fid]+[con[2]]+[con[3]]+[answer]+[int(con[5])]+[nid]
                question.append(tuple(arr))

            cur.executemany("insert into question (fid,con,`option`,answer,point,nid) values (%s,%s,%s,%s,%s,%s)",(question))
            db.commit()
            return 'ok'
        else:
            return "error"
