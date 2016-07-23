'''
Created on 23 Jul 2016

@author: professor
'''

from datetime import datetime
import math
import sys
import threading

from Data import Signal, State
from Sched import Sched
from custom_exceptions.Exceptions import VariableValueError

sys.path.append('..')


class Manager():
    """A Manager controls the activity of the intersection, and communicates with any Nodes using
    it. It is responsible for sending the correct signals to all Nodes.
    Every time a Manager receives an update from a Node, it recalculates its state, and replies to
    the Node with the correct signal.
    """
    def __init__(self, rotation_time, directions, comm_distance, speed_limit):
        self.rotation_time = rotation_time
        self.directions = directions
        self.comm_distance = comm_distance
        self.speed_limit = speed_limit
        self.node_times = {}
        self.time = 0
        self.index = 0
        self.current_direction = directions[0]
        self.current_direction.open()
        self.direction_lock = threading.Lock()


    def begin(self):
        if not self.directions:
            raise VariableValueError('variable \'directions\' cannot be None.')

        # Schedule the rotation timer for Directions
        self.timer = Sched(self.tick, None)
        self.timer.schedule(1000, 1000)


    def tick(self):
        """Increment the manager's time. Rotate the direction if the timer is exhausted.
        """
        self.time += 1
        self.calculate_weights()
        if not self.time % self.rotation_time:
            self.rotate()


    def rotate(self):
        """Rotate to the next Direction.
        In order, this performs: close, rotate, and open a Direction.
        """
        self.direction_lock.acquire()
        self.current_direction.close()
        self.index = (self.index + 1) % len(self.directions)
        self.current_direction = self.directions[self.index]
        self.current_direction.open()
        self.direction_lock.release()


    def calculate_weights(self):
        """Calculate the weight of the current direction according to each node's weight.
        """
        WEIGHT_PER_SECOND = 1  # TODO: This could go in Direction
        for d in self.directions:
            d.update_weight(WEIGHT_PER_SECOND)


    def print_directions(self):
        for d in self.directions:
            print (d)
        print('')


    def update(self, node):
        """ Called by a Node whenever it moves under a new panel. After processing its data, the
        Manager responds with a signal on the panel the Node is approaching. The weight of the
        Node's Direction is updated.

        Args:
            node: the calling Node.

        Returns:
            The current colour of the Direction. #TODO: return colours based on speed/comm distance
            Signal.INTERSECTION if the node has passed the final panel.
        """
        self.direction_lock.acquire()
        self.update_node_times(node)
        now, last = self.node_times[node.registration]

        panel = math.floor(node.distance)
        if panel == 0:
            # We can't do anything here. The first panel is only used to record the Node's initial
            # speed.
            self.direction_lock.release()
            return self.current_direction.colour

        print (node.direction, self.current_direction.direction)
        # TODO: Use the speed to see if the node can brake before the intersection.
        # This only matters if the light is green; when red, we can simply brake.
        speed = 1 / (last - now).total_seconds()


        light = None
        panel = math.floor(node.distance) + 1  # Find the next panel
        if node.direction == self.current_direction.direction:
            if panel >= self.comm_distance:
                light = Signal.INTERSECTION
            else:
                # TODO: this shouldn't always return green; if a Node cannot brake before the
                # intersection, it must receive a green light.
                if self.current_direction.state == State.CHANGING:
                    # TODO: Check if a Node can 'make it' in time. This may be complex.
                    pass
                light = Signal.GREEN
        else:
            light = Signal.RED
        self.direction_lock.release()

        return light


    def update_node_times(self, node):
        """"Extract a Node's now/last times for calculating its speed.

        Args:
            node: a Node to extract the data from.
        """
        last = 0
        now = datetime.now()
        times = self.node_times.get(node.registration)
        if times:
            last = times[0]
        self.node_times[node.registration] = (now, last)


