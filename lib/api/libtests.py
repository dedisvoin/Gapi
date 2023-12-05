from colorama import (Fore, Style)
from typing import Callable
from time import time, sleep

def _test_passed(test_name: str, test_type, method: Callable,time,*args, **kvargs  ):
    
    try:
        string = Fore.BLACK + f'{test_type} Test:' +Fore.BLUE+ f' {test_name}' + f'( {method.__name__} )' + Fore.MAGENTA + f' args{args}' + f' kvargs{kvargs}' + Fore.RED + ' ... '  + Fore.GREEN + ' ok ' + Fore.RESET
    except:
        string = Fore.BLACK + f'{test_type} Test:' +Fore.BLUE+ f' {test_name}' + f'( {type(method)} )' + Fore.MAGENTA + f' args{args}' + f' kvargs{kvargs}' + Fore.RED + ' ... '  + Fore.GREEN + ' ok ' + Fore.RESET
    print('')
    print(Fore.GREEN + f"{'-'*(len(string)-30+1)}" + Fore.RESET)
    print(string+Fore.GREEN+'|'+Fore.LIGHTMAGENTA_EX+ f' time : {round( time, 2)}'+Fore.RESET+'s')
    print(Fore.GREEN + f"{'-'*(len(string)-30+1)}" + Fore.RESET)
    print('')

def _test_not_passed(test_name: str, test_type, method: Callable,time,*args, **kvargs  ):
    try:
        string = Fore.BLACK + f'{test_type} Test:' +Fore.BLUE+ f' {test_name}' + f'( {method.__name__} )' + Fore.MAGENTA + f' args{args}' + f' kvargs{kvargs}' + Fore.RED + ' ... '  + Fore.RED + ' err ' + Fore.RESET
    except:
        string = Fore.BLACK + f'{test_type} Test:' +Fore.BLUE+ f' {test_name}' + f'( {type(method)} )' + Fore.MAGENTA + f' args{args}' + f' kvargs{kvargs}' + Fore.RED + ' ... '  + Fore.RED + ' err ' + Fore.RESET
    print('')
    print(Fore.RED + f"{'-'*(len(string)-30+1)}" + Fore.RESET)
    print(string+Fore.RED+'|'+Fore.LIGHTMAGENTA_EX+ f' time : {round( time, 2)}'+Fore.RESET+'s')
    print(Fore.RED + f"{'-'*(len(string)-30+1)}" + Fore.RESET)
    print('')

class LibTestCase:
    def assertTrue(test_name_: str, __test__: bool | Callable,*args , **kvargs):
        if isinstance(__test__, Callable):
            st = time()
            value = __test__(*args, **kvargs)
            et = time()
            if value == True:
                _test_passed(test_name_,'AssertTrue', __test__,et-st, *args, **kvargs)
            else:
                _test_not_passed(test_name_,'AssertTrue', __test__,et-st, *args, **kvargs)
        else:
            if __test__ == True:
                _test_passed(test_name_,'AssertTrue', __test__,0, *args, **kvargs)
            else:
                _test_not_passed(test_name_,'AssertTrue', __test__,0, *args, **kvargs)
                
    def assertFalse(test_name_: str, __test__: bool | Callable,*args , **kvargs):
        if isinstance(__test__, Callable):
            st = time()
            value = __test__(*args, **kvargs)
            et = time()
            if value == False:
                _test_passed(test_name_,'AssertFalse', __test__,et-st, *args, **kvargs)
            else:
                _test_not_passed(test_name_,'AssertFalse', __test__,et-st, *args, **kvargs)
        else:
            if __test__ == False:
                _test_passed(test_name_,'AssertFalse', __test__,0, *args, **kvargs)
            else:
                _test_not_passed(test_name_,'AssertFalse', __test__,0, *args, **kvargs)
    
                

def test(a,b):
    l = []
    for i in range(a):
        l.append(i)
    sleep(1)
    return len(l) == b
        

LibTestCase.assertTrue('Value Test', test, 5000000, 5000000)
