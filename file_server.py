#!/usr/bin/env python
import socket
import sys
from threading import Thread
from Queue import Queue

STUDENT_ID = '<To be filled in>'
IP = 'some IP'

class Worker(Thread):
    """individual thread that handles the clients requests"""

    def __init__(self, tasks, cmdParser):
        Thread.__init__(self)
        self.tasks = tasks  # each task will be an individual connection
        self.cmdParser = cmdParser
        self.daemon = True
        self.start()

    def run(self):
        # run forever
        while True:
            conn = self.tasks.get()  # take a connection from the queue
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
            if data == "KILL SERVICE\n":
                print 'Shutting down...'
                conn.sendall("Shutting down the BaseServer...")
                sys.exit()
            elif data.startswith("HELO ") and data.endswith("\n"):
                conn.sendall('{}\nIP:{}\nStduentID:{}\n'.format(data, IP, self.port, STUDENT_ID))
        

def main():
    if len(sys.argv)!=3:
        print 'Invalid number of arguments: 2 arguments required, port number to which bind the server and the size of the thread pool to be created.\nActual number of arguments: ' + str(len(sys.argv)-1)
        sys.exit()
    port = int(sys.argv[1])
    numThread = int(sys.argv[2])
    fileServer = FileServer(numThread, port)
    fileServer.listen()

if __name__ == "__main__":
    main()


