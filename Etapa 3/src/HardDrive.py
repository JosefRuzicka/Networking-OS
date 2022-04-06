import RAM
import PageTable



class HardDrive:
    # TODO check the size (256 bytes)
    def __init__(self, hardDrive_size, page_size, ram, pageTable):
        self.hardDrive_size = hardDrive_size
        self.page = []
        self.page_size = page_size
        self.structure_hardDrive = self.make_structure_hardDrive()
        self.ram = ram
        self.pageTable = pageTable

    def make_structure_hardDrive(self):
        structure = ["-" for data_index in range(self.hardDrive_size)]
        return structure

    def make_new_page(self):  # routing data is a string
        structure = ["-" for data_index in range(self.page_size)]
        return structure

    def add_data_in_page(self, page, physical_direction):  # routing data is a string
        flag = False
        top_page = int(physical_direction)
        end_page = top_page + self.page_size
        # si esta medio vacio ver cuanto puedo llenar de la pagina
        actual_size = 0
        if (self.hardDrive_empty != True):
            for index in range(self.hardDrive_size):
                if (self.structure_hardDrive[index] != '-'):
                    actual_size += 1 
                elif(self.structure_hardDrive[index] == '-'):
                    index = self.hardDrive_size
            if (actual_size < self.page_size and actual_size != 0):
                flag = self.fill_page_notFull_hardDrive(actual_size, page)
            elif (actual_size > self.page_size and actual_size != 0):
                flag = self.fill_page_full_hardDRive(top_page, end_page, page, physical_direction)
              
        else:
            raise NameError ("Empty Disk")
        
        return flag
    
    def fill_page_notFull_hardDrive(self, actual_size, page):
        index = 0
        while (index < actual_size):
            if(actual_size < self.page_size):
                page[index] = (self.structure_hardDrive[index])
                index += 1 
        return True    
           
    def fill_page_full_hardDRive(self, top_page, end_page, page, physical_direction):
        try:
            index = 0
            flag = False
            while (top_page < end_page and top_page >= physical_direction and 
            self.structure_hardDrive[top_page] != "-"):  # podría llenar con "-"
                page[index] = self.structure_hardDrive[top_page]
                top_page +=1
                index += 1
                flag = True
        except:
            raise NameError (" El disco no tiene esa posición de inicio de pagina")
            flag = False
        return flag

    # offset 0*12= 0
    def add_data_from_hardDrive_to_ram(self, physical_direction, victim_page, ID): # "-" if isn't necessary
        flag = False
        if (self.hardDrive_empty != True and len(self.structure_hardDrive) >= int(physical_direction)):
            page = self.make_new_page()
            # filling a page
            pageFlag = self.add_data_in_page(page, physical_direction)
            if (pageFlag != False):
                self.ram.add_to_ram(page, victim_page, ID)
                self.ram.find_in_ram(physical_direction, ID)
                flag = True
            else:
                raise NameError("Can't create a new page")
        else:  # si esta vacío no crea paginas
            raise NameError("The Disk is empty you can't create a new page")
        return flag

    def add_to_hardDrive(self, routing_data):  # inter: p2,puerto intra: C1-C2, puerto
        flag = False
        actual_data = "-"
        # separate the string in a array
        data = routing_data.split(",", len(routing_data))
        for indexHardDrive in range(self.hardDrive_size):
            if(self.structure_hardDrive[indexHardDrive]== "-" and flag!=True):
                for index in range(len(data)):
                    actual_data = data[index]
                    self.structure_hardDrive[indexHardDrive+index]= actual_data
                    flag = True
                indexHardDrive = self.hardDrive_size
        
        self.refresh_pageTable()
        return flag

    def refresh_pageTable(self) : # puede que  lo anterior no 
        ID_page = ""
        for index in range (self.hardDrive_size):
            if (self.structure_hardDrive[index] == "-"): #TODO salir?
                last_position = 0
                position = index
                if (position % 12 == 0): # si es mi primera posicion
                    last_position = index + self.page_size
                else: # si es otro indice que no es multiplo de 12
                    residue = position % self.page_size
                    position = position - residue
                    last_position = position + self.page_size
                while (position <= last_position-1):
                    if (position % 2 == 0 and self.structure_hardDrive[position] != "-"):
                        ID_page += self.structure_hardDrive[position] +","
                        position = position+2 #P1,P2,P3
                    elif (self.structure_hardDrive[position]=="-"):
                        break
                break
       
        self.pageTable.refresh_new_data(ID_page)

    def refresh_data_hardDrive(self,routing_data):
        flag = False
        data = routing_data.split(",", len(routing_data))
        for index in range (self.hardDrive_size):
            if (self.structure_hardDrive[index] == data[0]):
                data_index = 0
                while (data_index < len(data)) :
                    self.structure_hardDrive[index] = data[data_index]
                    index += 1
                    data_index += 1
                    flag = True
                    self.refresh_page(index, data)
                break
        return flag
    
    def refresh_page(self, position, data):
        page = False
        try:
            if (position % self.page_size == 0): #top of the page
                position = (position / self.page_size)-1
                page = self.ram.find_page_in_ram(position)
            else:
                residue = position % self.page_size
                position = position - residue
                position = (position / self.page_size)
                page = self.ram.find_page_in_ram(position)
            try:
                if (page != False) :
                    for index in range(0, self.page_size):
                        if(index % 2 == 0):
                            if (page[index] == data[0]):
                                data_index = 0
                                while (data_index < len(data)):
                                    page[index] = data[data_index]
                                    data_index += 1
                        index = index + 1
                    self.ram.replace_page_in_ram(position, page)
            except:
                raise NameError("The page isn't in the ram")
        except:
            raise NameError("The Disk is empty you can't create a new page")


    def hardDrive_empty(self):
        flag = True
        for index in range(self.hardDrive_size):
            if (self.structure_hardDrive[index] != None and flag != False):
                flag = False
                break
        return flag

    # the physical direction is an index
    def find_in_hardDrive(self, physicalDirection): # recibe un int 
        physicalDirection = int(physicalDirection)
        try:
            data = self.structure_hardDrive[physicalDirection]
        except:
            data = False
        return data
