import datetime, random, time,asyncio
from typing import Optional

#用于生成12位随机ID，时间戳精度秒，每秒8个ID
class StandardFlake:
    def __init__(self):
        self.sequence = 0
        self.sequence_bits = 3
        self.timestamp_left_shift = self.sequence_bits
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)
        self.last_timestamp = -1
        self.random_number = random.randint(0, 13600)
        self.last_date = datetime.datetime.now().date()
        self.last_time = datetime.datetime.now().replace(microsecond=0)



    def _til_next_second(self, last_timestamp: int) -> int:
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def _time_gen(self) -> int:
        now = datetime.datetime.now()
        if now.date() != self.last_date:
            self.random_number = random.randint(0, 13600)
            self.last_date = now.date()

        wait_time = now - self.last_time
        if wait_time < datetime.timedelta(seconds=1):
            now = datetime.datetime.now()

        self.last_time = now.replace(microsecond=0)
        seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        time_salt_number = str(int(seconds) + self.random_number).zfill(5)

        return int(now.strftime('%y%m%d') + time_salt_number)

    def next_timestamp_part(self) -> Optional[int]:
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
        return timestamp

    def next_sequence_part(self) -> int:
        return self.sequence

    def next_id(self) -> Optional[int]:

        timestamp_part = self.next_timestamp_part()
        sequence_part = self.next_sequence_part()

        if timestamp_part is None:
            return None

        return int(f"{timestamp_part}{sequence_part}")

