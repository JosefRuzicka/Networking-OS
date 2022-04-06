
import sys
import socket
import threading
import queue
import time

import networkx as nx # python -m pip install networkx
from FileManager import FileManager
import VirtualMemory

P_FLAG = 0
C_FLAG = 1
CONFIG_FILE = "config.txt"
FORMAT = "ISO-8859-1"

fileManager = FileManager()
virtualMemory = None
idP = "-"
idC = "-"
routing_table_mutex = threading.Lock()
routing_table = [] # ID Prov, Puerto, Hops
ports = []
gateway_added = threading.Event()

# BGP
# ‘T’,Yo (C1) , Provincia1, Distancia, ruta, Provincia2, Distancia, ruta … ProvinciaN, Distancia, ruta 
#  T,P2,P1,Port,1,P3,Port,1

# OSPF
# ‘T’,Enviador , Canton, Vecino1, Vecino2
# ‘T’, C1, C1, C2, C3

class Physical_Port(threading.Thread):
    def __init__(self,port_number,queue,values,typeflag,flag):
        threading.Thread.__init__(self)
        self.port_number = port_number
        self.typeflag = typeflag
        self.queue = queue
        self.flag = flag
        self.values = values
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def run(self):
        self.handle_connections()

    def handle_connections(self):
        if (self.flag == 0): # Server
                self.socket.bind((self.values[1], int(self.values[2])))
                print(f"Socket Now listening in host {self.values[1]} and port {self.values[2]} ")
                print(f"Connected to physical port {self.port_number}")
                self.socket.listen()
                self.socket, addr = self.socket.accept()

        else: # Client
                connected = False
                while not connected:
                    try:
                        self.socket.connect((self.values[1], int(self.values[2])))
                        connected = True
                    except:
                        continue
                
        if(self.typeflag == P_FLAG):
            self.add_to_p_routing_table(idP,self.values[0],str(self.port_number),"1")
        else:
            self.add_to_c_routing_table(idC,self.values[0],str(self.port_number))

        if (self.port_number == 0):
            gateway_added.set()
        self.listen()

    def add_to_p_routing_table(self,senderID,neighborID,port,hops): 
        routing_table_mutex.acquire()

        if(senderID != idP and neighborID != idP):
            if(senderID in routing_table):
                if(not neighborID in routing_table):
                    index = routing_table.index(senderID)
                    #routing_table.append(neighborID)
                    #routing_table.append(routing_table[index+1])
                    #routing_table.append(str((int(hops)+int(routing_table[index+2]))))
                else:
                    index = routing_table.index(neighborID)
                    if ((int(hops)+int(routing_table[index+2])) < (int(routing_table[index+2]))):
                        routing_table[index+1] = port
                        routing_table[index+2] = hops
        else:
            if(not neighborID in routing_table and neighborID != idP ):
                #new_data = neighborID + "," + port + "-" + hops
                #virtualMemory.add_data(new_data)
                #virtualMemory.printhard_drive()
                routing_table.append(neighborID)
                routing_table.append(port)
                routing_table.append(hops)

        routing_table_mutex.release()

    def add_to_c_routing_table(self,senderID,neighborID,port): 
        routing_table_mutex.acquire()
        if(senderID != idC and neighborID != idC):
            routeExists = False

            for index in range(0,len(routing_table),3):
                if((routing_table[index] == senderID or routing_table[index+1] == senderID) and (routing_table[index] == neighborID or routing_table[index+1] == neighborID)):
                    routeExists = True
            
            if (not routeExists):
                routing_table.append(senderID)
                routing_table.append(neighborID)
                routing_table.append(port)
        else:
            if(not neighborID in routing_table and neighborID != idC ):
                #new_data = idC + "-" + neighborID + "," + port
                #virtualMemory.add_data(new_data)
                #virtualMemory.printhard_drive()
                routing_table.append(idC)
                routing_table.append(neighborID)
                routing_table.append(port)

        routing_table_mutex.release()

    def dijkstra(self,start_point,destination):
        prov_graph = nx.Graph()
        for index in range(0,len(routing_table),3):
            edge = []
            edge.append(routing_table[index])
            edge.append(routing_table[index+1])
            prov_graph.add_edge(*edge)
        
        djk_path= nx.dijkstra_path(prov_graph, source=start_point, target=destination, weight=False)
        return djk_path[1]

    def listen(self):
        while(True):
            self.socket.settimeout(1)
            msg_received = False
            received_by_queue = False
            data = 0
            try:
                data = self.socket.recv(1024)
                msg_received = True
            except socket.timeout:
                try:
                    data = self.queue.get(True,1)
                    msg_received = True
                    received_by_queue = True
                except queue.Empty:
                    continue
            
            if (msg_received):
                message = bytes.decode(data,encoding=FORMAT).split(",")
                if(len(message) > 2):         
                    self.socket.settimeout(None)
                    if(message[0] == "T"):      # If message type is T
                        self.handle_table_message(received_by_queue,data)
                    elif(message[0] == "M"):    # If message type is M
                        self.handle_message(received_by_queue,data)
                            
    def handle_table_message(self,received_by_queue,data):
        message = bytes.decode(data,encoding=FORMAT).split(",")
        if(received_by_queue):
            self.socket.sendall(data)
        else:
            if(self.typeflag == P_FLAG):
                # T, P1, P, Hops
                for index in range(2,len(message),3):
                    if (self.port_number != 0):
                        self.add_to_p_routing_table(message[1],message[index],message[index+1],0)
            else:
                # ‘T’,Enviador , Canton, Vecino1, Vecino2
                # ‘T’, C1, C1, C2, C3
                if(message[1] != idC and message[1] != idP):
                    new_data = message[0] + "," + idC + "," + message[2]
                    for index in range(3,len(message)):
                        if (message[index].find('T') != -1):
                            break
                        port = self.port_number
                        self.add_to_c_routing_table(message[2],message[index],port)
                        new_data += "," + message[index]
                    new_data_bytes = str.encode(new_data,encoding=FORMAT)
                    if(message[2] != idC):
                        self.socket.sendall(new_data_bytes)

    def handle_message(self,received_by_queue,data):
        message = bytes.decode(data,encoding=FORMAT).split(",")
        if (received_by_queue):
            print(f"Mensaje a enviar: {message}")
            self.socket.sendall(data)
        else:
            # M,01,02,03,117000951
            #‘M’,Provincia_Destino, Cantón_Destino, Area_Salud_Destino, Datos 
            if(self.typeflag == P_FLAG):
                if (message[1] == idP):
                    ports[0].queue.put(data)
                else:
                    if (message[1] in routing_table):
                        # find destination P in routing table
                        routeIndex = routing_table.index(message[1])
                        port = int(routing_table[routeIndex+1])
                        # find port to destination P in Ports and put data in its queue.
                        ports[port].queue.put(data)
                    else:
                        print(f"{message[2]} was not found in routing table.")
            else:
                if (message[1] == idP):
                    if (message[2] == idC):
                        print(f"Mensaje: {message} llego correctamente")
                    else:
                        #dijkstra para el canton correcto
                        next_hop = self.dijkstra(idC,message[2])
                        routeIndex = routing_table.index(next_hop)
                        for index in range(0,len(routing_table),3):
                            if((routing_table[index] == idC or routing_table[index+1] == idC) and
                            (routing_table[index] == next_hop or routing_table[index+1] == next_hop)):
                                port = int(routing_table[index+2])
                                ports[port].queue.put(data)
                                break
                else:
                    #dijkstra para el gateway y agregar en la cola del 2do slot del dijkstra path
                    next_hop = self.dijkstra(idC,idP)
                    routeIndex = routing_table.index(next_hop)
                    for index in range(0,len(routing_table),3):
                        if((routing_table[index] == idC or routing_table[index+1] == idC) and
                        (routing_table[index] == next_hop or routing_table[index+1] == next_hop)):
                            port = int(routing_table[index+2])
                            ports[port].queue.put(data)
                            break

