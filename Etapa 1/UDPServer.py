from typing import Protocol
from FileManager import FileManager

import queue
import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432     # Port to listen on
FORMAT = "ISO-8859-1"
DISCONNECT_SIGNAL = b'disconnect'

fileManager = FileManager()
addresses = {}

class Client_Threads(threading.Thread):
    def __init__(self,queue,addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.queue = queue
    
    def run(self):
        while True:
            try:
                data = self.queue.get(True,120)
            except queue.Empty:
                break
            signal = data[:10]
            if(signal == DISCONNECT_SIGNAL):
                del addresses[self.addr]
                break
            self.handle_client(data)

        print(f"closing the connection with {self.addr}")

    def handle_client(self, data):
        receivedMessage = bytes.decode(data,encoding=FORMAT).split(",")
        # Grant or deny access to client.
        if (len(receivedMessage) == 2):
            file = 'UsersAndPasswords.txt'
            if (fileManager.csv_find_data(file, (receivedMessage[0]+','+receivedMessage[1]))):
                reply = str.encode('Acceso otorgado')
            else:
                reply =  str.encode('Acceso denegado')
        else:
            receivedMessage = bytes.decode(data,encoding=FORMAT)

            sentMessagesCount = int.from_bytes(data[-16:-12],'big') #4
            messagesToBeSent = int.from_bytes(data[-12:-8],'big') #5
            messageSize = int.from_bytes(data[-8:-4],'big') #6
            receivedPackages = int.from_bytes(data[-4:], 'big') # 7

            
            if(len(data) == messageSize*receivedPackages+16):
                # build reply
                receivedBytesStart = (sentMessagesCount*messageSize).to_bytes(4,'big')
                receivedBytesFinish = (receivedPackages*messageSize).to_bytes(4, 'big')
                bytesToBeReceived = (messagesToBeSent* messageSize).to_bytes(4,'big')
                packagesArrived = (receivedPackages).to_bytes(4,'big')

                reply = receivedBytesStart + receivedBytesFinish + bytesToBeReceived + packagesArrived
                
                file = 'Database.txt'
                bytecounter = 0
                while(bytecounter < messageSize*receivedPackages):
                    client_data = data[bytecounter:bytecounter+18]
                    bytecounter += 18
                    # only add data if it didnt already exist in dataBase.
                    if fileManager.csv_find_data(file, bytes.decode(client_data,encoding=FORMAT)) == False:
                        fileManager.csv_write_file(file, bytes.decode(client_data,encoding=FORMAT))
            else:    
                reply = (0).to_bytes(4,'big')
        # send message to client.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(reply , self.addr)
            
def main():
    print("The server is starting")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"The server is listening on {HOST} in the port {PORT}")
        while True:
            try:
                data, addr = s.recvfrom(1024)
                print ('Received Message from [' + str(addr[0]) + ':' + str(addr[1]) + ']')
                if data:
                    if (addr not in addresses):
                        new_queue = queue.Queue()
                        addresses[addr] = Client_Threads(new_queue,addr)
                        addresses[addr].start()
                    
                    addresses[addr].queue.put(data)

                print(f"Current Connections {threading.active_count() - 1}")
            except KeyboardInterrupt:
                print("Server is closing")
                break

if __name__ == "__main__":
    main()