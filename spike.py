# encoding:utf-8
class Celsius:
    def __init__(self, temp = 0):
        self._temperature = None
        self.temperature(temp)

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property
    def temperature(self):
        print("Getting value")
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        print("Setting value")
        self._temperature = value



class P:

    def __init__(self,x):
        self.__set_x(x)

    def __get_x(self):
        return self.__x

    def __set_x(self, x):
        if x < 0:
            # print ('<0')
            self.__x = 0
        elif x > 1000:
            #print ('>1000')
            self.__x = 1000
        else:
            #print ('-1 < x 1001')
            self.__x = x

    def __clean_x(self):
        print('goodbye')

    x = property(__get_x, __set_x, __clean_x)


class Q:

    def __init__(self,x):
        self.__x = property(self.get_x, self.__set_x, self.__clean_x)
        self.__set_x(x)

    def get_x(self) -> int:
        return self.__x

    def __set_x(self, x):
        if x < 0:
            #print ('<0')
            self.__x = 0
        elif x > 1000:
            #print ('>1000')
            self.__x = 1000
        else:
            #print ('-1 < x 1001')
            self.__x = x

    def __clean_x(self):
        print('goodbye')


for i in range(1000):
    q = Q(i-1)
    p = P(i-1)

import threading
import time


class Wait(threading.Thread):
    def __init__(self, time):
        threading.Thread.__init__(self)
        self.__time = time

    def run(self):
        try:
            time.sleep(self.__time)
        except InterruptedError as ie:
            print(ie)


import Folke_Bengtsson_3

x = Folke_Bengtsson_3.Wallet('folke', None)
sb = Folke_Bengtsson_3.SafetyBox
# wlt = sb.create_wallet('fb', {'ticket':4})
# print(wlt)
print(x.__class__)
print('wallet-id:', x.wallet_id)
Folke_Bengtsson_3__wallet_id = 12
print('wallet-id:', x.wallet_id)


def singleton(cls):
    return cls()


@singleton
class Foo(object):
    def bar(self):
        print('bar')


foo = Foo
foo.bar()
x = Foo.__class__.__new__(Foo.__class__)
print(x == Foo)
x.bar()