class Router:
    def __init__(self,type_flag):
        self.type_flag = type_flag

    def run(self):
        self.read_configuration()
        self.send_RoutingTable()
        
    def send_RoutingTable(self):
        m_counter = 1
        while(True):
            time.sleep(10)
            print("Enviando Tablas de enrutamiento")
            routing_table_mutex.acquire()
            print(routing_table)
            msg_to_send = "T,"
            if(self.type_flag == P_FLAG):
                msg_to_send += idP
                for index in range(3,len(routing_table),3):
                    msg_to_send += "," + routing_table[index] + "," + routing_table[index+1] + "," + routing_table[index+2]
            else:
                msg_to_send += idC + "," + idC
                for index in range(0,len(routing_table),3):
                    if(routing_table[index] == idC):
                        msg_to_send += "," + routing_table[index+1]

            # only send message if (not P_C_ConnectionFlag)
            bytes_to_send = str.encode(msg_to_send,encoding=FORMAT)
            for port_num in range(0,len(ports)):
                ports[port_num].queue.put(bytes_to_send)

            routing_table_mutex.release()

            #### Enviando mensajes para pruebas
            if(m_counter%6 == 0):
                if(idC == "C3"):
                    msg_to_send = "M,P3,C6,0,117000951"
                    bytes_to_send = str.encode(msg_to_send,encoding=FORMAT)
                    for port_num in range(0,len(ports)):
                        ports[port_num].queue.put(bytes_to_send)

            if(m_counter%8 == 0):
                if(idC == "C4"):
                    msg_to_send = "M,P1,C3,0,117000951"
                    bytes_to_send = str.encode(msg_to_send,encoding=FORMAT)
                    for port_num in range(0,len(ports)):
                        ports[port_num].queue.put(bytes_to_send) 
            m_counter += 1
            ####
            
    def read_configuration(self):

        if(self.type_flag == P_FLAG):
            sv_neighbors, c_neighbors = fileManager.list_neighbors_lines(CONFIG_FILE,idP)
        else:
            sv_neighbors, c_neighbors = fileManager.list_neighbors_lines(CONFIG_FILE,idC)

        port_counter = 0
        if len(sv_neighbors) != 0:
            for line in sv_neighbors:
                values = self.extract_values_from_line(line,0)
                new_queue = queue.Queue()
                ports.append(Physical_Port(port_counter,new_queue,values,self.type_flag,0))
                port_counter+= 1

        if len(c_neighbors) != 0:
            for line in c_neighbors:
                values = self.extract_values_from_line(line,1)
                new_queue = queue.Queue()
                ports.append(Physical_Port(port_counter,new_queue,values,self.type_flag,1))
                port_counter+= 1

        for index in range(0,len(ports)):
            ports[index].start()
            if (self.type_flag == P_FLAG):
                gateway_added.wait()


    def extract_values_from_line(self,line,flag): # Enviar a filemanager
        list = []
        words = line.split(',')
        # if flag is server = 0
        if (flag == 0):
            list.append(words[1])
        else:
            list.append(words[0])

        list.append(words[2])
        list.append(words[3])
        return list


if __name__ == "__main__":
    if (len(sys.argv) == 2):
        p_router = Router(P_FLAG)
        idP = sys.argv[1]
        #virtualMemory = VirtualMemory.VirtualMemory(32,8,128,40,12,p_router)
        p_router.run()
    else:
        if(len(sys.argv) == 3):
            c_router = Router(C_FLAG)
            idP = sys.argv[1]
            idC = sys.argv[2]
            #virtualMemory = VirtualMemory.VirtualMemory(80,12,256,50,25,c_router)
            c_router.run()
        else:
            print("Por favor use: [Ejecutable] [ID Provincial] [ID Cantonal] \n Ultimo parametro Opcional. ")