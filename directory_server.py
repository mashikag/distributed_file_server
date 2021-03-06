#!/usr/bin/env python
import socket
import sys
import random
import hashlib
import re
from threading import Thread
from Queue import Queue


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
    PATH_REG_EX = r'-\s*path\s*[a-zA-Z\\/0-9]+\s*'
    KILL_CMD = r'\s*KILL\s+SERVICE\s*'
    NEW_FILE_SERVER_BEACON = r'\s*file_server=\s*[.0-9]*:[0-9]+\s*'
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
            print 'Incoming connection established with ' + address[0] + ':' + str(address[1])
            self.threadPool.addTasks(connection)

    def cmdParser(self, conn):
          data = conn.recv(2048)
          print 'Data received: ' + data.strip()
          if self.killCmdRegEx.match(data):
              print 'Shutting down...'
              conn.sendall("Shutting down the Directory Server...")
              sys.exit()
          elif self.pathReqRegEx.match(data):
              print 'file server data requested for a path'
              pathKeyWord = "-path"
              pathKeyWordStartIndex = data.find(pathKeyWord)
              path = data[(pathKeyWordStartIndex + len(pathKeyWord)):]
              path = path.strip()
              fileServerAddress = ''
              fileServerFileId = ''
              fileServerAddress, fileServerFileId = self.getFileServerData(path)
              if fileServerAddress is not None and fileServerFileId is not None:
                  response = self.generateResponse(fileServerFileId + ";" + fileServerAddress)
              else:
                  response = self.generateResponse("101-ERROR: unnable to get file server data. Possibly directory server is unaware of any running file servers. ")
              print 'sending response'
              conn.sendall(response)
          elif self.newFileServerBeacon.match(data):
              address = data.split('=',1)[1]
              address.strip()
              print 'received new file server beacon from ' + address
              self.fileServersList.append(address)
              response = self.generateResponse("OK")
              print 'sending an ack'
              conn.sendall(response)
          else:
              print 'unsupported command received'
              response = self.generateResponse("100-ERROR: unsupported command received")
              conn.sendall(response)
    
    def pathExists(self, path):
        exists = False
        
        if path in self.directoriesDict:
            exists = True
            
        return exists
        
    def getFileServerData(self, path):
        address = ''
        fileId = ''
        
        if self.pathExists(path):
            print 'path already exists in the dictionary'
            serverData = str(directoriesDict[path])
            serverDataSplit = serverData.split(';',1)
            fileId = serverDataSplit[0]
            address = serverDataSplit[1]
        else:
            print 'new path to be added to the dictionary'
            address = self.pickFileServer()
            if address is None:
                print "Unable to pick file server"
                return (None, None)
            else:
                fileId = self.generateFileId(path)
        return (address, fileId)
    
    def generateFileId(self, path):
        fileId = hashlib.sha224(path).hexdigest()
        print 'generated new file server fileID: ' + fileId
        return fileId
        
    def pickFileServer(self):
        'picking file server randomly'
        fileServerListLength = len(self.fileServersList)
        if fileServerListLength > 0:
            fileServerIndex = random.randint(0, fileServerListLength-1)
        else:
            return None
        return self.fileServersList[fileServerIndex]
            
    def generateResponse(self, message):
        return self.SERVER_NAME + "=" + message + "\n\n"

def main():
    if len(sys.argv)!=3:
        print 'Invalid number of arguments: 2 arguments required.' +\
           '\n-port number to which bind the server and the size of the thread pool to be created.' +\
           '\n-size of the thread pool of the server' +\
           '\nActual number of arguments: ' + str(len(sys.argv)-1)
        sys.exit()
    port = int(sys.argv[1])
    numThread = int(sys.argv[2])
    directoryServer = DirectoryServer(numThread, port)
    directoryServer.listen()

if __name__ == "__main__":
    main()


