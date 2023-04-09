##
# Used this tutorial as reference to build a unit test framework:
# https://dev.to/azure/how-you-can-build-your-own-test-framework-in-python-using-decorators-2b00
##

import functools
import random
from Utils import TestError
import Common

##
# Imports functools, random, TestError from Utils and Common
#
# The "test" function is a decorator that wraps another function and
# catches any exceptions of the type "TestError". If such an exception is
# raised, the wrapper function returns False.
#
# The wrapped function is also added to a dictionary "eg" in
# a module "Common" with its name as the key.
##
def test(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except TestError as te:
            return False

    Common.eg[wrapper.__name__] = wrapper
    return wrapper

##
# The "runs" function is a part of a basic unit testing framework in Python.
# It takes a testName argument, which represents the name of a unit test to
# run. If the test name is not found in the "eg" dictionary in the "Common"
# module, the function simply returns.
#
# The function then seeds the random number generator with a value
# specified in the "seed" field of the "cfg" dictionary in the "Common"
# module. It creates a backup of the current values of all fields in the
# "cfg" dictionary, and sets the "status" variable to True.
#
# If the "dump" field of the "cfg" dictionary is True, the "out" variable
# is assigned the result of running the unit test associated with the given
# testName. Otherwise, the function tries to run the test and catch any
# exceptions that may occur. If an exception occurs, the "status" variable
# is set to False.
#
# The original values of the fields in the "cfg" dictionary are then
# restored, and a message indicating the status of the test is printed (e
# g. "PASS", "FAIL", or "CRASH"). The "status" variable is then returned.
##
def runs(testName):
    if testName not in Common.eg:
        return
    random.seed(Common.cfg['the']['seed'])
    old = {}
    for k, v in Common.cfg['the'].items():
        old[k] = v

    status = True
    if Common.cfg['the']['dump']:
        out = Common.eg[testName]()
    else:
        try:
            res = Common.eg[testName]()
            out = res
            status = res
        except:
            status = False

    for k, v in old.items():
        Common.cfg['the'][k] = v

    msg = ("PASS" if out else "FAIL") if status else "CRASH"
    if testName != 'ALL':
        testName = testName[3:]
    print("!!!!!!\t" + msg + "\t" + testName + "\t" + str(status))
    return status