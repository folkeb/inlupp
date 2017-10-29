# encoding:utf-8
import ast
import collections
import configparser
import random
import threading
import time


class AmusementException(Exception):
    """AmusementException is raised when bad happens to amusement."""

    def __init__(self, message, errors):
        """instantiated with a message of the couse, and a possiblity of saving errors for the record."""
        super(AmusementException, self).__init__(message)
        self.__errors = errors


class RideIsFullException(AmusementException):
    """RideIsFullException will be raised if the ride is full."""

    def __init__(self, message, errors):
        super(RideIsFullException, self).__init__(message, errors)

class InstantiationException(Exception):
    """InstantiationException is raised if object-instantiation fails."""
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(InstantiationException, self).__init__(message)
        # Now for your custom code...
        self.errors = errors


class IllegalArgumentException(Exception):
    def __init__(self, message):
        super(IllegalArgumentException, self).__init__(message)


class IllegalAgeException(IllegalArgumentException):
    """IllegalAgeException represents the state when an age lower than permitted is announced"""

    def __init__(self, message, errors):
        super(IllegalArgumentException, self).__init__(message)
        self.errors = errors


class LengthOutOfRangeException(IllegalArgumentException):
    """LengthOutOfRangeException represents the state when a length is outside the permitted interval"""

    def __init__(self, message, errors='no cause'):
        super(IllegalArgumentException, self).__init__(message)
        self.errors = errors


class DefaultProperties:
    FILE_NAME = './Folke_Bengtsson_3.props'  # '/Users/folkeb/PycharmProjects/inlupp/Folke_Bengtsson_3/Folke_Bengtsson_3.props'

    SOUNDS = {'child': ('oooh', 'wow', 'help'),
              'teen': ('boring', 'fuck yeah'),
              'adult': ('sweet Jesus',)}

    ABSOLUTE_MAX_LENGTH = 260
    ABSOLUTE_MIN_LENGTH = 50

    MIN_LENGTH = (ABSOLUTE_MIN_LENGTH, 80)
    MED_LENGTH = (81, 110)
    MAX_LENGTH = (111, ABSOLUTE_MAX_LENGTH)

    LENGTH_LIMITS = {'short': MIN_LENGTH,
                     'medium': MED_LENGTH,
                     'max': MAX_LENGTH}

    AGES = {'child': (0, 12), 'teen': (13, 19), 'adult': (20,)}


