'''
Created on 23 Jul 2016

@author: professor
'''

from threading import Thread

from Direction import Direction
from Manager import Manager
from NodeFactory import NodeFactory


class Main():
    def __init__(self):
        pass


    def begin(self):
        """ Initialise the Manager and any Nodes which shall use it.
        """
        directions = []
        dirs = ['UP', 'UPR', 'DOWN']  # , 'DOWNR', 'LEFT', 'LEFTR', 'RIGHT', 'RIGHTR']

        for d in dirs:
            directions.append(Direction(d, max_closed_time=10))

        # Initialise a Node
        node_factory = NodeFactory(dirs)
        node_factory.add_single(reg='AAAAAA', direction='UP')
        node = node_factory.get_nodes()[0]

        # Initialise the Manager
        manager = Manager(rotation_time=100, directions=directions, comm_distance=200, speed_limit=5)
        t = Thread(target=manager.begin)
        t.start()


        node.add_manager(manager)
        node.set_speed(2.0)
        node.travel()


if __name__ == '__main__':
    main = Main()
    main.begin()


