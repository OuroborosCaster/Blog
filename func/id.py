from .standardflake import StandardFlake
from .singleflake import SingleFlake
from typing import Optional

# 用户ID生成器
uid_gen = SingleFlake()


def get_uid():
    return uid_gen.next_id()


# 评论ID生成器
cid_gen = SingleFlake(sequence_bits=12)


def get_cid():
    return cid_gen.next_id()


# 会话ID生成器
sid_gen = SingleFlake(sequence_bits=12, accuracy=1000)


def get_sid():
    return sid_gen.next_id()


# 博客ID生成器
bid_gen = StandardFlake()


def get_bid() -> Optional[str]:
    return bid_gen.next_id()
