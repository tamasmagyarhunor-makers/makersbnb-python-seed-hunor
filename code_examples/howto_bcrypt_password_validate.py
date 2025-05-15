import bcrypt

# How to hash a password

plain_password = 'password12345'
print(plain_password)
byte_password = plain_password.encode('utf-8')
print(byte_password)
salt = bcrypt.gensalt()
print(salt)

hashed = bcrypt.hashpw(byte_password, salt)
print(hashed)

# How to check a hash

password_input = input().encode('utf-8')

if bcrypt.checkpw(password_input,hashed):
    print('Login Accepted')
else:
    print('Access Denied')