#!/usr/bin/env python
import socket
import sys
import re
from threading import Thread
from Queue import Queue

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
        # put a new connection on the queue
        self.tasks.put(conn)
        
        
        

class FileServer:
    HOST = ''
    KILL_CMD = r'\s*KILL\s+SERVICE\s*'
    BEACON_CMD = "file_server= {0}:{1}"
    WRITE_CMD = r'\s*write\s+-id\s+\w+\s+-data\s+[\w\s]+\s*'
    GET_CMD = r'\s*get\s+-id\s+\w+\s*'
    FILE_DATA_RESPONSE = "-data:\"{0}\""
    ACK = "OK"

    def __init__(self, numThread, port, directoryServerPort):
        self.port = port
        self.directoryServerPort = directoryServerPort
        self.numThread = numThread
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.bind((self.HOST, int(port)))
        except socket.error, msg:
            print 'Failed to bind the server socket: ' + str(msg[0])
            sys.exit()
        print 'Socket successfully bound.'
        
        self.threadPool = ThreadPool(numThread, self)
        
        self.killCmdRegEx = re.compile(self.KILL_CMD)
        self.writeCmdRegEx = re.compile(self.WRITE_CMD)
        self.getCmdRegEx = re.compile(self.GET_CMD)
        
        self.sendBeaconToDirectoryServer()
    
    def sendBeaconToDirectoryServer(self) :
        print 'Sending beacon to the directory server - advertising its presence.'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('',self.directoryServerPort))
        ipAddress = sock.getsockname()
        msg = self.BEACON_CMD.format(ipAddress[0], self.port)
        response = self.generateResponse(msg)
        sock.sendall(response)
        ack = sock.recv(2048)
        if self.ACK in ack:
            print "Directory server is now successfully aware of the file server"
        else:
            print "Uknown response from the directory server: " + ack
        sock.close()
        
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
        if self.killCmdRegEx.match(data):
            print 'Shutting down...'
            conn.sendall("Shutting down the BaseServer...")
            sys.exit()
        elif self.writeCmdRegEx.match(data):
            print 'Write cmd request received.'
            fileId = self.getFileIdFromRequest(data)
            dataToWrite = self.getDataToWrite(data)
            self.writeFile(fileId, dataToWrite)
            print 'Sending ack.'
            response = self.generateResponse(self.ACK)
            conn.sendall(response)
        elif self.getCmdRegEx.match(data):
            print 'Get cmd request received.'
            fileId = self.getFileIdFromRequest(data)
            fileData = self.getFileData(fileId)
            if None:
                msg = "Error: " + fileId + " - File not found."
                print msg
                response = self.generateResponse(msg)
                conn.sendall(response)
            else:
                print "Sending back file "+fileId+" contents."
                msg = self.FILE_DATA_RESPONSE.format(fileData)
                response = self.generateResponse(msg)
                conn.sendall(response)
        else:
            msg = 'Error - Unrecognized command received. ' + data
            print msg
            response = self.generateResponse(msg)
            conn.sendall(response)
                
    def writeFile(self, fileId, data):
        fileId = fileId.strip()
        print 'Opening the file: ' + fileId
        f = open(fileId, 'w')
        print 'Writing the file: ' + fileId
        f.write(data)
        f.close()
    
    def getFileData(self, fileId):
        f = open(fileId, 'r')
        data = f.read()
        f.close()
        return data
    
    def getDataToWrite(self, requestData):
        dataFlag = '-data'
        dataFlagStartIndex = requestData.find(dataFlag)
        data = requestData[(dataFlagStartIndex+len(dataFlag)):]
        return data
        
    def getFileIdFromRequest(self, requestData):
        idFlag = '-id'
        dataFlag = '-data'
        idFlagStartIndex = requestData.find(idFlag)
        fileId = requestData[(idFlagStartIndex+len(idFlag)):].strip()
        
        dataFlagStartIndex = fileId.find(dataFlag)
        if dataFlagStartIndex != -1:
            fileId = fileId[:dataFlagStartIndex]
            
        return fileId
        
    def generateResponse(self, msg):
        return msg + "\n\n"

def main():
    if len(sys.argv)!=4:
        print 'Invalid number of arguments: 2 arguments required' + \
            '\nport number to which bind the server and the size of the thread pool to be created.'+\
            '\nsize of the thread pool of the server'+\
            '\nport number of the directory server'+\
            '\nActual number of arguments: ' + str(len(sys.argv)-1)
        sys.exit()
    port = int(sys.argv[1])
    numThread = int(sys.argv[2])
    directoryServerPort = int(sys.argv[3])
    fileServer = FileServer(numThread, port, directoryServerPort)
    fileServer.listen()

if __name__ == "__main__":
    main()


