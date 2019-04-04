# import urllib2
import threading
import queue
import urllib
import urllib.parse
import urllib.error
import urllib.request

threads = 5
target_url = "https://www.jianshu.com"
wordlist_file = "/root/PycharmProjects/BHP3/Chapter5/dirbuster-ng/wordlists/small.txt"  # from SVNDigger
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"


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


def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # check to see if there is a file extension; if not, it's a directory
        # path we're bruting
        if ".".encode(encoding='utf-8') not in attempt:
            attempt_list.append("/{}/".format(attempt))
        else:
            attempt_list.append("/{}".format(attempt))

        # if we want to bruteforce extensions
        if extensions:
            for extension in extensions:
                # pass
                attempt_list.append("/{}{}".format(attempt, extension))

        # iterate over our list of attempts
        # print(attempt_list)
        for brute in attempt_list:
            brute_list = brute.split('\'')
            if len(brute_list) == 3:
                url = "{}/{}{}".format(target_url, brute_list[1], brute_list[2])
            elif len(brute_list) == 2:
                url = "{}/{}".format(target_url, brute_list[1])

            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                }
                req = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(req)
                if len(response.read()):
                    print("[{}] => {}".format(response.code, url))

            # except urllib.error as e:
            # if hasattr(e, 'code') and e.code != 404:
            # print( "!!! {} => %{}".format(e.code, url))
            except:
                # print("urllib error!")
                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php", ".bak", ".orig", ".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
    t.start()
