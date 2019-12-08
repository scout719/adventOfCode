# pylint: disable=import-error
from threading import Thread
import functools
from timeit import default_timer as timer
import sys
import os
# pylint: enable=import-error

""" AUX FUNCTIONS """
class SignalCatchingError(Exception):
    """ Base class for exceptions in this module. """

HEAVY_EXERCISE = "nil (too computationally heavy)"
EXERCISE_TIMEOUT = 120  # secs

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            res = [SignalCatchingError('function [%s] timeout [%s seconds] exceeded!' %
                                       (func.__name__, seconds_before_timeout))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except BaseException as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

def execute_day(_globals, year, day, part):
    func_name = "day{0}_{1}".format(day, part)
    if func_name in _globals:
        start = timer()
        try:
            result = timeout(seconds_before_timeout=EXERCISE_TIMEOUT)(
                _globals[func_name])(read_input(year, day))
        except SignalCatchingError:
            result = HEAVY_EXERCISE
        end = timer()
        print("Day {0}, part {1}: {2} ({3:.3f} secs)".format(
            day, part, result, end - start))

def read_input(year, day):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    with open("{0}/../{1}/input/day{2}".format(file_dir, year, day), "r") as fileReader:
        return [line.rstrip('\n') for line in fileReader]

def main(argv_, globals_, year):
    start_day = None
    if len(argv_) > 1:
        try:
            if len(argv_) > 2:
                raise ValueError
            start_day = int(argv_[1])
        except ValueError:
            print("Usage: adventOfCode.py [<day>]")
            sys.exit(1)
    initial_day = 1
    end_day = 25
    if start_day is not None:
        initial_day = start_day
        end_day = start_day

    for day in range(initial_day, end_day + 1):
        execute_day(globals_, year, day, 1)
        execute_day(globals_, year, day, 2)
