README
====
Rewrite the ie_exfil.py with selenium package, cause many html labels in tumblr site
-----
have no id or name, we need find another way to locate them.
-----
Be careful about that the iedriver64 with IE11 have a bug that when using send_keys() 
----
to send english characters or number there have a lang pause whichabout 5 seconds between each char.
-----
Install a lower version of IE or use the iedriver32 instead may solve this problem.
----
Last, both of the two program are runing in the enviroment that the browser has already remembered the password. 
-----
mitb.py and cred_server.py is a group, and others belong to another.
