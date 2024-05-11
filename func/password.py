import hashlib
import random
import string


def sha256(salted_password):
    # 创建一个 SHA-256 哈希对象
    hash_object = hashlib.sha256()
    # 更新哈希对象
    hash_object.update(salted_password.encode('utf-8'))
    # 获取十六进制格式的哈希值
    hashed_password = hash_object.hexdigest()
    # 返回哈希值
    return hashed_password


def generate_salt():
    # 所有可能的字符
    all_chars = string.ascii_letters + string.digits + string.punctuation
    # 生成并打乱随机字符串
    salt = ''.join(random.choices(all_chars, k=16))
    return salt


def encrypt_password(password):
    salt = generate_salt()
    salted_password = password + salt
    hashed_password = sha256(salted_password)
    return hashed_password, salt


def verify_password(password, salt, hashed_password):
    return sha256(password + salt) == hashed_password
