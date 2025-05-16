from password_hashing_and_validation import *

password = 'test'

x = hash_password(password)

print(x)

hash='$2b$12$n1GzTQLs1ukQAslENaCMbu2iqxle6HjEp/1ly.OuXfBuZeY/hRs/y'

print(check_password('test',hash))