import bcrypt

# Test Salt

salt = '$2b$12$n1GzTQLs1ukQAslENaCMbu'.encode('utf-8')

# Production Salt

# salt = bcrypt.gensalt()

def hash_password(password):
    byte_password = password.encode('utf-8')

    hashed = bcrypt.hashpw(byte_password, salt)

    return hashed

def check_password(password,hash):
    byte_password = password.encode('utf-8')
    byte_hash = hash.encode('utf-8')
    return bcrypt.checkpw(byte_password,byte_hash)

