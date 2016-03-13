#!/usr/bin/env python
import socket
import re
import sys

class Client:
    WRITE_CMD = r'write\s+-path\s+[a-zA-Z\\/0-9]+\s+-data\s".*"$'
    GET_CMD = r'get\s+-((path)|(id))\s+[a-zA-Z\\/0-9]+' #for dir server the argument is the file path and for the file server the argument is the file_id
    LOCK_CMD = r'lock\s+-id\s+\w+'
    UNLOCK_CMD = r'unlock\s+-id\s+\w+'
    QUIT_CMD = "quit"
    DIRECTORY_SERVER_NAME = "directory_server"

    def __init__(self, directoryServerPort):
        self.directoryServerPort = directoryServerPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shouldGetInput = True
        
        self.writeCmdRegEx = re.compile(self.WRITE_CMD)
        self.getCmdRegEx = re.compile(self.GET_CMD)
        self.lockCmdRegEx = re.compile(self.LOCK_CMD)
        self.unlockCmdRegEx = re.compile(self.UNLOCK_CMD)

    def start(self):
        self.getUserInput()
    
    def getUserInput(self):
        while self.shouldGetInput:
            self.userInput = str(raw_input("Enter command: "))
            self.parseCmd(self.userInput)
    
    def parseCmd(self, cmd):
        if cmd == self.QUIT_CMD:
            print "Exiting client..."
            sys.exit()
        elif self.writeCmdRegEx.match(cmd) != None:
            print "expecting write exec"
            
            pathRegExRaw = r'\s-path\s+[a-zA-Z\\/0-9]+\s+'
            pathRegEx = re.compile(pathRegExRaw)
            pathMatch = pathRegEx.search(cmd)
            pathStr = cmd[pathMatch.start() : pathMatch.end()].split()[1]
            
            dataStr = cmd[pathMatch.end() : ].split()[1] #-data part of the cmd starts after path part finishes
            dataStr = dataStr[1:-1] #get rid of the quotations
            
            self.getFileServerData(pathStr)
        elif self.getCmdRegEx.match(cmd) != None:
            print "expecting get exec"
            pathRegExRaw = r'\s-path\s+[a-zA-Z\\/0-9]+\s*'
            pathRegEx = re.compile(pathRegExRaw)
            pathMatch = pathRegEx.search(cmd)
            if pathMatch:
                print 'get path argument found assuming call to the directory server'
                pathStr = cmd[pathMatch.start() : pathMatch.end()].split()[1]
                print "path: " + pathStr
            else:
                print 'get path argument not found assuming call to the file server'
                idRegExRaw = r'\s-id\s+[a-zA-Z\\/0-9]+\s*'
                idRegEx = re.compile(idRegExRaw)
                idMatch = idRegEx.search(cmd)
                if idMatch:
                    idStr = cmd[idMatch.start() : idMatch.end()].split()[1]
                    print "id: " + idStr
        elif self.lockCmdRegEx.match(cmd) != None:
            idRegExRaw = r'\s-id\s+[a-zA-Z\\/0-9]+\s*'
            idRegEx = re.compile(idRegExRaw)
            idMatch = idRegEx.search(cmd)
            if idMatch:
                idStr = cmd[idMatch.start() : idMatch.end()].split()[1]
                print "id: " + idStr
        elif self.unlockCmdRegEx.match(cmd) != None:
            print "expecting unlock exec"
            print 'get path argument not found assuming call to the file server'
            idRegExRaw = r'\s-id\s+[a-zA-Z\\/0-9]+\s*'
            idRegEx = re.compile(idRegExRaw)
            idMatch = idRegEx.search(cmd)
            if idMatch:
                idStr = cmd[idMatch.start() : idMatch.end()].split()[1]
                print "id: " + idStr
        else:
            print "'"+cmd+"'unrecognized command"
        
    def getFileServerData(self, path):
        fileId = ''
        ipAddress = ''
        port = 0
        pathKeyWord = "-path"
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('',self.directoryServerPort))
        sock.sendall(pathKeyWord + " " + path)
        dirServerResponse = ''
        while "\n\n" not in dirServerResponse:
            print 'receiving data'
            dirServerResponse += sock.recv(2048)
        sock.close()
        if "ERROR" in dirServerResponse:
            print dirServerResponse
        else:
            print dirServerResponse
            dirServerResponse.strip()
            dirServerResponse = dirServerResponse[(len(self.DIRECTORY_SERVER_NAME)+1):] #strip off the server name prefix of the response
            
            print dirServerResponse
            fileId, address = dirServerResponse.split(";",1)
            ipAddress, port = address.split(":",1)
            print "Files server data extracted: fileId="+fileId+"; address="+ipAddress+":"+port
        return (fileId, ipAddress, port)
        
        
def main():
    if len(sys.argv)!=2:
        print 'Invalid number of arguments: 2 arguments required.' + \
            '\n-port number of the dir server\nActual number of arguments: ' + \
            str(len(sys.argv)-1)
        sys.exit()
    directoryServerPort = int(sys.argv[1])
    client = Client(directoryServerPort)
    client.start()

if __name__ == "__main__":
    main()

