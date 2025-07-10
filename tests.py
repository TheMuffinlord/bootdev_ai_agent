#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

try:
    test1 = run_python_file("calculator", "main.py")
    print(test1)
    t1p = True
except Exception as e:
    print(e)
    t1p = False
print("====")
try:
    test2 = run_python_file("calculator", "tests.py")
    print(test2)
    t2p = True
except Exception as e:
    print(e)
    t2p = False
print("====")
try:
    test3 = run_python_file("calculator", "../main.py")
    print(test3)
    t3p = True
except Exception as whoops:
    print(whoops)
    t3p = False
print("====")
try:
    test4 = run_python_file("calculator", "nonexistent.py")
    print(test4)
    t4p = True
except Exception as whoops:
    print(whoops)
    t4p = False
print("====")
if t1p and t2p and t3p and t4p:
    print("if you see this it all worked")
else:
    if not t1p:
        print("test 1 failed")
    if not t2p:
        print("test 2 failed")
    if not t3p:
        print("test 3 failed")
    if not t4p:
        print("test 4 failed")
