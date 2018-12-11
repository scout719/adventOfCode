from threading import Thread
import functools

""" AUX FUNCTIONS """
class SignalCatchingError(Exception):
    """ Base class for exceptions in this module. """
    pass

HEAVY_EXERCISE = "nil (too computationally heavy)"
EXERCISE_TIMEOUT = 10000#3 #secs

def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [SignalCatchingError('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
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
        try:
            result = timeout(seconds_before_timeout=EXERCISE_TIMEOUT)(_globals[func_name])(read_input(year, day))
        except SignalCatchingError:
            result = HEAVY_EXERCISE
        print("Day {0}, part {1}: {2}".format(day, part, result))

def read_input(year, day):
    import os
    file_dir = os.path.dirname(os.path.realpath(__file__))
    with open("{0}/../{1}/input/day{2}".format(file_dir,year, day),"r") as fileReader:
        return [line.rstrip('\n') for line in fileReader]
