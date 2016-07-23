'''
Created on 23 Jul 2016

@author: professor
'''

from time import sleep

from Data import Signal


class Node():
    """A Node is a representation of a vehicle.
    """
    def __init__(self, registration, direction, speed=None, weight=None, priority=None):
        self.registration = registration
        self.direction = direction
        self.speed = speed
        self.weight = weight
        self.priority = priority
        self.distance = 0
        self.time_travelled = 0.0
        self.ACCELERATION = 2.5  # TODO: move to appropriate file

    def __str__(self):
        """The string representation of the object. It prints all the fields.

        Returns:
            a Node as a string.
        """
        return 'rego=%s \tdir=%s \tspeed=%s \tdistance=%s' % (self.registration, self.direction,
                                                              self.speed, self.distance)


    def add_manager(self, manager):
        self.manager = manager


    def set_speed(self, speed):
        """Set the speed in m/s.

        Args:
            speed in metres per second.
        """
        self.speed = speed


    def travel(self):
        """Begin communicating with the Manager. This occurs when the Node moves under the first
        panel. The Node will obey a series of colours that each panel will display, which tell it
        to accelerate or to decelerate. A Node will update the Manager with its state whenever it
        travels underneath a panel.
        A Node's behaviour is very simple: obey the panel colours, sleep until we reach the next
        panel, and then notify the Manager.
        """
        while True:
            self.last_speed = self.speed
            signal = self.manager.update(self)
            print ('signal:', signal)
            print ('before: %s' % self)

            # Signal is either: Green, Red or None. If None, it's the first panel, so do nothing.
            if signal == Signal.RED:
                self.decelerate()
                print('Red!')
            elif signal == Signal.GREEN:
                self.accelerate()
                print ('Green')
            elif signal == Signal.INTERSECTION:
                print ('Intersection', self.distance)  # TODO: implement.
            else:
                print 'What happened here?'

            ''' To simulate moving under the panels, the Node must sleep the amount of time it
            takes to travel between each panel.  '''
            distance = self.calculate_distance(self.speed, self.last_speed)

            if not distance:
                # We're stopped. Sleep for at most 0.3 seconds so we don't get "stuck".
                # TODO: arbitrary number
                distance = 3.0

            sleep_for = 1.0 / distance
            print ('Sleeping for', sleep_for)
            sleep(sleep_for)
            if self.speed:
                # Move to the next panel.
                self.distance += 1
            self.time_travelled += (sleep_for)
            print ('Travelled %sm in %ss' % (self.distance, self.time_travelled))
            print ('after: %s' % self)


    def decelerate(self):
        """Decelerate. Never allow a negative speed.
        """
        self.speed -= self.ACCELERATION
        if self.speed < 0:
            self.speed = 0


    def accelerate(self):
        """Accelerate. Never go above the speed limit.
        """
        self.speed += self.ACCELERATION
        if self.speed > self.manager.speed_limit:
            self.speed = self.manager.speed_limit


    def calculate_distance(self, final, initial):
        """Calculate the distance travelled using an initial speed, a final speed and acceleration.
        Note: the acceleration is treated as always being a constant.

        Args:
            final: final speed.
            initial: current speed.

        Returns:
            The distance travelled. Return 0 if we are stopped.
        """
        print final, initial
        if not final and not initial:
            return 0
        if final == initial:
            # No calculation - we aren't accelerating.
            return final

        distance = abs((float(final ** 2) - (initial ** 2)) / (2 * self.ACCELERATION))
        return distance


