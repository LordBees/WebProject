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



##gets the route status by the primary key from the given table
def getstatusbyID(RouteID,Rawtable):
        qry = 'SELECT Status FROM '+Rawtable+' WHERE ID = %s'
        args = (RouteID,)
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(qry,args)
        result = cursor.fetchone()
        conn.close()
        return result

##sets the status of a route by id in a given table
def setstatusbyID(routeID,rawTable,status):
        ##qry = 'SELECT Status FROM '+Rawtable+' WHERE ID = %s'
        ##args = (routeID,)
        query = "UPDATE "+str(rawTable)+" SET Status = %S WHERE ID = %s"
	args = (status,RouteID)

	##qry
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(qry,args)
        ##result = cursor.fetchone()
        conn.close()
        #query = "UPDATE webferrytt SET DepartureTime = %s, ArrivalTime =%s, FerryNum =%s, Price =%s, Status = %s WHERE Departure =%s AND Arrival =%s AND DepartureTime = %s AND ArrivalTime =%s"
	#args = (newDepartTime,newArriveTime,newVessleNumber,price,status,departLocation, arriveLocation, prevDepartTime+":00", prevArriveTime+":00")
	##cursor.execute(query,args)

	
        ##return result
        
##checks a status for the route with a given id 
def isstatus(routeID,rawTable,status):
        if(status == getStatusById(routeID,rawTable)):
                return True
        return False



