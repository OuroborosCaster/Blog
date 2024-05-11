from .standardflake import StandardFlake
from settings import NICKNAME_ENCODING
# 创建一个空列表来存储汉字
gbk = []

# 打开文件
with open('./func/gbk.txt', 'r', encoding='utf-8') as file:
    # 读取文件中的所有内容
    content = file.read()

for char in content:
    gbk.append(char)

# 昵称生成器
nickname_gen = StandardFlake()

encoding=NICKNAME_ENCODING

def convert_to_base_54(num):
    base_54_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if num == 0:
        return '0'
    result = []
    while num > 0:
        num, remainder = divmod(num, 54)
        result.append(base_54_chars[remainder])
    return ''.join(reversed(result))


def get_nickname():
    s = str(nickname_gen.next_id())
    if encoding == 'gbk':
        return ''.join([gbk[int(s[i:i + 4])] for i in range(0, 12, 4)])
    elif encoding == 'utf8':
        return ''.join(chr(int(s[i:i + 4]) + 19968) for i in range(0, 12, 4))
    elif encoding == 'ascii':
        return convert_to_base_54(s)
