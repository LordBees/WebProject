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

##debug mode
SCRIPT_DEBUG = False





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


##writes file array each entry is a new line
def writefilearray(name,data,Table,ext = RecieptExt,fpath=RecieptPath):
    f = open(fpath+Table+"\\"+str(name)+ext,'w')
    for x in data:
        f.write(x+'\n')
    f.close()##add safety to this

##check for folder for each table
def chk_RF_exists(Ttype):##checks+creates folders for transport types
    if(SCRIPT_DEBUG):
        print("dircheck: "+Ttype)
    if(not os.path.isdir(RecieptPath+Ttype)):
        if(SCRIPT_DEBUG):
            print("making dir:"+Ttype)
        os.mkdir(RecieptPath+Ttype)
        
##check for if reciept exists already as no need to reprint
def RecieptExists(Ttype,rid):##checks whether reciept exists for a given transport type
    ##fsexists
    if(os.path.isfile(RecieptPath+Ttype+"\\"+str(rid)+RecieptExt)):
        return True
    return False

####
##desc:
# resolves the transport type to
# a database table
##inputs
# Tmode - as the mode of transport
##outputs
# returner - as the table name for bookings for the transport type
##misc
#
####
def resolve_tname(Tmode):
    returner = "invalid"
    ##
    if  (Tmode == "train"):
        returner = "webtrainbook"
    elif(Tmode == "air"):
        returner = "webairbook"
    elif(Tmode == "ferry"):
        returner = "webferrybook"
    elif(Tmode == "taxi"):
        returner = "invalid"
    elif(Tmode == "bus"):
        returner = "invalid"
    ##
    return returner

#format reciept for printing to file
def prep_reciept(data):
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
##returns the reciept id on completion or -1 for fail if needed
def WriteReciept(Table,recieptid):#
    ##check if directory exists and script alreay exists
    chk_RF_exists(Table)
    if(RecieptExists(Table,recieptid)):
        return RecieptPath+recieptid+RecieptExt
        #return recieptid
    
    ##process receipt
    SQLq = SQLpre+Table+SQLpost##build query for receipt
    args = (recieptid,)
    
    result = Qman.executequerywithargs(SQLq,args)
    if(SCRIPT_DEBUG):
        print ('\n data got:\n',result,'\n')
        #return result
        
    rdat = prep_reciept(result) 
    if(SCRIPT_DEBUG):
        for x in rdat:##debug print result
            print(x)##
            
    writefilearray(recieptid,rdat,Table)#


    ##
    print("written id: ",end = '')
    return RecieptPath+recieptid+RecieptExt
    #return recieptid

    
    
    

    
    

    

        
    
