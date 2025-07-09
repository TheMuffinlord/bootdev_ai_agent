from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


test1 = get_file_content("calculator", "lorem.txt")
print(test1)
print("====")
test2 = get_file_content("calculator", "main.py")
print(test2)
print("====")
try:
    test3 = get_file_content("calculator", "pkg/calculator.py")
    print(test3)
except Exception as whoops:
    print(whoops)
print("====")
try:
    test4 = get_file_content("calculator", "/bin/cat")
    print(test4)
except Exception as whoops:
    print(whoops)
print("====")
print("if you see this it all worked")