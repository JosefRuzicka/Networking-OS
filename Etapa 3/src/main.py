import PageTable
import VirtualMemory
import TLB

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from _typeshed import self


def main():
    # self,ram_size, page_size, hardDrive_size, pageTable_size, tlb_size)
    virtualMemory_prov = VirtualMemory.VirtualMemory(32,12,128,40,12)
    virtualMemory_cant = VirtualMemory.VirtualMemory(80,12,256,50,25)

    print("-----------PROVINCIAL---------------")
    print()
    virtualMemory_prov.add_data("P1,8080-1,P2,8081-1,P3,8082-1")

    print(virtualMemory_prov.obtenerDatos("P2"))
    virtualMemory_prov.refresh_data_hardDrive("P1,8080-2")
    virtualMemory_prov.refresh_data_hardDrive("P3,8082-4")
    print(virtualMemory_prov.obtenerDatos("P1"))
    print(virtualMemory_prov.obtenerDatos("P3"))

    virtualMemory_prov.print_structures()

###########

    
    print("-----------CANTONAL---------------")
    print()
    virtualMemory_cant.add_data("C1-P1,6061,C2-C3,6062,C3-C4,6063,C3-C5,6064,C4-C6,6065")

    print(virtualMemory_cant.obtenerDatos("C1-P1"))
    virtualMemory_cant.add_data("C3-C8,6071,C9-C7,6070")
    print(virtualMemory_cant.obtenerDatos("C3-C8"))

    virtualMemory_cant.print_structures()
if __name__ == "__main__":
    main()