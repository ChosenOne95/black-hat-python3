# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:11:23 2019

@author: QIAN
"""
import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key =b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAs7RXkZdpnzK1ybre0ooS5rRByRnU6GHPoIhnHcT5lBrsFiFu\nu9kilu/zTcVKomFzoKsraOTLqD00RKlwr7O41CjUKJCt5CKGHOmdKOUEEzCis9Zk\nX0QUYnlwmHPx65GN0FC0OWuei7QpxRLNBOTbsLU6nve5X0AauPV6qY8mywZm7JrZ\nd5zjGE4jXBvy0cUxhhbhfGgju4JZ7xuYLTAttnJzouk4LiVWxwodnVcV/IufRnES\nQHdcNXa75oc7QIfb6GXqZhiQhehZOGsv06RAmhXgjGyVDKz7tOcI0ssOoXBSp+BS\nqNQaHipLf3LtqWsSeORYkGRrvR0q4RodTNU2fwIDAQABAoIBAAX7rSa1ydh5EcBj\nrmOIIVT5D2+oooQSLZ2ErRo6oqyhsNaTymIKurIXzxv5w6Bgaj8hM9LMO1Ogpgrb\nMVtIOpElwtqO5ps/4wM3a/oeleIlrmUacEETvTICJROOWLGlKPmUlkuLH747A2EC\nXT0aeY4KmqcMTGm1cq5RzgGzOHFt+NrgIbKKtx202wL+GQ5AmtiZNlzpCFCxLdX0\nNp4iomKwjpX3iCc1Yb28q16896Z/6QLkS3fMhvLlb6iMDMZR1/t/O3xzDgezPkVa\nkPI8Vqbx1yl4N0DJiskPpr24m/FryawgbcdY+lf0AIg0QzG8qey8/YoiRhAU5NcL\nCArPkXECgYEA1OZMHGwP+D2czVjZFO6+WsRH1tbFuHO6tWh+fGJjyIgVMR+iHyfn\n2t99Ooop7sk4frGr8f2QzjjcB2xL1TXLLufIJmB6F2Fk2GTjQYtZ6zRZJAxScm8c\nfPKi94sUNmS6l27HSh6yhzMMJwe8Dv5LAIqunorvU6VWDexowgKnO+MCgYEA2BWt\ntAys3ppnGm4hTnnx05DCuiYOrqgLZM20vahknr+8JGqgP+ORJD/20U+s/X7uwXR4\nWq1uU9ylqxfy+OM+ZnNzafRtJBye9dhcQFCWQU1GskHCSttrAHKrVd7nOKxu+Wog\njZxYSG0SWmmK06PeLIQKwO3HqrSk+yyNzCxs1bUCgYEAqk0uRO4MOD7Q11JjE+OG\nUYUBElHrB4lLqSFVTJpHx3lTul/bh6CcTvDHc7Rhpqk/j9j/+isjUlMZbraqUnsd\ndP/jkw9JmrpFuPO69gtKemL9i2Bv8yn+V9Sfl/SgzoH04H203Q2BMbUb23zMahHw\nXRaSaDArEXYISEr74XXN4JECgYEAqxDGelLKjFP6Kb9kGMeLfe0Na+bzGqwokP4V\nB0yHk/HAlafgA5Q59FO7J0uHbQwPIhH9sfO48yUr9n44OXdVkC/3/7qkqMELyx8l\nMTlbKolt3XMXyMFaPXmKUKntrT09gbDV4qYScgv/SpphcFk7a0yBYukbd/YY4kwM\nWcYVxz0CgYAghhwRwmePl1p0lrKsrH7d1sbmrME/w8SbJDa96RhDgwMInGj7umPM\n11Kdzvf/e77rVDZIJ5uREdi9LAAB4tKO0e6rmZBpK9fkQn1i//1+wuD1XbbO7eWW\n8ru3UqUYt7ghGc7cT9Ai0qrO0Eknv8+zWruJ0Fad1G0gBN4UYVoBbg==\n-----END RSA PRIVATE KEY-----'
rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

chunk_size = 128
offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset+chunk_size])
    offset += chunk_size

# now we decompress to original
plaintext = zlib.decompress(decrypted)

print (plaintext)
