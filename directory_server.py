#!/usr/bin/env python
import socket
import sys
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

class DirectoryServer:
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
    directoryServer = DirectoryServer(numThread, port)
    directoryServer.listen()

if __name__ == "__main__":
    main()


