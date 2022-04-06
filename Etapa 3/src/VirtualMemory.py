import HardDrive
import RAM
import TLB
import PageTable


class VirtualMemory:

    def __init__(self,ram_size, page_size, hardDrive_size, pageTable_size, tlb_size):
        self.ram = RAM.RAM(ram_size, page_size)
        self.current_pageTable = PageTable.PageTable(pageTable_size, self.ram)
        self.current_hardDrive = HardDrive.HardDrive(hardDrive_size, page_size, self.ram, self.current_pageTable)
        self.current_tlb = TLB.TLB(tlb_size, self.ram, page_size ,self.current_pageTable)
        #Usar las mismas estructuras
        self.ram.pageTable = self.current_pageTable
        self.current_pageTable.tlb = self.current_tlb 
        self.current_pageTable.hardDrive = self.current_hardDrive

    def add_data(self, data):# redes 
        flag = False
        self.current_hardDrive.add_to_hardDrive(data) #(ID, otra, ID, otra )
        return flag
    
    def refresh_data(self, data):# redes 
        flag = False
        self.current_hardDrive.refresh_data_hardDrive(data) #"x,y"
        return flag

    def obtenerDatos(self, id):
        flag = self.current_tlb.find_in_tlb(id)

    #
    def print_hard_drive(self):
        print(self.current_hardDrive.structure_hardDrive)

    def refresh_data_hardDrive(self,routing_data):
        flag = False
        data = routing_data.split(",", len(routing_data))
        for index in range (self.current_hardDrive.hardDrive_size):
            if (self.current_hardDrive.structure_hardDrive[index] == data[0]):
                data_index = 0
                while (data_index < len(data)) :
                    self.current_hardDrive.structure_hardDrive[index] = data[data_index]
                    index += 1
                    data_index += 1
                    flag = True
                    self.current_hardDrive.refresh_page(index, data)
                break
        return flag
    
    def print_structures(self):
        print("-------------HARD DRIVE-----------------")
        print(self.current_hardDrive.structure_hardDrive)
        print("----------------------------------------")
        print()
        
        print("-------------PAGE TABLE-----------------")
        for row in range(len(self.current_pageTable.structure_pageTable)):
            for column in range(6):
                print(self.current_pageTable.structure_pageTable[row][column], end= " ")
            print()
        print("----------------------------------------")
        print()

        print("-----------------TLB--------------------")
        for row in range(len(self.current_tlb.structure_tlb)):
            for column in range(3):
                print(self.current_tlb.structure_tlb[row][column], end= " ")
            print()
        print("----------------------------------------")
        print()

        print("-----------------RAM--------------------")
        for row in range(len(self.ram.ram_structure)):
            print(self.ram.ram_structure[row], end= " ")
        print("----------------------------------------")
        print()
    

