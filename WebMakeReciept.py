##make reciept


## imports
import os,sys
import mysql.connector

# other imports
import WebSQLUtil as Qman


##vars/defs
# queries for reciept
SQLpre = "SELECT * FROM "
SQLpost = " WHERE ID = %s"

# system path to save reciepts into
RecieptPath = "reciepts\\"
RecieptExt =  ".txt"



##functions/procs

##file io
def readfile(name):
    pass


##writes file array each entry is a new line

def writefilearray(name,data,Table,ext = RecieptExt,fpath=RecieptPath):
    f = open(fpath+Table+"\\"+str(name)+ext,'w')
    for x in data:
        f.write(x+'\n')
    f.close()##add safety to this

##
def chk_RF_exists(Ttype):##checks+creates folders for transport types
    print("dircheck: "+Ttype)
    if(not os.path.isdir(RecieptPath+Ttype)):
        print("making dir:"+Ttype)
        os.mkdir(RecieptPath+Ttype)
##
def RecieptExists(Ttype,rid):##checks whether reciept exists for a given transport type
    ##fsexists
    if(os.path.isfile(RecieptPath+Ttype+"\\"+str(rid)+RecieptExt)):
        return True
    return False

def prep_reciept(data):#format reciept for printing to file
    BookID =data[0][0]
    PFname =data[0][1]
    PLname =data[0][2]
    TID    =data[0][3]
    Bags   =data[0][4]
    Cost   =data[0][5]
    CustID =data[0][6]
    
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
    data2write.append("|<><><><><> <><><><><>|")
    ##########end reciept############
    return data2write

##get query
##open file name = Reciepts/[bookingref].txt
##write contents and close
##takes the raw table name for the query and the reciept id to write
##returns the recieptd id on completion or -1 for fail if needed
def WriteReciept(Table,recieptid):#
    chk_RF_exists(Table)
    if(RecieptExists(Table,recieptid)):
        return recieptid
    ##process receipt
    #conn = Qman.getconn()
    #if (conn == None):
    #    return -1
    
    SQLq = SQLpre+Table+SQLpost##build query for receipt
    args = (recieptid,)
    result = Qman.executequerywithargs(SQLq,args)
    print ('\n data got:\n',result,'\n')
    #return result
    rdat = prep_reciept(result)
    for x in rdat:##debug print result
        print(x)##
    writefilearray(recieptid,rdat,Table)#
    return recieptid

    
    
    

    
    

    

        
    
