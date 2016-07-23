'''
Created on 23 Jul 2016

@author: professor
'''

import random, string

from Node import Node
from custom_exceptions.Exceptions import DuplicateRegistrationError


class NodeFactory(object):
    def __init__(self, directions):
        self.directions = directions
        self.nodes = []


    def add_single(self, reg=None, direction=None):
        """Add a single Node to the list of Nodes.

        Args:
            reg: the Node's registration.
            direction: the Node's direction.
        """
        node = self.generate(reg, direction)
        try:
            self.add(node)
        except DuplicateRegistrationError as e:
            print '%s: Node was not added.' % e


    def add_many(self, regs=[], directions=[]):
        pass


    def generate(self, reg, direction):
        """Create a Node with a registration and a direction. If neither parameter is specified,
        generate random values for each.

        Args:
            reg: the Node's registration.
            direction: the Node's direction.

        Returns:
            A new Node.
        """
        if not reg:
            reg = self.gen_random_rego()
        if not direction:
            direction = self.gen_random_direction()

        return Node(reg, direction)



    def add(self, new_node):
        """Insert a Node to the list of Nodes. Ensure there are no duplicate registrations, and that
        insertion keeps the list sorted.

        Args:
            new_node: the Node to add to the existing list of Nodes.

        Raises:
            DuplicateRegistrationError: the Node's registration already exists in other Node.
        """
        for i, node in enumerate(self.nodes):
            if node.registration == node.reg:
                raise DuplicateRegistrationError('Registration %s already exists.' % node.reg)
            if node.registration > node.reg:
                self.nodes.insert(i, new_node)
                break
        else:
            self.nodes.append(new_node)


    def get_nodes(self):
        return self.nodes


    def print_nodes(self):
        print ('Nodes:')
        for i, node in enumerate(self.nodes):
            print ('  %d: rego-%s dir-%s' % (i, node.registration, node.direction))


    def gen_random_direction(self):
        num = random.randint(0, len(self.directions) - 1)
        return self.directions[num]


    def gen_random_rego(self):
        return self.gen_random_string(size=6, chars=string.ascii_uppercase + string.digits)


    def gen_random_string(self, size, chars):
        return ''.join(random.choice(chars) for _ in range(size))

