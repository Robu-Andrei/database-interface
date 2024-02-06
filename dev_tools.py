import os
import sys
import json
import sqlite3
from cryptography.fernet import Fernet


def get_version():
    with open("config/version.txt", "r") as f:
        version = f.read()
        return version


# get the parameters from the 'config.json' file via the key argument
def get_parameter(key):
    with open("config/config.json", "r") as f:
        # load the json file
        data = json.load(f)
        return data[key]


def encrypt_password(password):
    # get the key from the json file
    key = get_parameter("key")
    encrypted_password = Fernet(key).encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    # get the key from the json file
    key = get_parameter("key")
    password = Fernet(key).decrypt(encrypted_password).decode()
    return password


# generate the key for encryption
def generate_key():
    key = Fernet.generate_key()
    print(key)
    return key