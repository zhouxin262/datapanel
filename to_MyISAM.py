import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '', 'datapanel')
cur = con.cursor()
sql = "show tables"
cur.execute(sql)
t = cur.fetchone()[0]
msql = ""
while t:
    try:
        #print t
        msql += "ALTER TABLE " + t  + " ENGINE=MyISAM;\n"
        t = cur.fetchone()[0]
    except:
        break

print msql
cur.execute(msql)
