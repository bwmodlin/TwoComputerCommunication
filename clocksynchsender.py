
import pigpio
import time

clockspeed = 1.0

GPIO_TRANSMITTER_NUMBER = 27
GPIO_RECEIVER_NUMBER = 26

def one_pulse(pi):
    print("one pulse")
    pi.write(GPIO_TRANSMITTER_NUMBER, 1)
    time.sleep(clockspeed)
    pi.write(GPIO_TRANSMITTER_NUMBER,0)
    time.sleep(clockspeed)

def header(pi, message):
    print("header")
    length = bin(len(message))[2:]
    if len(length) < 8:
        for i in range(8-len(length)):
            length = "0" + length

    for bit in length:
        pi.write(GPIO_TRANSMITTER_NUMBER, int(bit))
        time.sleep(clockspeed)

def send_message(pi, message):
    print("send message")
    for bit in message:
        pi.write(GPIO_TRANSMITTER_NUMBER, int(bit))
        time.sleep(clockspeed)

pi = pigpio.pi()
pi.write(GPIO_TRANSMITTER_NUMBER, 0)

message = input("What message do you want to send: ")

receiver_ready = False

def detect_response(a, b, c):
    print("detect response")
    global receiver_ready
    receiver_ready = True
    time.sleep(clockspeed)
    header(pi, message)
    send_message(pi, message)

pi.callback(GPIO_RECEIVER_NUMBER, pigpio.RISING_EDGE, detect_response)

while not receiver_ready:
    one_pulse(pi)
