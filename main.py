import sys
import getopt
import pprint
from comp import Component
from link import Link
from port import Port
from model import Model
from example import daj

"""  Client(send) --- Channel(recv)*Channel(se) --- Server(recv)
        (send2) --- Channel2                                """

def main():

   #DFS
    explored = []
    behs = {}

    def dfs_visit(vert):

        print(vert.name, end="")
        explored.append(vert.name)
        connections = vert.get_connections()
        for con in connections.keys():
            if con.name not in explored:
                shared = connections[con].name + "" + connections[con].other.name
                if vert.beh is not None:
                    # Podmien nazwy akcji w body behavioura
                    vert.beh = vert.beh.replace(connections[con].name, shared)
                    behs[vert.name] = vert.beh
                    other_beh = connections[con].other.parent.beh
                    if other_beh is not None:
                        other_beh = other_beh.replace(connections[con].other.name, shared)
                        behs[connections[con].other.parent] = other_beh
                print("<" + shared + ">", end="")

                dfs_visit(con)

    dfs_visit(daj())
    print("\n")
    print("Printing behavioural definitions:\n")
    for procdef in behs:
        print(behs[procdef])
        print()

if __name__ == "__main__":
    main()
