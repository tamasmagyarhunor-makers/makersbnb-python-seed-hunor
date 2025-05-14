import bcrypt
from salt import bcrypt_salt

password = '12345'.encode('utf-8')
print(password)
print(str(password))
salt = bcrypt_salt
print(salt)
hashed = bcrypt.hashpw(password,salt)
print(hashed)

# pass_to_check = input()
# pass_to_check = pass_to_check.encode('utf-8')

# # if bcrypt.checkpw(pass_to_check,hashed):
# #     print('Correct')
# # else:
# #     print('Wrong password')