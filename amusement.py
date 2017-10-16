# encoding:utf-8
import threading
import time


class Properties(object):
    class LoadProps(object):
        pass

    @staticmethod
    def get_sound(length):
        key = Properties.type_of_user(length)
        sounds = {'child': ('oooh', 'wow', 'help'), 'teen': ('boring', 'fuck yeah'), 'adult': ('sweet Jesus',)}
        return sounds[key]

    @staticmethod
    def type_of_user(length):
        return 'child' if length < 130 else 'teen' if length < 160 else 'adult'


class Customer(threading.Thread):
    def __init__(self, name, length, age):
        # super(Customer, self)
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
        return (str(self.name()) + ':' + str(self.length()) + ':' + str(self.age()) + ':' + str(self.sound()))

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

            # get_a_sound()
            print(self.__sounds)
            # sound()

    def stop(self):
        self.__running = False
        return self.a_restartable_me()


class Amusement(threading.Thread):
    __passengers = list()

    def __init__(self, max_size, x_faxtor, run_time):
        super(Amusement, self).__init__()
        self.__max_size = max_size
        self.__x_factor = x_faxtor
        self.__run_time = run_time
        self.__is_full = len(self.__passengers) < self.__max_size
        self.__stop_running = False

    def get_passengers(self):
        if threading.current_thread().is_alive():
            return self.__passengers.copy()
        else:
            return self.disembark_ride()

    def disembark_ride(self):
        ret_val = list()
        for p in self.__passengers:
            ret_val.append(p.stop())
        self.__passengers = None
        return ret_val

    def add_passenger(self, a_passenger):
        if self.free_seats():
            a_passenger.shout_interval(1 / self.__x_factor)
            self.__passengers.append(a_passenger)
        else:
            print('ride is full, <', a_passenger, '> has to wait.')

    def free_seats(self):
        return self.__max_size - len(self.__passengers)

    def is_full(self):
        return len(self.__passengers) < self.__max_size

    def stop_running(self):
        self.__stop_running = True

    def start_running(self):
        self.__stop_running = False

    def is_running(self):
        return not self.__stop_running

    def run(self):
        self.start_running()
        self.__start_up_passengers()

        while self.is_running():
            try:
                time.sleep(1 / self.__x_factor)
                print(type(self).__name__)
                self.__run_time = self.__run_time - 1
                if self.__run_time < 0:
                    self.stop_running()
                    for p in self.__passengers:
                        p.stop()
            except InterruptedError:
                print('interrupted:', threading.current_thread())
            except KeyboardInterrupt:
                print('goodbye', threading.current_thread())

    def __start_up_passengers(self):
        for p in self.__passengers:
            p.start()

    def __str__(self):
        return (str(threading.current_thread().is_alive()))


class Carousel(Amusement):
    def __init__(self, max_size=4, x_faxtor=5, run_time=5):
        super(Carousel, self).__init__(max_size=4, x_faxtor=5, run_time=5)

    def __str__(self):
        return super().__str__()


class Nyckelpigan(Amusement):  # implement min-height
    def __init__(self):
        super(Nyckelpigan, self).__init__()
        pass


cc = Carousel()
print(cc)
customers = list()
customers.append(Customer('folke', 185, 55))
customers.append(Customer('fritjof', 150, 14))
customers.append(Customer('vidar', 125, 9))
customers.append(Customer('vidar', 125, 9))
customers.append(Customer('vidar', 125, 9))
customers[0].shout_interval(3 / 4)
customers[1].shout_interval(1 / 2)
customers[2].shout_interval(1 / 3)

for customer in customers:
    cc.add_passenger(customer)

cc.start()
cc.join()
print(cc.get_passengers())
list = cc.disembark_ride()
for elem in list:
    print(elem)
