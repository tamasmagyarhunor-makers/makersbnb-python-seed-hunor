import bcrypt

# How to hash a password

plain_password = 'mypassword1234'
print(plain_password)

byte_password = plain_password.encode('utf-8')
print(byte_password)

salt = '$2b$12$n1GzTQLs1ukQAslENaCMbu'.encode('utf-8')
print(salt)

hashed = bcrypt.hashpw(byte_password, salt)
print(str(hashed))

# How to check a hash

password_input = input().encode('utf-8')

if bcrypt.checkpw(password_input,hashed):
    print('Login Accepted')
else:
    print('Access Denied')