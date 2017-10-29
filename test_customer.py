from unittest import TestCase

import Folke_Bengtsson_3.Folke_Bengtsson_3  as fb3


class TestCustomer(TestCase):
    CHILD_NAME = 'kim'
    TEEN_NAME = 'spook'
    ADULT_NAME = 'kaj'

    def setUp(self):
        self.properties = fb3.Properties()
        self.config = self.properties.get_config()
        self.child_customer = fb3.Customer(
            TestCustomer.CHILD_NAME, 55, 3, self.properties)
        self.teen_customer = fb3.Customer(
            TestCustomer.TEEN_NAME, 110, 16, self.properties)
        self.adult_customer = fb3.Customer(
            TestCustomer.ADULT_NAME, 185, 55, self.properties)

    def test_create(self):
        self.assertNotEqual(None, self.child_customer)
        self.assertNotEqual(None, self.teen_customer)
        self.assertNotEqual(None, self.adult_customer)

        with self.assertRaises(fb3.InstantiationException):
            fb3.Customer('foo', -1, 123, self.properties)
            fb3.Customer('foo', 123, -1, self.properties)
            fb3.Customer('foo', 123, 123, None)
            fb3.Customer('foo', 123, None, self.properties)
            fb3.Customer('foo', None, 123, self.properties)
            fb3.Customer(None, 123, 123, self.properties)

    def test_new_instance(self):
        cc = self.child_customer.new_instance()
        self.assertNotEqual(cc, self.child_customer, )
        cc = self.teen_customer.new_instance()
        self.assertNotEqual(cc, self.child_customer, )
        cc = self.adult_customer.new_instance()
        self.assertNotEqual(cc, self.child_customer, )

    def test_customer_name(self):
        self.assertEqual(TestCustomer.CHILD_NAME,
                         self.child_customer.customer_name())
        self.assertEqual(TestCustomer.TEEN_NAME,
                         self.teen_customer.customer_name())
        self.assertEqual(TestCustomer.ADULT_NAME,
                         self.adult_customer.customer_name())

    def test_length(self):
        self.assertEqual('min', self.child_customer.length())
        self.assertEqual('med', self.teen_customer.length())
        self.assertEqual('max', self.adult_customer.length())

    def test_age(self):
        self.assertEqual('child', self.child_customer.age())
        self.assertEqual('teen', self.teen_customer.age())
        self.assertEqual('adult', self.adult_customer.age())

    def test_shout_interval(self):
        self.assertEqual(1, self.teen_customer._Customer__shout_interval)

    def test_shout(self):
        import ast
        sounds = [e for e in ast.literal_eval(self.config['child']['sounds'])]
        for e in ast.literal_eval(self.config['teen']['sounds']): sounds.append(e)
        for e in ast.literal_eval(self.config['adult']['sounds']): sounds.append(e)

        for i in range(len(sounds) ** 2):
            self.assertTrue(self.child_customer.shout() in sounds)
            self.assertTrue(self.teen_customer.shout() in sounds)
            self.assertTrue(self.adult_customer.shout() in sounds)

    def test_buckle_up(self):
        class Amusement(object):
            def __init__(self):
                self.x = 0

            def fear_factor(self):
                self.x = self.x + 1
                return self.x

        mock_amusement = Amusement()
        for i in range(6, 1):  # 1 - 5
            self.teen_customer.buckle_up(mock_amusement)
            expected = 1 / i
            self.assertEqual(expected, self.teen_customer._Customer__shout_interval)

    def test_run(self):
        pass

    def test_start(self):
        customer = self.adult_customer
        customer._Customer__shout_intervalt = 0.01
        customer.start()
        try:
            customer.stop()
            customer.join()
        except Exception:
            self.fail('must not happen')
        self.assertFalse(customer.is_alive())

    def test_stop(self):
        customer = self.adult_customer
        customer._Customer__shout_interval = 0.01
        customer.start()
        try:
            result = customer.stop()
            customer.join()
        except Exception:
            self.fail('must not happen')

        self.assertEqual(result.customer_name(), customer.customer_name())
        self.assertEqual(result.length(), customer.length())
        self.assertEqual(result.age(), customer.age())
        self.assertNotEqual(result._Customer__shout_interval,
                            customer._Customer__shout_interval)
        self.assertTrue(result._Customer__instance is None)
        self.assertFalse(customer._Customer__instance is None)
        self.assertEqual(result, customer._Customer__instance)

        self.assertNotEqual(result, customer)

    def test_get_instance(self):
        orig_customer = self.adult_customer
        copy_customer = orig_customer.get_instance()

        self.assertEqual(copy_customer, orig_customer.get_instance())
        self.assertNotEqual(copy_customer, orig_customer)
