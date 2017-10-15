#encoding:utf-8
import threading
import time

class Properties (object):
    class LoadProps(object):
        pass

    @staticmethod
    def get_sound(length):

        key = Properties.type_of_user(length)
        sounds = {'child': ('oooh', 'wow', 'help'), 'teen': ('boring', 'fuck yeah'), 'adult': ('sweet Jesus',)}
        return sounds[key]

    def type_of_user(length):
        return 'child' if length < 130 else 'teen' if length < 160 else 'adult'

class Customer(threading.Thread):

    def __init__(self, name, length, age):
        #super(Customer, self)
        super(Customer, self).__init__()
        self.__name = name
        self.__length = length
        self.__age = age
        self.__sounds = Properties.get_sound(length)
        self.__running = False

    def name(self):
        return self.__name

    def length(self):
        return self.__length

    def age(self):
        return self.__age

    def sound(self):
        return self.__sounds

    def __str__(self):
        return (str(self.name()) + ':' + str(self.length()) + ':' + str (self.age()) + ':' + str(self.sound()))

    def new_instance(self):
        c = Customer(self.__name, self.__length, self.__age)
        return c

    def shout_interval(self, value):
        self.__shout_interval = value

    def a_restartable_me(self):
        return self.new_instance()

    def run(self):
        self.__running = True
        while (self.__running):
            try:
                time.sleep(self.__shout_interval)
            except InterruptedError as ie:
                print(ie)

            #get_a_sound()
            print(self.__sounds)
            #sound()

    def stop(self):
        self.__running = False

        return self.a_restartable_me()

class Amusement (threading.Thread):
    def __init__(self):
        super.__init__()
        pass

c = Customer('foo', 185, 55)
print(c)
c.shout_interval(2/3)
c.start()
try:
    time.sleep(3)
except:
    print('interrupt')
print('stop')
c = c.stop()

c.shout_interval(1/3)
c.start()
try:
    time.sleep(3)
except:
    print('interrupt')
print('stop')

c = c.stop()


