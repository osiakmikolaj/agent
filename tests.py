# from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

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
print("Result for 'main.py' file")
print(get_file_content("calculator", "main.py"))

# Test for 'pkg/calculator.py' file
print("Result for 'pkg/calculator.py' file")
print(get_file_content("calculator", "pkg/calculator.py"))

# Test for '/bin/cat' file
print("Result for '/bin/cat' file")
print(get_file_content("calculator", "/bin/cat"))
