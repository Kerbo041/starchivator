import random
import time
import math
def generate_random_analog_value(start_of_interval, end_of_interval):
    length_of_interval = end_of_interval - start_of_interval
    return random.random() * length_of_interval + start_of_interval

def generate_walking_analog_value(start_of_interval, end_of_interval):
    raw_value = math.sin(time.time() * 2 * math.pi / 100)
    length_of_interval = end_of_interval - start_of_interval
    return  raw_value * length_of_interval + (start_of_interval + length_of_interval / 2)


def generate_random_signal():
    # signals = [b"\x08", b"\x50", b"\x30", b"\x1b"]
    signals = [b"\xff", b"\xff", b"\xff", b"\xff"]
    return signals[random.randint(0, len(signals) - 1)]

def generate_random_update_signal():
    # signals = [b"\xae", b"\xbc", b"\xbb", b"\xee"]
    # signals = [b"\xaa", b"\xaa", b"\xaa", b"\xaa"]
    signals = [b"\xa8", b"\xa8", b"\xa8", b"\xa8"]
    return signals[random.randint(0, len(signals) - 1)]

def generate_random_update_signal_many(i):
    # signals = [b"\xae", b"\xbc", b"\xbb", b"\xee"]
    signals = [b"\xaa", b"\xbb", b"\xcc", b"\xdd"]
    return signals[i]

def generate_random_discrete_value(length):
    value = random.randint(0, pow(2, length-1))
    return value