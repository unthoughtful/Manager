'''
Created on 17 Jun 2016

@author: professor
'''

from Data import Signal
from Data import State


class Direction:
    """"Contains all the information needed to describe a direction that a Node can travel.
    """

    def __init__(self, direction, max_closed_time, state=State.CLOSED, colour=Signal.RED, shared=[]):
        self.direction = direction  # Direction as a string
        self.state = state
        self.colour = colour
        self.max_closed_time = max_closed_time  # The maximum time before requesting to open
        self.opened_time = 0
        self.closed_time = 0
        self.node_count = 0
        self.weight = 0
        self.shared = shared  # Directions which can be safely open simultaneously


    def set_shared_directions(self, directions):
        """Append a series of Direction objects. The objects are preferred over the direction
        string for in case we wish to calculate the combined waiting time.
        """
        self.shared.append(directions)


    def open(self):
        """Open the direction.
        """
        self.state = State.OPEN
        self.colour = Signal.GREEN


    def close(self):
        """Close the direction.
        """
        self.state = State.CLOSED
        self.colour = Signal.RED


    def update_weight(self, multiplier):
        """Increase the weight for this Direction. This is updated by a Manager at specific time
        intervals so that a Direction's weight can increase over time.
        """
        self.weight = self.weight * multiplier


    def __str__(self):
        return 'direction=%s \tstate=%s \tweight=%s' % (self.direction, self.state, self.weight)




