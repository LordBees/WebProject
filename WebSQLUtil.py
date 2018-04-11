##sql utilities
import mysql.connector
##SERVER INFO
#############
host           = "localhost"
db             = "gt"
user           = "root"
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

#universal qry function       
def internal_SQLexec(md,qry,args = ('',),noargs = True):
        ##connection
        conn = getConnection()
        cursor = conn.cursor()

        ##argument
        if (noargs):
                cursor.execute(qry)
        else:
                cursor.execute(qry,args)
                
        ##what to return
        if  (md == 'fetchone'):
                result = cursor.fetchone()
        elif(md == 'fetchall'):
                result = cursor.fetchall()
        elif(md == 'noreturn'):
                result = [('NORETRIEVE',)]
        conn.close()

        #return it
        return result

def executeSQLFetchOne_args(qry,args):
        return internal_SQLexec('fetchone',qry,args,noargs = False)
def executeSQLFetchOne_noargs(qry):
        return internal_SQLexec('fetchone',qry,args)

def executeSQLFetchAll_args(qry,args):
        return internal_SQLexec('fetchall',qry,args,noargs = False)
def executeSQLFetchAll_noargs(qry):
        return internal_SQLexec('fetchall',qry,args)

def executeSQL_args(qry,args):
        return internal_SQLexec('noreturn',qry,args,noargs = False)
def executeSQL_noargs(qry):
        return internal_SQLexec('noreturn',qry,args)
