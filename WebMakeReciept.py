##make reciept

##imports

#system/packages
import os,sys
import mysql.connector

#other imports
import WebSQLUtil as Qman


##vars/defs

# queries for reciept
SQLpre = "SELECT * FROM "
SQLpost = " WHERE ID = %s"

# system path to save reciepts into
RecieptPath = "static\\reciepts\\"
RecieptExt =  ".txt"

##debug mode
SCRIPT_DEBUG = True





##functions/procs

####
##desc:
#
##inputs
#
##outputs
#
##misc
#
####

##functions/procs
#gets username by custid
def getUnameByID(CustID):
    SQLq = "SELECT userName FROM userlogin WHERE customerID = %s"
    args = (CustID,)
    return Qman.executequerywithargs(SQLq,args)

#gets pwd by custid
def getPwdByID(CustID):
    SQLq = "SELECT PassWord FROM userlogin WHERE customerID = %s"
    args = (CustID,)
    return Qman.executequerywithargs(SQLq,args)

#writes file array each entry is a new line
def writefilearray(name,data,Table,ext = RecieptExt,fpath=RecieptPath):
    f = open(fpath+Table+"\\"+str(name)+ext,'w')
    for x in data:
        f.write(x+'\n')
    f.close()##add safety to this


#check for folder for each table
def chk_RF_exists(Ttype):##checks+creates folders for transport types
    if(not os.path.isdir(RecieptPath)):
        if(SCRIPT_DEBUG):
            print("making dir for Reciepts")
        os.mkdir(RecieptPath)
        
    if(SCRIPT_DEBUG):
        print("dircheck: "+Ttype)
    if(not os.path.isdir(RecieptPath+Ttype)):
        if(SCRIPT_DEBUG):
            print("making dir:"+Ttype)
        os.mkdir(RecieptPath+Ttype)

        
#check for if reciept exists already as no need to reprint
def RecieptExists(Ttype,rid):##checks whether reciept exists for a given transport type
    ##fsexists
    if(os.path.isfile(RecieptPath+Ttype+"\\"+str(rid)+RecieptExt)):
        return True
    return False


#get the actual table name for the transport mode
def resolve_tname(Tmode):
    #setup
    returner = "invalid choice"
    Tmode = Tmode.lower()

    #what to return
    if  (Tmode == "train"):
        returner = "webtrainbook"
    elif(Tmode == "plane"):
        returner = "webairbook"
    elif(Tmode == "ferry"):
        returner = "webferrybook"
    elif(Tmode == "taxi"):
        returner = "invalidu"
    elif(Tmode == "bus"):
        returner = "invalidu"

    #return it
    return returner


#format reciept for printing to file
def prep_reciept(data):
    #data preparation
    BookID =data[0][0]
    PFname =data[0][1]
    PLname =data[0][2]
    TID    =data[0][3]
    Bags   =data[0][4]
    Cost   =data[0][5]
    CustID =data[0][6]
    Cust_Uname = getUnameByID(CustID)[0][0]
    Cust_Pwd = getPwdByID(CustID)[0][0]
    ##processing of data
    #round(Cost, 2)
    ##Cust_Uname = Cust_Uname[0][0]
    ##Cust_Pwd = Cust_Pwd[0][0]
    
    
    #######reciept formatting####
    data2write = []
    data2write.append("|<><><><><> <><><><><>|")
    data2write.append("| Reciept for booking |")
    data2write.append("|_____________________|")
    data2write.append("|Booking  ID:"+str(BookID))
    data2write.append("|Customer ID:"+str(CustID))
    data2write.append("|---------------------|")
    data2write.append("|     booking info    |")
    data2write.append("|---------------------|")
    data2write.append("|Name: "+str(PFname)+" "+str(PLname))
    data2write.append("|you are boarding on: "+str(TID))
    data2write.append("|With "+str(Bags)+" Bag(s)")
    data2write.append("|---------------------|")
    data2write.append("|     cost info       |")
    data2write.append("|---------------------|")
    data2write.append("|Total cost:")
    data2write.append("|£"+str(Cost)+"")
    data2write.append("|_____________________|")
    data2write.append("|                     |")
    data2write.append("|    extra addition   |")
    data2write.append("|  username/password  |")
    data2write.append("|username: "+str(Cust_Uname))
    data2write.append("|password: "+str(Cust_Pwd))
    data2write.append("|<><><><><> <><><><><>|")
    
    
    ##########end reciept############

    #return receipt as an array
    return data2write


#write the reciept for the booking and return the result
def WriteReciept(Table,recieptid):#
    #check if directory exists and script alreay exists
    chk_RF_exists(Table)
    if(RecieptExists(Table,recieptid)):
        return RecieptPath+Table+"\\"+str(recieptid)+RecieptExt
        #return recieptid

    #query + arg building
    SQLq = SQLpre+Table+SQLpost##build query for receipt
    args = (recieptid,)

    #process query + args then return result
    result = Qman.executequerywithargs(SQLq,args)
    if(SCRIPT_DEBUG):#debug
        print ('\n data got:\n',result,'\n')

    #process data from SQL query then format into reciept to save
    rdat = prep_reciept(result) 
    if(SCRIPT_DEBUG):#debug
        for x in rdat:
            print(x)

    #write to file
    writefilearray(recieptid,rdat,Table)


    #print result to console as minimal output
    print("written id: ",end = '')
    print(RecieptPath+Table+"\\"+str(recieptid)+RecieptExt)

    ##return local path to reciept
    return RecieptPath+Table+"\\"+str(recieptid)+RecieptExt
    #return recieptid

    
def quickWrite(data):
    f = open("static\\report.txt",'w')
    q = []
    for x in data:
        for i in x:
            f.write(str(i)+',')
        f.write('\n')
    f.close()##add safety to this
    
def makeAdminReport():
    SQLq1 = "SELECT * FROM webairbook"
    SQLq2 = "SELECT * FROM webferrybook"
    SQLq3 = "SELECT * FROM webtrainbook"
    conn = Qman.getConnection()
    cursor = conn.cursor()
    
    cursor.execute(SQLq1)
    result = cursor.fetchall()
    cursor.execute(SQLq2)
    result2 = cursor.fetchall()
    cursor.execute(SQLq3)
    result3 = cursor.fetchall()
    conn.close()
    quickWrite(result)
    quickWrite(result2)
    quickWrite(result3)
    return "static\\report.txt"

    

####
##desc: resolve tname
# resolves the transport type to
# a database table
##inputs
# Tmode - as the mode of transport
##outputs
# returner - as the table name for bookings for the transport type
##misc
#
####


##get query
##open file name = Reciepts/[bookingref].txt
##write contents and close
##takes the raw table name for the query and the reciept id to write
##returns the reciept id on completion or -1 for fail if needed
    

        
    
