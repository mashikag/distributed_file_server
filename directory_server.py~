#!/usr/bin/env python
import socket
import sys
import random
import hashlib
from threading import Thread
from Queue import Queue

"""
The dir server will need to listen for requests to get and write to files(paths)
it will need to store address + port num of file servers and id of files associate with them and paths associate with the ids
hold dictionary of key:path, value:id;ip:port  

receive write request
  if path exists in the dict
    return the id and the address of the file server associated
  if doesnt
    create a new entry in the dic for the path
    return the address of the file server associated in the new entry
receive get request
  if path exists in the dict
    return the id and the address of the file server associated
  else
    return not found error message
"""

STUDENT_ID = '<To be filled in>'
IP = 'some IP'

class Worker(Thread):
    """individual thread that handles the clients requests"""

    def __init__(self, tasks, cmdParser):
        Thread.__init__(self)
        self.tasks = tasks  #each task will be an individual connection
        self.cmdParser = cmdParser
        self.daemon = True
        self.start()

    def run(self):
        while True:
            conn = self.tasks.get()  #take a connection from the queue
            self.cmdParser(conn)
            self.tasks.task_done()



class ThreadPool:
    """pool of worker threads all consuming tasks"""

    def __init__(self, numThread, baseServer):
        self.tasks = Queue(numThread)
        self.baseServer = baseServer
        for _ in range(numThread):
            Worker(self.tasks, baseServer.cmdParser)

    def addTasks(self, conn):
        #put a new connection on the queue
        self.tasks.put(conn)

class DirectoryServer:
    HOST = ''
    PATH_REG_EX = r'\s*[a-zA-Z\\/0-9]+\s*'
    KILL_CMD = r'\s*KILL\s+SERVICE\s*'
    NEW_FILE_SERVER_BEACON = r'\s*file_server:\s*[.0-9]*:[0-9]+\s*'
    SERVER_NAME = "directory_server"

    def __init__(self, numThread, port):
        self.port = port
        self.numThread = numThread
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.bind((self.HOST, int(port)))
        except socket.error, msg:
            print 'Failed to bind the server socket: ' + str(msg[0])
            sys.exit()
        print 'Socket successfully bound.'
        self.threadPool = ThreadPool(numThread, self)
        
        self.pathReqRegEx = re.compile(self.PATH_REG_EX)
        self.newFileServerBeacon = re.compile(self.NEW_FILE_SERVER_BEACON)
        self.killCmdRegEx = re.compile(self.KILL_CMD)
        
        self.directoriesDict = {}
        self.fileServersList = []
        
    def listen(self):
        print 'Server preparing to listen.'
        maxQueuedConnections = 5
        self.sock.listen(maxQueuedConnections)
        print 'Server listening on port: ' + str(self.port)
        while True:
            connection, address = self.sock.accept()
            print 'Incoming connection established with ' + addr[0] + ':' + str(addr[1])
            self.threadPool.addTasks(connection)

    def cmdParser(self, conn):
        while conn:
            data = conn.recv(2048)
            if self.killCmdRegEx.match(data):
                print 'Shutting down...'
                conn.sendall("Shutting down the Directory Server...")
                sys.exit()
            elif self.pathReqRegEx.match(data):
                print 'file server data requested for a path'
                path = data.strip()
                fileServerAddress = ''
                fileServerFileId = ''
                fileServerAddress, fileServerFileId = getFileServerData(path)
                if fileServerAddress is not None and fileServerFileId is not None:
                    response = generateResponse(fileServerFileId + ";" + fileServerAddress)
                else:
                    response = generateResponse("101-ERROR: unnable to get file server data. Possibly directory server is unaware of any running file servers. ")
                conn.sendall(response)
            elif self.newFileServerBeacon.match(data):
                print 'received new file server beacon'
                """TO DO NEXT"""
                """TO DO NEXT"""
                """TO DO NEXT"""
                """TO DO NEXT"""
                """TO DO NEXT"""
                """TO DO NEXT"""
            else:
                print 'unsupported command received'
                response = generateResponse("100-ERROR: unsupported command received")
                conn.sendall()
    
    def pathExists(self, path):
        exists = false
        
        if path in self.directoriesDict:
            exists = true
            
        return exists
        
    def getFileServerData(self, path):
        address = ''
        fileId = ''
        
        if pathExists(path)
            print 'path already exists in the dictionary'
            serverData = str(directoriesDict[path])
            serverDataSplit = serverData.split(';',1)
            fileId = serverDataSplit[0]
            address = serverDataSplit[1]
        elif
            print 'new path to be added to the dictionary'
            address = pickFileServer()
            if address is None:
                print "Unable to pick file server"
                return (None, None)
            else:
                fileId = generateFileId()
        return (address, fileId)
    
    def generateFileId(self):
        fileId = hashlib.sha224(path).hexdigest()
        print 'generated new file server fileID: ' + fileId
        return fileId
        
    def pickFileServer(self):
        'picking file server randomly'
        fileServerListLength = len(self.fileServersList)
        if fileServerListLength > 0:
            fileServerIndex = random.randint(0, fileServerListLength)
        else
            return None
        return self.fileServersList[fileServerIndex]
            
    def generateResponse(self, message):
        return self.SERVER_NAME + "=" + message

def main():
    if len(sys.argv)!=3:
        print 'Invalid number of arguments: 2 arguments required, port number to which bind the server and the size of the thread pool to be created.\nActual number of arguments: ' + str(len(sys.argv)-1)
        sys.exit()
    port = int(sys.argv[1])
    numThread = int(sys.argv[2])
    directoryServer = DirectoryServer(numThread, port)
    directoryServer.listen()

if __name__ == "__main__":
    main()


