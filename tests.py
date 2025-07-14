# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python_file import run_python_file

# get_files_info tests

# Test for currecnt directory
# print("Result for current directory:")
# print(get_files_info("calculator", "."))

# Test for 'pkg' directory
# print("Result for 'pkg' directory")
# print(get_files_info("calculator", "pkg"))

# Test for './bin directory'
# print("Result for './bin' directory")
# print(get_files_info("calculator", "./bin"))

# Test for '../' directory
# print("Result for '../' directory")
# print(get_files_info("calculator", "../"))

# get_file_content tests


# Test for 'lorem.txt' (above 10k chars) file
# print("Result for 'lorem.txt' file")
# print(get_file_content("calculator", "lorem.txt"))

# Test for 'main.py' file
# print("Result for 'main.py' file")
# print(get_file_content("calculator", "main.py"))

# Test for 'pkg/calculator.py' file
# print("Result for 'pkg/calculator.py' file")
# print(get_file_content("calculator", "pkg/calculator.py"))

# Test for '/bin/cat' file
# print("Result for '/bin/cat' file")
# print(get_file_content("calculator", "/bin/cat"))


# Test for write_file.py

# Test for 'lorem.txt' with 'wait, this isn't lorem ipsum'
# print("Result for 'lorem.txt' and 'wait, this isn't lorem ipsum'")
# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

# Test for 'pkg/morelorem.txt' with 'wait, this isn't lorem ipsum'
# print("Result for 'pkg/morelorem.txt' and 'lorem ipsum dolor sit amet'")
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

# Test for 'lorem.txt' with 'this should not be allowed'
# print("Result for '/tmp/temp.txt' and 'this should not be allowed'")
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


# Tests for run_python_file

# Test for 'main.py' file
print("Result for 'main.py' file")
print(run_python_file("calculator", "main.py"))

# Test for 'tests.py'
print("Result for 'tests.py' file")
print(run_python_file("calculator", "tests.py"))

# Test for '../main.py'
print("Result for '../main.py' file")
print(run_python_file("calculator", "../main.py"))

# Test for 'nonexistent.py'
print("Result for 'nonexistent.py' file")
print(run_python_file("calculator", "nonexistent.py"))
