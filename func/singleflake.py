import time
from typing import Optional


# 用于生成位随机ID，时间戳精度自定义，默认秒，起始时间2024年1月1日，每秒ID个数自定义，默认8位
class SingleFlake:
    def __init__(self, sequence_bits=3, accuracy=1):
        # 初始化序列号
        self.sequence = 0
        # 初始化时间戳精度
        self.accuracy = accuracy

        # 定义序列号的位数
        self.sequence_bits = sequence_bits

        # 计算每个部分的位移
        self.timestamp_left_shift = self.sequence_bits

        # 定义时间戳的起始点和序列号的掩码
        self.twepoch = 1704067200

        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        # 初始化最后一次生成ID的时间戳
        self.last_timestamp = -1


    def _til_next_second(self, last_timestamp: int) -> int:
        # 等待直到下一个秒
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def _time_gen(self) -> int:
        # 获取当前时间戳（秒）
        return int(time.time() * self.accuracy)

    def next_timestamp_part(self) -> int:
        # 生成时间戳部分
        timestamp = self._time_gen()

        if timestamp < self.last_timestamp:
            print(f"Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} seconds")
            return None

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._til_next_second(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        return (timestamp - self.twepoch) << self.timestamp_left_shift

    def next_sequence_part(self) -> int:
        # 生成序列号部分
        return self.sequence

    def next_id(self) -> Optional[int]:
        # 生成下一个ID
        timestamp_part = self.next_timestamp_part()
        sequence_part = self.next_sequence_part()

        if timestamp_part is None:
            return None

        return timestamp_part | sequence_part
