import socket
import sys


def messagetrans():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('123.45.67.89', 1234)

    sensorType = "B" #can be T, H, or B for different sensors
    sensorID = "1" #to be incremented for each sensor used
    sensorData = "101325" #Measurement data from sensor

    message = sensorType + "\t" + sensorID + "\t" + sensorData

    try:

        # Send data
        sock.setblocking(0)
        print >>sys.stderr, 'sending "%s"' % message
        sent = sock.sendto(message, server_address)

        sock.settimeout(5)
        #5 second timeout in the event of a transmission being lost for reliability
        while True:
            try:
                data = sock.recv(4096)
                sock.close()
                return data
            except socket.timeout:
                print "resending data"
                sent = sock.sendto(message, server_address)
                try:
                    data = sock.recv(4096)
                except socket.timeout:
                    print "There was a serious error, try again later"
                    return False
                    #still erroneous transmission, restart from beginning

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

ack = False
#continue trying until a sucessful transmission is established
while ack == False:
    ack = bool(messagetrans())

