##sql utilities
import mysql.connector
##SERVER INFO
#############
host           = "localhost";
db             = "gt";
user           = "root";
passwd         = ""
############

##functions/procs
def getConnection():
        conn = mysql.connector.connect(user=user,password=passwd,host=host,database=db)
        return conn

def executequerywithargs(qry,args):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(qry,args)
        result = cursor.fetchall()
        conn.close()
        return result

def executequerywithoutargs(qry):
        args = ()
        executequerywithargs(qry,args)
