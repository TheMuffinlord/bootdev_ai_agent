from functions.get_files_info import *

test1 = get_files_info("calculator", ".")
print(test1)
print("====")
test2 = get_files_info("calculator", "pkg")
print(test2)
print("====")
try:
    test3 = get_files_info("calculator", "/bin")
    print(test3)
except Exception as whoops:
    print(whoops)
print("====")
try:
    test4 = get_files_info("calculator", "../")
    print(test4)
except Exception as whoops:
    print(whoops)
print("====")
print("if you see this it all worked")