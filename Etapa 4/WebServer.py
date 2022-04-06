from typing import Protocol
from FileManager import FileManager
import html

import queue
import socket
import threading
import re

import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080     # Port to listen on

DATABASE_FILE = "ClientDataBase.txt"
#DISCONNECT_SIGNAL = b'disconnect'

fileManager = FileManager()

addresses = {}

class Client_Threads(threading.Thread):
    def __init__(self,queue,client_conn,address):
        threading.Thread.__init__(self)
        self.addr = address
        self.conn = client_conn
        self.queue = queue
        self.authenticated = False
    
    def run(self):
        while True:
            try:
                data = self.queue.get(True,60)
            except queue.Empty:
                break

            self.handle_client(data)

        print(f"closing the connection with {self.addr}")

    def handle_client(self, data):
        string_list = data.split(' ')
        method = string_list[0]
        request = string_list[1]
        response = ""

        if(method == "GET"):
            if(request == "/"):
                response = html.login()
            else:
                response = html.error_page()

            (self.conn).sendall(response.encode())
        
        if(method == "POST"):
            data_list = string_list[len(string_list) - 1].split('&')
            user_response = []
            for index in range (0, len(data_list)):
                user_input = data_list[index].split('=')
                user_response.append(user_input[1])

            if(request == "/"):
                Users_Passwords_file = 'UsersAndPasswords.txt'
                correct_credentials = False
                if (fileManager.csv_find_data(Users_Passwords_file, (user_response[0]+','+user_response[1]))):
                    correct_credentials = True

                if (correct_credentials):
                    response = html.form_page()
                else:
                    response = html.login()

                (self.conn).sendall(response.encode())

            if(request == "/verificar_datos"):
                correct_input = True
                new_input = ""
                id_regex = "^(\w|[.-])+$"
                num_id_regex = "^\d{9}$"
                form_length = len(user_response)
                for index in range(0,form_length):
                    if(index != form_length-1):
                        regex = re.match(id_regex,user_response[index])
                        new_input += user_response[index] + ','
                    else:
                        regex = re.match(num_id_regex,user_response[index])
                        new_input += user_response[index]
                    if(not regex):
                        correct_input = False
                        break
                
                if(correct_input):
                    if fileManager.csv_find_data(DATABASE_FILE, new_input) == False:
                        fileManager.csv_write_file(DATABASE_FILE, new_input)
                    
                    response = html.saved_data_page()
                else:
                    response = html.bad_request_page()
                
                (self.conn).sendall(response.encode())             

        
        self.conn.close()
            
def main():
    print("The server is starting")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"The server is listening in {HOST} on the port {PORT}")
        while True:
            try:
                client_conn, addr = s.accept()
                client_request = client_conn.recv(1024).decode()
                print ('Received Message from [' + str(addr[0]) + ':' + str(addr[1]) + ']')
                
                if client_request:
                    if (addr not in addresses):
                        new_queue = queue.Queue()
                        addresses[addr] = Client_Threads(new_queue,client_conn,addr)
                        addresses[addr].start()
                    
                    addresses[addr].queue.put(client_request)

                print(f"Current Connections {threading.active_count() - 1}")
            except KeyboardInterrupt:
                print("Server is closing")
                break

if __name__ == "__main__":
    main()