# little structure for save data
# More easy to find the data
# parts of the pague table
# need a conexion with page table
# the data in tlb are in the page table? YES

import RAM
import PageTable


class TLB:
    # TODO check the size (25 bytes) ?
    
    def __init__(self, tlb_size, ram, page_size, pageTable):
        self.n_row = tlb_size
        # id | PRESENT/ ABSENT | PHYSICAL DIRECTION VIRTUAL PAGE (vector ram index)
        self.n_column = 3
        self.structure_tlb = self.make_structure_tlb()
        self.ram = ram
        self.page_size = page_size
        self.pageTable = pageTable

    def make_structure_tlb(self):
        structure = ["-"] * self.n_row
        for row in range(self.n_row):
            structure[row] = ["-"] * self.n_column
        return structure

    '''
    ID |  PRESENT/ ABSENT | PHYSICAL DIRECTION VIRTUAL PAGE
    0            1                2
    '''

    def find_in_tlb(self, virtualdirection):  # P1
        tlb_failure = True
        physicalDirection = ""
        extract_ID = ""
        for current_row in range(self.n_row):
            current_ID = self.structure_tlb[current_row][0]
            if (current_ID != "-"):
                extract_ID = self.extract_virtualDirection(current_ID, virtualdirection)
                # current ID es P1-P2-P3 buscar dentro de eso
                if (extract_ID == virtualdirection and len(virtualdirection) == len(extract_ID)):
                    self.check_presentAbsent(current_row, virtualdirection)
                    break
                elif (current_row == self.n_row-1 and tlb_failure == True): 
                    self.pageTable.find_in_pageTable(virtualdirection, self.page_size)
                    tlb_failure = True
                    break
            else: 
                 self.pageTable.find_in_pageTable(virtualdirection, self.page_size) 

        # the page table has not been used recently in that direction (CONNECTION)
        return tlb_failure
    
    def check_presentAbsent(self, current_row, virtualdirection):
         # present/absent IS THERE = 1
        ID = virtualdirection
        if (self.structure_tlb[current_row][1] == "1"):  # present
            # index is in the second
            physicalDirection = self.structure_tlb[current_row][2]
            self.ram.find_in_ram(physicalDirection, ID)
            tlb_failure = False
            print("TLB encontro direccion fisica y llego a Ram ")
        elif (self.structure_tlb[current_row][1] == "0"):  # absent
            self.pageTable.find_in_pageTable(virtualdirection)
            tlb_failure = False
            print("TLB no encontro dirección fisica y paso la busqueda a page Table")

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


    # data ["P1,P2,P3", "1", "4"]
    # if I don't have a victim page write: "-"
    def add_data_tlb(self, data, victim_page):
        flag = False
        if (self.full_tlb() == True):  # full
            flag = self.add_in_full_tlb(data, victim_page)
        else:  # not full
            flag = self.add_in_notFull_tlb(data, victim_page, flag)
        return flag  # return false if it can't be added

    def add_in_full_tlb(self, data, victim_page):
        for current_row in range(self.n_row):
            refresh_Flag = self.refresh_data(data, current_row)
            if (refresh_Flag == True):
                break

        if (refresh_Flag == False):
            if(victim_page != "-"):
                position = self.delete_victim_page(victim_page)
            else:
                position = self.n_row
                if (self.n_row > 1 ) :
                    position -= 1 # take the last 

            if (len(data) == self.n_column):
                for i in range(len(data)):
                    self.structure_tlb[position][i] = data[i]
                    flag = True
        return flag
    
    def add_in_notFull_tlb(self, data, victim_page, flag):
        if (len(data) == self.n_column):
            for current_row in range(self.n_row):
                current_ID = self.structure_tlb[current_row][0]
                if (flag != True):
                    if (current_ID == data[0]):
                        refresh_Flag = self.refresh_data(data, current_row)
                        flag = refresh_Flag
                    elif(current_ID == "-"):
                        for i in range(len(data)):
                            self.structure_tlb[current_row][i] = data[i]
                            flag = True
        return flag

    def full_tlb(self):  # if find a "-" in a column ID is not full
        flag = True
        for row in range(self.n_row):
            if (self.structure_tlb[row][0] == "-"):
                flag = False
        return flag

    def delete_victim_page(self, victim_page_ID):
        for current_row in range(self.n_row):
            actual_column = 0
            position = self.structure_tlb[current_row][actual_column]
            if (position == victim_page_ID):
                self.structure_tlb[current_row] = ["-"] * \
                    self.n_column  # put all the row in "-"
                new_position = current_row
        return new_position

    def refresh_data(self, data, current_row):
        flag = False
        current_ID = self.structure_tlb[current_row][0]
        if (current_ID == data[0]):
            for i in range(len(data)):
                self.structure_tlb[current_row][i] = data[i]
                flag = True
        return flag


