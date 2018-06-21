import socket
import sys
import time
import csv


lastseq = 0
#ensures that a recognized data format is received
def datavalidation(data, ip, filename):
    try:
        
        error = False # assume there are no errors
        if data[0] == "B" or data[0] == "T" or data[0] == "H": #checks for correct type
            if int(data[2]) > 0: #id should be greater than 0
                if float(data[4]) == float(data[4]):#special for python to check if a value is not NaN
                    if int(data[6]) > 0:   
                        logvalues(data, ip, filename)
            #if any conditions are untrue then there was an error
                    else:
                        print data[6], " failed"
                        error = True
                else:
                    print data[4], "failed"
                    error = True
            else:
                print data[2], "failed"
                error = True
        else:
            print data[0], "failed"
            error = True
            #makes the error format easier to read
        return not error
    except Exception as e:
        print "There was an error in received data, error is: \t", e
        return False


#uses the current logfile to store the data received along with the ip address and time
def logvalues(data, ip, filename):
    with open(filename, 'ab') as f:
        global lastseq
        writer = csv.writer(f)
        reader = csv.reader(f)

        #handles possible resubmission
        if data[6] != lastseq:
            writer.writerow([data[0], data[2], data[4], ip, time.asctime()])
                      
        lastseq = data[6]
                 


# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# Bind the socket to the port
host = '123.45.67.89'
port = 5678

#setup csv file for logging data
filename = 'serverlog' + str(int(time.time())) +'.csv'
with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'Unit', 'Value', 'IP', 'Timestamp'])


#start server
print 'starting up on ', host, ' port ', port
s.bind((host, port))

#print statement for verifying data from terminal
print >>sys.stderr, 'Type \t Unit \t Value \t IP \t \t Timestamp'

#continue serving clients until shutdown
while True:
    try:
        data, address = s.recvfrom(4096)
        #records data and address of received data packet
        
        if datavalidation(data, address[0], filename):
            #ensures the data is correctly formated
            print data, "\t", address[0], "\t", time.asctime()
            send = s.sendto(True, address)
        else:
            #requests a retransmission from the client sensor
            print "\n failured to validate data, requesting retransmission"
            send = s.sendto(False, address)
    except KeyboardInterrupt:
        s.shutdown()

