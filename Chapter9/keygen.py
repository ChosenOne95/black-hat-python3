# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:10:10 2019

@author: QIAN
"""
from Crypto.PublicKey import RSA

new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

print (public_key)
print (private_key)