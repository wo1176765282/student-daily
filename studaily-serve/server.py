import pymysql
db = pymysql.connect(host="localhost",
                     user="root",
                     password="wo1176765282",
                     db="lzm",
                     cursorclass=pymysql.cursors.DictCursor,
                     charset="utf8")
cur = db.cursor()