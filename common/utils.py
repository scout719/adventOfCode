# pylint: disable=import-error
from threading import Thread
import functools
from timeit import default_timer as timer
import sys
import os
# pylint: enable=import-error
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

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

            res = [SignalCatchingError(
                f'function [{func.__name__}] timeout [{seconds_before_timeout} seconds] exceeded!')]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except BaseException as e:  # pylint: disable=broad-except
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
    func_name = f"day{day}_{part}"
    if func_name in _globals:
        start = timer()
        try:
            timeout_secs = EXERCISE_TIMEOUT
            if sys.gettrace() is not None:
                # debugger attached
                timeout_secs = EXERCISE_TIMEOUT * 1000
            result = timeout(seconds_before_timeout=timeout_secs)(
                _globals[func_name])(read_input(year, day))
        except SignalCatchingError:
            result = HEAVY_EXERCISE
        end = timer()
        print(f"Day {day}, part {part}: {result} ({(end - start):.3f} secs)")

def read_input(year, day, is_sample=False):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    inputs_folder = "input/sample" if is_sample else "input"
    path = f"{file_dir}/../{year}/{inputs_folder}/day{day}"
    with open(path, "r", encoding="ascii") as fileReader:
        return [line.rstrip('\n') for line in fileReader]

def day_with_validation(globals_, YEAR, DAY, expected_result, part, data):
    func = globals_[f"day{DAY}_{part}"]
    if expected_result is not None:
        data_ex = read_input(YEAR, DAY * 100 + 1, True)
        result = func(data_ex)
        if result != expected_result:
            print(f"{bcolors.FAIL}FAIL")
            print(f"WAS: {result} SHOULD BE: {expected_result}")
            print(f"{bcolors.ENDC}")
            sys.exit(0)
        print(f"{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}")
    return func(data)

def main(argv_, globals_, year):
    sys.setrecursionlimit(9999)
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
