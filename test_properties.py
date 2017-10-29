# file encoding:utf-8
import sys

sys.path.append('./')

from unittest import TestCase
import Folke_Bengtsson_3.Folke_Bengtsson_3 as fb3
import ast


class TestProperties(TestCase):
    def setUp(self):  # fresh setup inbetween invocations of test_ methods
        self.properties = fb3.Properties()
        self.config = self.properties.get_config()

    def test_properties_not_None(self):  # test that properties are created
        self.assertNotEqual(self.properties, None)

    def test_get_config(self):  # test that config is reachable and constructable
        self.assertNotEqual(self.config, None)

    def test_store_properties(self):  # test that properties are saved to a fil
        from pathlib import Path
        import os
        test_file = '/tmp/test.cfg'  # setup test_file

        self.properties.store_properties(test_file)

        expected = Path(test_file)
        self.assertTrue(expected.exists())

        # test that we still have value of our config-object after writing to file
        self.assertNotEqual(self.properties.get_config(), None, 'config can not be None')

        os.remove(expected)

    def test_get_length(self):  # testing that method get_length returns expected lengths regarding of cm
        p = self.properties  # initial configuration
        config = self.config

        min_length = config.getint('DEFAULT', 'min_length')
        max_length = config.getint('DEFAULT', 'max_length')
        STOP_INDEX = 1
        short_stop = ast.literal_eval(config['height']['min'])[STOP_INDEX]
        med_stop = ast.literal_eval(config['height']['med'])[STOP_INDEX]
        max_stop = ast.literal_eval(config['height']['max'])[STOP_INDEX]

        with self.assertRaises(fb3.LengthOutOfRangeException):  # testing that we handle negaive lengths
            p.get_length(min_length - 1)

        with self.assertRaises(fb3.LengthOutOfRangeException):  # testing that we reject lengths above limit
            p.get_length(max_length + 1)

        with self.assertRaises(ValueError):  # testing that we handle None-objects
            p.get_length(None)

        with self.assertRaises(ValueError):  # testing that we handle different types than string. and integer-classes
            p.get_length(object())

        expected = 'min'
        # testing that 'min' is returned for a specific interval
        for i in range(min_length, short_stop + 1):
            if i <= short_stop:
                actual = p.get_length(i)
                self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual:{:s}'.format(expected, actual))

        expected = 'med'
        # testing that 'med' is returned for interval inbetween 'min and max'
        for i in range(short_stop + 1, med_stop + 1):
            if i <= med_stop:
                actual = p.get_length(i)
                self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual:{:s}'.format(expected, actual))

        expected = 'max'
        # testing that 'max' is returned for interval over med'
        for i in range(med_stop + 1, max_stop + 1):
            if i <= max_stop:
                actual = p.get_length(i)
                self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual:{:s}'.format(expected, actual))

    def test_get_age(self):  # testing correct return value 'child'|'teen'|'adult depending on value of year
        p = self.properties  # initial configuration
        config = self.config
        START = 0  # lowest value in range for each category
        STOP = 1  # highest value in range for each category

        lowest_age = ast.literal_eval(config['child']['age'])[START]
        min_child_age = lowest_age
        max_child_age = ast.literal_eval(config['child']['age'])[STOP]
        min_teen_age = ast.literal_eval(config['teen']['age'])[START]
        max_teen_age = ast.literal_eval(config['teen']['age'])[STOP]
        adult_age_starts = ast.literal_eval(config['adult']['age'])[START]

        expected = 'child'
        for i in range(min_child_age, max_child_age + 1):
            actual = p.get_age(i)
            self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual{:s}'.format(expected, actual))

        expected = 'teen'
        for i in range(min_teen_age, max_teen_age + 1):
            actual = p.get_age(i)
            self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual{:s}'.format(expected, actual))

        expected = 'adult'
        for i in range(max_teen_age + 1, adult_age_starts ** 3, adult_age_starts ** 2):  # no need for small increments
            actual = p.get_age(i)
            self.assertEqual(expected, actual, 'can not differ expected:{:s}, actual{:s}'.format(expected, actual))

        with self.assertRaises(fb3.IllegalArgumentException):
            p.get_age(None)

        with self.assertRaises(fb3.IllegalAgeException):
            p.get_age(lowest_age - 1)

    def test_get_sounds(self):
        p = self.properties
        config = self.config
        START = 0
        STOP = 1
        lowest_age = ast.literal_eval(config['child']['age'])[START]
        min_child_age = lowest_age
        max_child_age = ast.literal_eval(config['child']['age'])[STOP]
        min_teen_age = ast.literal_eval(config['teen']['age'])[START]
        adult_age_starts = ast.literal_eval(config['adult']['age'])[START]

        ILLEGAL_NUMERICAL_AGE = -1
        NUMBER_OF_ADULTS = adult_age_starts * adult_age_starts

        with self.assertRaises(fb3.IllegalArgumentException):
            p.get_sounds(None)

        with self.assertRaises(fb3.IllegalArgumentException):
            p.get_sounds(config)

        with self.assertRaises(fb3.IllegalArgumentException):
            p.get_sounds(ILLEGAL_NUMERICAL_AGE)

        # could be gathered to a function for the three testcases - but i think more readable this way

        # assert 12 children, assert same set of sounds
        child_result = dict()  # dict for holding the test-results

        child_key = ast.literal_eval(config['child']['sounds'])  # the key whose counter should increase
        child_result[child_key] = 0  # which is instantiated to 0

        expected_child_dict = {child_key: max_child_age - min_child_age}  # the anticipated outcome of the test

        for age in range(min_child_age, max_child_age):  # count the number of sounds that is found for child
            child_result[p.get_sounds(age)] += 1
        self.assertEqual(expected_child_dict, child_result)  # assert the result visavi the prediction

        # assert 7 teens, assert same set of sounds
        teen_result = dict()  # the predicted result (sound and number) as above

        teen_key = ast.literal_eval(config['teen']['sounds'])
        teen_result[teen_key] = 0

        expected_teen_dict = {teen_key: adult_age_starts - min_teen_age}

        for age in range(min_teen_age, adult_age_starts):
            teen_result[p.get_sounds(age)] += 1
        self.assertEqual(expected_teen_dict, teen_result)

        # assert NUMBER_OF_ADULTS sharing the same set of sounds

        adult_result = dict()  # special case all adults are min 20 y o, no adult has a upper limit

        adult_key = ast.literal_eval(config['adult']['sounds'])

        expected_adult_dict = {adult_key: NUMBER_OF_ADULTS}
        adult_result[adult_key] = 0

        for age in range(adult_age_starts, NUMBER_OF_ADULTS + adult_age_starts):
            adult_result[p.get_sounds(age)] += 1
        self.assertEqual(expected_adult_dict, adult_result)

        # test for giving sounds on a string-parameter
        # the string is supposed to be one of "child", "teen" or "adult", if string is not found we will fallback

        teen_sounds = ast.literal_eval(config['teen']['sounds'])
        child_sounds = ast.literal_eval(config['child']['sounds'])
        adult_sounds = ast.literal_eval(config['adult']['sounds'])
        default_fall_back_sounds = ('burrp',)

        sound_set = frozenset({teen_sounds, child_sounds, adult_sounds, default_fall_back_sounds})

        ages = ('child', 'teen', 'adult', 'retired')

        for age in ages:
            result = p.get_sounds(age)
            self.assertTrue(result in sound_set)

        result = p.get_sounds('retired', ['yahoo'])  # one fallback value given by user
        self.assertEqual(result, ('yahoo',))  # expected tuple of one item

        result = p.get_sounds('retired', ['yahoo', 'tjoho'])  # two fallback values given by user
        self.assertEqual(result, ('yahoo', 'tjoho'))  # expected tuple of two items


import unittest

if __name__ == '__main__':
    unittest.main()
