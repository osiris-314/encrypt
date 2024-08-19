#!/usr/bin/env python3
import os
import sys
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

# Initialize Colorama
init()

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key(file_path):
    return open(file_path, "rb").read()

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        file_data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def encrypt_directory(directory_path, key, recursive=False):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
        if not recursive:
            break

def main():
    print(Fore.CYAN + "Select an option:" + Style.RESET_ALL)
    print("1 Encrypt a single file")
    print("2 Encrypt all files in a directory")
    print("3 Encrypt all files in a directory and its subdirectories")
    
    choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)

    if choice not in ['1', '2', '3']:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        sys.exit(1)

    path = input(Fore.GREEN + "Enter the path: " + Style.RESET_ALL)

    if not os.path.exists(path):
        print(Fore.RED + f"Error: The path {path} does not exist." + Style.RESET_ALL)
        sys.exit(1)

    print()
    print(Fore.CYAN + "Select a key option:" + Style.RESET_ALL)
    print("1. Generate a new key")
    print("2. Use an existing key")
    
    key_choice = input(Fore.GREEN + "Enter your choice (1/2): " + Style.RESET_ALL)

    if key_choice == '1':
        key = generate_key()
        print(Fore.GREEN + f"New key generated: {key.decode()}" + Style.RESET_ALL)
    elif key_choice == '2':
        key_path = input(Fore.GREEN + "Enter the path to the key file: " + Style.RESET_ALL)
        if not os.path.isfile(key_path):
            print(Fore.RED + f"Error: The key file {key_path} does not exist." + Style.RESET_ALL)
            sys.exit(1)
        key = load_key(key_path)
        print(Fore.GREEN + f"Key loaded from {key_path}: {key.decode()}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        sys.exit(1)

    if choice == '1':
        if os.path.isfile(path):
            encrypt_file(path, key)
            print(Fore.GREEN + f"File {path} encrypted successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: The path {path} is not a file." + Style.RESET_ALL)
    elif choice == '2':
        if os.path.isdir(path):
            encrypt_directory(path, key, recursive=False)
            print(Fore.GREEN + f"All files in directory {path} encrypted successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: The path {path} is not a directory." + Style.RESET_ALL)
    elif choice == '3':
        if os.path.isdir(path):
            encrypt_directory(path, key, recursive=True)
            print(Fore.GREEN + f"All files in directory and subdirectories {path} encrypted successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: The path {path} is not a directory." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error: Invalid choice." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
