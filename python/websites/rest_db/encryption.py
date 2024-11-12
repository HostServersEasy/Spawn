import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(13)
    hashed_password = bcrypt.hashpw(password.encode("UTF-8"), salt)
    return hashed_password.decode('utf-8')

def hash(info):
    salt = bcrypt.gensalt(13)
    hashed = bcrypt.hashpw(info.encode("UTF-8"), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("UTF-8"), hashed_password)

def check_hash(key:bytes, hashed_key:bytes):
    return bcrypt.checkpw(key, hashed_key)