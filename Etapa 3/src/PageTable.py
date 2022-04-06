# A larger structure to save frequent data

from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from _typeshed import self

import TLB
import RAM
import HardDrive


class PageTable:
    # STRUCTURE:
    # ID | VALUE| PRESENT/ ABSENT | REFRENCE BIT | MODIFIED BIT | PHYSICAL DIRECTION VIRTUAL PAGE (vector ram index)

    def __init__(self, pageTable_size, ram):
        self.row = pageTable_size
        self.column = 6
        self.ram = ram
        self.tlb = 0
        self.hardDrive = 0
        self.structure_pageTable = self.make_structure_pageTable()

    def make_structure_pageTable(self):
        structure_pageTable = [["-" for i in range(50)]for j in range(6)]
        return structure_pageTable

     # this method add new data to the page table
    def refresh_new_data(self, value):
        flag = 0
        for i in range(self.row):
            if flag == 1:
                break
            if(self.structure_pageTable[i][1] == "-"):
                self.structure_pageTable[i][1] = value
                self.structure_pageTable[i][0] = str(i)
                self.structure_pageTable[i][5] = "0"
                self.structure_pageTable[i][2] = "0"
                self.structure_pageTable[i][3] = "0"
                self.structure_pageTable[i][4] = "0"
                i = self.row
                flag = 1
                break
            else:
                i=i+1
        

    # this method split de value, to find de id to know if the id is the page table
    def find_split_words(self, value, searchWord):
        x = value.find(searchWord)
        if(x==-1):
            return False
        else:
            return True

   # this method return the physical address to ram
    def find_in_pageTable(self, value, pageSize):  # value P1
        physicalAddress = 0
        # offset is -1 when the value is not in the page table
        offset = "-1"
        id = 0
        pageName = "-"
       
        for i in range(len(self.structure_pageTable)):
            # search the value in the page table
            if self.find_split_words(self.structure_pageTable[i][1], value) == True:
                # compare if the present or absent bit is one (the bit exists)
                pageName = self.structure_pageTable[i][1]
                if self.structure_pageTable[i][2] == "1":
                    offset = i
                    id = value
                    physicalAddress = (int(offset)*pageSize)
                    # the reference bit is modified
                    self.structure_pageTable[i][3] = 1
                    self.ram.find_in_ram(self.structure_pageTable[i][5], value)
                    break
                # otherwise add the value in the page table
                else:
                    offset = i
                    physicalAddress = self.add_data_pageTable(pageSize, pageName, i)


    def add_data_pageTable(self, pageSize, value, newId):
        case1 = 0
        case2 = 0
        case3 = 0
        case4 = 0
        flag = False
        tlbNewPage = []
        victimPage = "-1"
        mostUsedPage = 0
        incompleteTableFlag = 0
        id = 0
        tlbNewPage = ["-" for i in range(3)]
        # algorithm NRU
        for i in range(len(self.structure_pageTable)):
            if self.structure_pageTable[i][3] == "-":
                incompleteTableFlag = i
            # search the victim page
            if self.structure_pageTable[i][3] == "0":
                if self.structure_pageTable[i][4] == "0":
                    #case 1 bit R, and bit M (0,0)
                    case1 = i
                else:
                    #case 2, bit R, and bit M (0,1)
                    case2 = i
            elif self.structure_pageTable[i][3] == "1":
                #case 3, bit R, and bit M (1,0)
                if self.structure_pageTable[i][4] == "0":
                    case3 = i
                else:
                    #case 4, bit R, and bit M (1,1)
                    case4 = i
       #Find victim page
        if(case1!=0):
            victimPage = self.structure_pageTable[case1][1]
            id = case1
            flag = True
        elif(case2!=0 and flag == False):
            victimPage = self.structure_pageTable[case2][1]
            id = case2
            flag = True
        elif(case3!=0 and flag == False):
            victimPage = self.structure_pageTable[case3][1]
            id = case3
            flag = True
        elif(case4!=0 and flag == False):
            victimPage = self.structure_pageTable[case4][1]
            id = case4
            flag = True

        flag = False
        #Find most used page
        if(case4!=0):
            mostUsedPage = case4
            flag = True
        elif(case3!=0 and flag == False):
            mostUsedPage = case3
            flag = True
        elif(case2!=0 and flag == False):
            mostUsedPage = case2
            flag = True
        elif(case1!=0 and flag == False):
            mostUsedPage = case1
            flag = True
        
        # make structure victim page for tlb
        tlbNewPage[0] = self.structure_pageTable[(mostUsedPage)][1]  # value
        tlbNewPage[1] = 1  # present or absent bit
        tlbNewPage[2] = str(mostUsedPage*pageSize)  # physicalAddress
        
        offset = newId*pageSize
        if(incompleteTableFlag != 0):
            victimPage = "-"

        else:
            self.structure_pageTable[int(victimPage)][3] = "1"
            self.structure_pageTable[int(victimPage)][4] = "1"
            self.structure_pageTable[int(victimPage)][5] = "1"

        self.tlb.add_data_tlb(tlbNewPage, victimPage)
        self.hardDrive.add_data_from_hardDrive_to_ram(offset, victimPage,value) # "-" if isn't necessary

# To refresh the page table data
    def refresh_data(self, data):  #id = value
        flag = 0
        for i in range(self.row):
            if flag == 1:
                break
                if(self.structure_pageTable[i][1] == data[0]):
                    self.structure_pageTable[i][2] = data[1]
                    self.structure_pageTable[i][3] = data[2]
                    self.structure_pageTable[i][4] = data[3]
                    self.structure_pageTable[i][5] = data[4]
                    i = self.row
                    flag = 1
                    break
                else:
                    i=i+1
        
