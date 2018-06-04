# Networking
Basic networking programs to look into UDP and TCP sockets

Meant as an excerise for principles of communication II, there are programs for a UDP server and UDP client.
The intention is to make UDP reliable by adding features such as data acknowledgement and checksum.

The sensors are for a temperature, humidity, and barometric pressure sensor which are reporting measurements to a server which logs the data.

Checksum is not implemented as of 6/4/2018

It is not entirely error proof, and includes methods which would throw errors, such as inputing illegal datatypes into the checked values,
so this code should not actually be used without monitoring to ensure that the server remains running in case of errors.
