Run instructions:
1.Run the directory server first because it keeps the list of the available file_server's and whenever a file_server is initiated it advertises its presence with the directory_server.
2.Next run either the client or the file server the order does not matter here.

Setup example:
python directory_server.py 6666 20
python file_server.py 6667 20 6666
python file_server.py 6668 20 6666
python client.py 6666


Client:
within the client I have managed to only fully implement two commands:
  - write -path some/path/here -data "data to be written into a file goes here"
  - get -path some/path/here


Note:
I have rushed writing the distribute file system and by no means it is optimal and well designed system. In fact I believe the design is very poor. However it does implement the fundamental concepts of a distributed file server system: the directory server and the file server.

Lock Server:
Unfortunately due to lack of time I have never managed to finish implementing the lock server.

Authentication Server:
If I had more time I would have implement an authentication server for the system that would allow users to have seperate virtual address spaces. I would base the authentication system on the kerberos protocol.
