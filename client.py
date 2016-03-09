#!/usr/bin/env python
import socket
import re
import sys

class Client:
    #WRITE_CMD = r'write -path[\s][\\\w][\s]-data[\s][\w\d\s\S]'
    WRITE_CMD = r'write*'
    GET_CMD = "get -{0}\"{0}\"\n\n" #for dir server the argument is the file path and for the file server the argument is the file_id
    LOCK_CMD = "lock:{0}\n\n"
    UNLOCK_CMD = "unlock:{0}\n\n"
    QUIT_CMD = "quit"

    def __init__(self, clientPort, directoryServerPort):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = clientPort
        self.shouldGetInput = True

    def start(self):
        self.getUserInput()
    
    def getUserInput(self):
        while self.shouldGetInput:
            self.userInput = str(raw_input("Enter command: "))
            self.parseCmd(self.userInput)
    
    def parseCmd(self, cmd):
        self.writeCmdRegEx = re.compile(self.WRITE_CMD)
        if cmd == self.QUIT_CMD:
            print "Exiting client..."
            sys.exit()
        elif self.writeCmdRegEx.match(cmd) != None:
            print "expecting write exec"
        elif cmd.startswith("get ") and cmd.endswith("\n\n"):
            print "expecting get exec"
        elif cmd.startswith("lock ") and cmd.endswith("\n\n"):
            print "expecting lock exec"
        elif cmd.startswith("unlock ") and cmd.endswith("\n\n"):
            print "expecting unlock exec"
        else:
            print "'"+cmd+"'unrecognized command"
        

def main():
    if len(sys.argv)!=3:
        print 'Invalid number of arguments: 2 arguments required, port number to which bind the clint and the port number of the dir server.\nActual number of arguments: ' + str(len(sys.argv)-1)
        sys.exit()
    port = int(sys.argv[1])
    directoryServerPort = int(sys.argv[2])
    client = Client(port, directoryServerPort)
    client.start()

if __name__ == "__main__":
    main()