class Properties(object):
    __properties = None

    def __init__(self):
        """instantiation is done lazily, when asked for in method get_props(self). Probably a candidate for
         a Singleton/Borg design pattern.


        returns: Properties object"""
        self.__properties = self.get_config()

    def get_config(self):
        """calculates a config object that returns properties that are used
        returns: a config object with properties set"""
        if self.__properties is None:
            self.__properties = self.store_properties()
        return self.__properties

    def store_properties(self, property_file_name=DefaultProperties.FILE_NAME, default_properties=DefaultProperties):
        """creates a property object, stores it to a file and returns the properties as a config-object
        property_file_name: the name of the file to be saved
        default_properties: to be transparent which input is used.
        returns: a config-object"""

        config = configparser.ConfigParser()

        config['DEFAULT'] = {'MAX_LENGTH': DefaultProperties.ABSOLUTE_MAX_LENGTH,
                             'MIN_LENGTH': DefaultProperties.ABSOLUTE_MIN_LENGTH}

        config['child'] = {}
        child = config['child']
        child['sounds'] = str(default_properties.SOUNDS['child'])
        child['age'] = str(default_properties.AGES['child'])

        config['teen'] = {}
        teen = config['teen']
        teen['sounds'] = str(default_properties.SOUNDS['teen'])
        teen['age'] = str(default_properties.AGES['teen'])

        config['adult'] = {}
        adult = config['adult']
        adult['sounds'] = str(default_properties.SOUNDS['adult'])
        adult['age'] = str(default_properties.AGES['adult'])

        config['height'] = {}
        height = config['height']
        height['min'] = str(default_properties.MIN_LENGTH)
        height['med'] = str(default_properties.MED_LENGTH)
        height['max'] = str(default_properties.MAX_LENGTH)

        config['length_limits'] = {}
        length_limits = config['length_limits']
        length_limits['easy_ride'] = str(default_properties.LENGTH_LIMITS['short'])
        length_limits['comfy_ride'] = str(default_properties.LENGTH_LIMITS['medium'])
        length_limits['uneasy_ride'] = str(default_properties.LENGTH_LIMITS['max'])

        with open(property_file_name, 'w') as configfile:
            try:
                config.write(configfile)
            finally:
                configfile.flush()
                configfile.close()

        return config

    def get_length(self, length):
        """service method to get interval of a specific length
        length: the length in cm to be transformed to 'min', 'med' or 'max'
        returns: 'min', 'med' or 'max'
        exception: LengthOutOfRangeException is raised if length < 0 and > MAX_LENGTH (260CM)
        exception: ValueError for all arguments whose type are not int"""

        if length is None:
            raise ValueError('can not handle None as length')

        if not isinstance(length, int):
            raise ValueError('can not handle {:s} type expected <int> got {:s}'.format(str(type(length)), str(length)))

        max_length = self.__properties['DEFAULT'].getint('max_length')
        min_length = self.__properties['DEFAULT'].getint('min_length')

        if (length < min_length or length > max_length):
            raise \
                LengthOutOfRangeException \
                    ('value is outside interval <{0:d}:{1:d}> I got {2:d}'.format(min_length, max_length, length))

        store = dict()  # to be used as configparsers values are always strings - and i want to use tuples as datatype
        store['min'] = ast.literal_eval(self.__properties['height']['min'])
        store['med'] = ast.literal_eval(self.__properties['height']['med'])
        store['max'] = ast.literal_eval(self.__properties['height']['max'])

        for k, v in store.items():  # check whether the length is within the interval
            if v[0] <= length <= v[1]:
                return k  # the length is returned and its value can be used for checking

    def get_age(self, age):
        """method to compute age-interval given age, the interval is used in order to determine what sounds are to be uttered
        age: the age in whole years
        returns: 'child', 'teen' or 'adult'
        exception: IllegalAgeException is raised when age lower than 0 is given or if type differs from int."""
        if age is None:
            errorstring = "age is None, can not handle"
            raise IllegalArgumentException(errorstring)

        if not isinstance(age, int):
            errorstring = "age is of wrong type <{:s}>".format(age)
            raise IllegalAgeException(errorstring, age)

        child = ast.literal_eval(self.__properties['child']['age'])
        teen = ast.literal_eval(self.__properties['teen']['age'])
        adult = ast.literal_eval(self.__properties['adult']['age'])  # not used, but is anticipated in last else clause
        the_ret_vals = ('child', 'teen', 'adult')

        lowest_age = child[0]

        if age < lowest_age:  # there is no upper limit for age
            errorstring = "age is to low <{:d}>".format(age)
            raise IllegalAgeException(errorstring, age)

        if child[0] <= age and age <= child[1]:
            retval = the_ret_vals[0]
        elif teen[0] <= age and age <= teen[1]:
            retval = the_ret_vals[1]
        else:
            retval = the_ret_vals[2]
        return retval

    def get_sounds(self, age, fallback_value=['burrp']):
        """service method for returning the list of sounds for a specific age
        age: is one of 'adult', 'teen' or 'child', or a numeric value
        returns: a tuple of sounds expected from people in those ages, will act silent if no age is found - fallback is 'burrp'
        exception: IllegalArgumentException, is raised if type of age is not string or int or if age has a bad value"""

        ret_val = tuple(fallback_value)  # used if age can not be determined

        if age is None:
            raise IllegalArgumentException('can not determine:{:s}'.format(str(age)))

        if not (isinstance(age, str) or isinstance(age, int)):
            raise IllegalArgumentException('illegal argument: expected string or int: i got {:s}'.format(str(age)))

        if isinstance(age, str) and age in (
        'child', 'teen', 'adult'):  # must check instance if wrong age-string is given
            ret_val = ast.literal_eval(self.__properties[age]['sounds'])
        elif isinstance(age, int):
            try:
                ret_val = ast.literal_eval(self.__properties[self.get_age(age)]['sounds'])
            except IllegalAgeException as e:
                raise IllegalArgumentException(e.args)

        return ret_val


