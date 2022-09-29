import pigpio
import time

GPIO_TRANSMITTER_NUMBER = 27
GPIO_RECEIVER_NUMBER = 26

start_time = None
end_time = None

clock_time = None

pi = pigpio.pi()

pi.write(GPIO_TRANSMITTER_NUMBER, 0)

def detect_message(length):
    print("detect message")
    message = ""
    for i in range(length):
        message += str(1 - pi.read(GPIO_RECEIVER_NUMBER))
        time.sleep(clock_time)

    print(message)

def detect_header():
    print("detect header")
    length_message = ""
    for i in range(8):
        length_message += str(1 - pi.read(GPIO_RECEIVER_NUMBER))
        time.sleep(clock_time)

    detect_message(int(length_message, 2))


def send_confirmation():
    print("send confirmation")
    pi.write(GPIO_TRANSMITTER_NUMBER, 1)
    time.sleep(clock_time)
    pi.write(GPIO_TRANSMITTER_NUMBER,0)
    time.sleep(clock_time)
    detect_header()


def start_pulse_callback(a, b, c):
    global start_time
    start_time = time.perf_counter()
    print("start pulse callback")

def end_pulse_callback(a, b, c):
    print("end pulse callback")
    global end_time, clock_time
    end_time = time.perf_counter()
    clock_time = end_time - start_time
    time.sleep(clock_time)
    send_confirmation()


pi.callback(GPIO_RECEIVER_NUMBER, pigpio.FALLING_EDGE, start_pulse_callback)
pi.callback(GPIO_RECEIVER_NUMBER, pigpio.RISING_EDGE, end_pulse_callback)

while True:
    continue
