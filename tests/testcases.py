import os

# check if the file 'gui.py' exists
def check_ui():
    if os.path.isfile("gui/gui.py"):
        print("Testcase: ui file exists" + "\033[92m" + " [OK]" + "\033[0m")
        return True
    else:
        print("Testcase: ui file exists" + "\033[91m" + " [FAIL]" + "\033[0m")
        return False


# check if there is a database
def check_db():
    if os.path.isfile("databases/test.db"):
        print("Testcase: database exists" + "\033[92m" + " [OK]" + "\033[0m")
        return True
    else:
        print("Testcase: database exists" + "\033[91m" + " [FAIL]" + "\033[0m")
        return False


# check if the 'config.json' file exists
def check_config():
    if os.path.isfile("config/config.json"):
        print("Testcase: config file exists" + "\033[92m" + " [OK]" + "\033[0m")
        return True
    else:
        print("Testcase: config file exists" + "\033[91m" + " [FAIL]" + "\033[0m")
        return False


# check if all the modules are installed
def check_modules():
    try:
        import os
        import sys
        import json
        import sqlite3
        from cryptography.fernet import Fernet
        from PyQt6 import QtCore, QtGui, QtWidgets
        print("Testcase: modules are installed" + "\033[92m" + " [OK]" + "\033[0m")
        return True
    except:
        print("Testcase: modules are installed" + "\033[91m" + " [FAIL]" + "\033[0m")
        return False


# check if the 'gui generation' file exists
def check_gui_generation():
    if os.path.isfile("gui/generate.sh"):
        print("Testcase: gui generation file exists" + "\033[92m" + " [OK]" + "\033[0m")
        return True
    else:
        print("Testcase: gui generation file exists" + "\033[91m" + " [FAIL]" + "\033[0m")
        return False


# execute all the test cases and return them in a list
def execute_testcases():
    result = []
    result.append(check_ui())
    result.append(check_db())
    result.append(check_config())
    result.append(check_modules())
    result.append(check_gui_generation())
    return result