class Customer(threading.Thread):  # prop sen prop.getconfig?, pirrfaktor styr frekvens på skrik

    # datatype for preserving original arguments when invoked
    args = collections.namedtuple('args',
                                  ('cust_name',
                                   'cust_length',
                                   'cust_age',
                                   'properties'
                                   ))

    def __init__(self, name, length, age, properties):

        super(Customer, self).__init__()
        self.__args = Customer.args(cust_name=name,
                                    cust_length=length,
                                    cust_age=age,
                                    properties=properties)

        try:
            self.__customer_name = name
            self.__config = properties.get_config()
            self.__properties = properties
            self.__length = self.__properties.get_length(length)
            self.__age = self.__properties.get_age(age)
            self.__sounds = self.__properties.get_sounds(age)
            self.__shout_interval = 1  # will change depending on the amusements fear-factor
            self.__running = False  # set to true when starts running
            self.__instance = None  # holder of new instance of Customer immediately before start()

        except:
            raise InstantiationException('something went wrong', (name, length, age, properties))

    def new_instance(self):  # copy-constructor
        c = Customer(self.__args.cust_name,
                     self.__args.cust_length,
                     self.__args.cust_age,
                     self.__args.properties)
        return c

    def start(self):
        """overrides start() in Thread and forces return of a startable/runnable
        customer object when customer-thread is dead"""
        self.__instance = self.new_instance()
        super(Customer, self).start()

    def customer_name(self):
        return self.__customer_name

    def length(self):
        return self.__length

    def age(self):
        return self.__age

    def __str__(self):
        message = \
            'The {0:s} is named {1:s} and is of {2:s} height. {1:s} shouts \'{3:s}\'.' \
                .format(self.age(), self.customer_name(), self.length(), self.shout())
        return message

    def __set_shout_interval(self, value):
        self.__shout_interval = value

    def __random_sound(self):
        return random.choice(self.__sounds)

    def shout(self):
        return self.__random_sound()

    def buckle_up(self, amusement):
        """setter for frequence of customer shouting
        mutates the frequence of screams depending of the amusements fear factor"""
        new_frequence = 1 / amusement.fear_factor
        self.__set_shout_interval(new_frequence)
        return True

    def run(self):
        self.__running = True

        while (self.__running):
            try:
                time.sleep(self.__shout_interval)
            except InterruptedError as ie:
                print(ie)
            print(self.shout())

    def get_instance(self):  # copies and stores a copy
        if self.__instance is None:
            self.__instance = self.new_instance()
        return self.__instance

    def stop(self):
        self.__running = False
        return self.get_instance()


class Amusement(object):
    args = collections.namedtuple('args', ('fear_factor', 'min_length', 'config'))

    def __init__(self, fear_factor=3, min_length=120, config=Properties().get_config()):
        self.__args = Amusement.args(fear_factor, min_length, config)
        super(Amusement, self).__init__()
        self.__config = config
        self.__can_ride = self.permit_riders(min_length)
        self.__OPTIONS = {}

    def register_options(self, name):
        self.__OPTIONS.setdefault(name, 1 << len(self.__OPTIONS))

    def has_option(self, options, name):
        return bool(options & name)

    def fear_factor(self):
        fears = ast.literal_eval(self.__config['length_limits']['uneasy_ride'])
        lengths = list(ast.literal_eval(self.__config['height']['min']))
        lengths.append(ast.literal_eval(self.__config['height']['med']))
        lengths.append(ast.literal_eval(self.__config['height']['max']))
        print(lengths, fears)
        l = zip(lengths, fears)
        print(l)
        for e in l:
            print(e)
        l = zip(lengths, fears)

        for e in l:
            print(e)

    def permit_riders(self, min_length):
        pass
