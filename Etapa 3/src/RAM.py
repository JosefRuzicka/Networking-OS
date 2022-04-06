import PageTable
import HardDrive

class RAM:
    #TODO check the ram_size (80 bytes)
    
    def __init__(self, ram_size, page_size):
        self.ram_size = ram_size
        self.ram_structure = self.make_structure_ram()
        self.page_size = page_size
        self.pageTable = 0
        #self.enrutador = enrutador

    def make_structure_ram(self):
        structure = ["-" for i in range(self.ram_size)]
        return structure

    def find_in_ram(self, physicalDirection, ID): 
        port = ""
        extractId ="-"
        try:
            page = self.ram_structure[int(physicalDirection)]

            print("-----------------PAGINA ACTUAL---------------" )
            print(page)
            print()
            for index in range(self.page_size): #recorre el page
                extractId = self.extract_virtualDirection(ID, page[index])
                if (extractId == page[index]):
                    port = page[index+1] # redes
                    print("---------------RETORNO/OBTENER DATOS--------------------")
                    print(f"RAM retorna : {port}")
                    print()
                    #self.enrutador.get_data(port) #TODO check
                    break 
        except:
            raise NameError("The data isn't in the RAM")
            
    def extract_virtualDirection(self, current_ID, virtualdirection):
        position = current_ID.find(virtualdirection)
        index = 0
        extract_ID = ""
        try:
            while(current_ID[position+index] != ","):
                extract_ID += current_ID[position+index]
                if (index-1 < len(current_ID)):
                    index += 1
        except:
            print("")
        return extract_ID

    def find_page_in_ram(self, physicalDirection): 
        physicalDirection = int(physicalDirection)
        page = []
        try:
            page = self.ram_structure[physicalDirection]
        except:
            page = False
        return page

    def replace_page_in_ram(self, physicalDirection, page): 
        page = []
        try:
            page = self.ram_structure[physicalDirection]
        except:
            page = False
        return page
    
    def add_to_ram(self, page, victimPage, ID):
        flag = False
        data =  ["-" for i in range(5)]
        data[0] = ID
        data[1] = "1"
        data[2] = "1"
        data[3] = "1"
        for index in range(self.ram_size):
            if (flag != True) :
                if (self.ram_structure[index] == "-"):
                    self.ram_structure[index] = page
                    data[4] = index
                    self.pageTable.refresh_data(data) # TODO 
                    flag = True
                else:
                    position = self.deletePage(victimPage) 
                    self.ram_structure[position] = page
                    data[4] = position
                    self.pageTable.refresh_data(data) 
                    #TODO solo modificar el R o el M ?
                    flag = True
            else:
                break
        return flag
    
    def deletePage(self,victim_page_ID): # TODO victim page is the ID page
        new_position = 0
        for actual_position in range(len(self.ram_structure)):
            position = self.ram_structure[actual_position]
            if (position == victim_page_ID):
                self.ram_structure[actual_position] = ["-"] 
                new_position = actual_position
        return new_position
