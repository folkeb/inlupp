# encoding:utf-8
import time


class InstantiationException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super(InstantiationException, self).__init__(message)
        # Now for your custom code...
        self.errors = errors


class Tickets(object):
    TICKET_NAME = 'ticket'

    def __add_ticket(self, ticket_name=TICKET_NAME):
        if ticket_name in self.__tickets:
            sum_of_tickets = self.__tickets[ticket_name]
            sum_of_tickets += 1
            self.__tickets[ticket_name] = sum_of_tickets
        else:
            self.__tickets[ticket_name] = 1

    def __init__(self, number_of_tickets=0):
        self.__tickets = dict()
        for each_ticket in range(number_of_tickets):
            self.__add_ticket(self)

    def use_ticket(self, ticket_name=TICKET_NAME):
        current_value = self.__tickets[ticket_name]
        new_value = 0 if current_value == 0 else current_value - 1
        self.__tickets[ticket_name] = new_value
        return True if current_value else False


class SafetyBox(object):  # the safetybox generates wallets
    def __init__(self):
        self.__stash = {}
        self.__stop = False

    def create_wallet(self, wallet_owner=None, wallet_content=None):
        while not self.__stop:
            the_wallet = Wallet(wallet_owner, wallet_content)
            self.__stash[the_wallet.user_wallet_id()] = the_wallet
            yield the_wallet

    def get_contents(self):
        return self.__stash if self.__stop else {}


class Wallet(object):
    def __init__(self, wallet_owner=None, wallet_content=None):
        """

        :type wallet_id: float
        """
        self.__user_wallet_id = None
        creation = time.clock()
        self.user_wallet_id(creation)


    @property
    def user_wallet_id(self):
        return self.__user_wallet_id

    @user_wallet_id.setter
    def user_wallet_id(self, value):
        if self.__user_wallet_id is None:
            self.__user_wallet_id = value
        else:
            raise InstantiationException('already instantiated', value)


    def __str__(self, ):
        return str(self.__user_wallet_id) + ':'

    @staticmethod
    def make_wallet(user_obj=None, ):
        pass


x = Wallet('folke', None )
print(x)
print(x.user_wallet_id())


class User(object):
    def __init__(self, user_name, user_length, user_wallet=Wallet(wallet_owner=None, wallet_content=None)):
        self.__user_name = user_name
        self.__user_length = user_length
        self.__user_wallet = user_wallet
        self.__user_wallet_id = time.clock()

    def make_user(self, user_name=None):
        pass


class Amusement(object):
    def __init__(self, attraction_name, attraction_characteristica, attraction_min_length,
                 user_characteristica=User.make_user('unknown'), ):
        self.__attraction_name = attraction_name  # namn på attraktionen t ex radiobil
        self.__attraction_characteristica = attraction_characteristica  # pirrfaktor
        self.__attraction_min_length = attraction_min_length  # minsta längd som tillåts åka
        self.__user_characteristica = user_characteristica  # användaren (vars längd är intressant)
        self.__user_can_ride = False

    @property
    def __user_can_ride(self):
        pass

    @__user_can_ride.setter
    def __user_can_ride(self, value):
        self.___user_can_ride = value
