import queue
import http
import threading
import os
import urllib
from urllib import request

threads = 10

target = "http://www.blackfire.mobi"
directory = "/root/PycharmProjects/BHP3/Chapter5/web_root/joomla-cms"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

web_paths = queue.Queue()

for r, d, f in os.walk("."):
    for file in f:
        # print(file)
        remote_path = "{}/{}".format(r, file)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(file)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        # print("go")
        # print(web_paths)
        # file = urllib.request.urlopen(target)
        path = web_paths.get()
        # print(path)
        # path = urllib.request.web_patchs.get()
        url = "{}{}".format(target, path)
        # print(url)
        #request = urllib.request.urlopen(url)

        try:

            response = urllib.request.urlopen(url)
            #response = urllib.urlopen(request)
            content = response.read()

            print("[{}] => {}".format(response.code, path))

            response.close()

        #except http.HTTPStatus as error:
            #print("Failed {}".format(error.code))
        except:
            pass


for i in range(threads):
    print("Spawning thread: {}".format(i))
    t = threading.Thread(target=test_remote)
    t.start()
