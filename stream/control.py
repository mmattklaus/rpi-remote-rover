import RPi.GPIO as GPIO
import termios
import sys, tty, time
import threading


class Car(object):
    def __init__(self, speed_steps=25):
        GPIO.setmode(GPIO.BOARD)

        self.EN_A = 7
        self.IN_1 = 11
        self.IN_2 = 12
        self.IN_3 = 13
        self.IN_4 = 15
        self.EN_B = 16

        self.DUTY_STEPPER = speed_steps
        self.speed = 50

    # def run(self):
    #     try:
    #         while True:
    #             print("looping")
    #             ch = getch()
    #             print("Choice: ", ch, type(ch))
    #             if ch in switcher():
    #                 switcher().get(ch, "0")()
    #             else:
    #                 invalid()
    #             time.sleep(0.5)
    #     except KeyboardInterrupt as k:
    #         self.reset()
    #     except:
    #         print("Exiting application")

    def init(self):
        GPIO.setup(self.EN_A, GPIO.OUT)
        GPIO.setup(self.IN_1, GPIO.OUT, initial=False)
        GPIO.setup(self.IN_2, GPIO.OUT, initial=False)
        GPIO.setup(self.IN_3, GPIO.OUT, initial=False)
        GPIO.setup(self.IN_4, GPIO.OUT, initial=False)
        GPIO.setup(self.EN_B, GPIO.OUT)

        self.pwma = GPIO.PWM(self.EN_A, 1000)
        self.pwmb = GPIO.PWM(self.EN_B, 1000)

        self.pwma.start(self.speed)
        self.pwmb.start(self.speed)

        return self

    # pwma.ChangeDutyCycle(0)
    # pwmb.ChangeDutyCycle(0)
    # stop()

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def invalid(self):
        print("Invalid response")

    def switcher(self):
        return {
            "8": self.forward,
            "4": self.left,
            "6": self.right,
            "2": self.backward,
            "1": self.speed_down,
            "3": self.speed_up,
            "5": self.stop,
            "\x1a": self.reset  # ctrl + z
        }

    def speed_up(self):
        self.speed += self.DUTY_STEPPER
        if self.speed > 100:
            self.speed = 100
        self.pwma.ChangeDutyCycle(self.speed)
        self.pwmb.ChangeDutyCycle(self.speed)
        print("Speed+: ", self.speed)

    def speed_down(self):
        self.speed -= self.DUTY_STEPPER
        if self.speed < 0:
            self.speed = 0
        self.pwma.ChangeDutyCycle(self.speed)
        self.pwmb.ChangeDutyCycle(self.speed)
        print("Speed-: ", self.speed)

    def forward(self):
        GPIO.output(self.IN_1, True)
        GPIO.output(self.IN_2, False)
        GPIO.output(self.IN_3, True)
        GPIO.output(self.IN_4, False)
        print("Forward")

    def backward(self):
        GPIO.output(self.IN_1, False)
        GPIO.output(self.IN_2, True)
        GPIO.output(self.IN_3, False)
        GPIO.output(self.IN_4, True)
        print("Backward")

    def left(self):
        GPIO.output(self.IN_1, False)
        GPIO.output(self.IN_2, True)
        GPIO.output(self.IN_3, True)
        GPIO.output(self.IN_4, False)
        print("Left")

    def right(self):
        GPIO.output(self.IN_1, True)
        GPIO.output(self.IN_2, False)
        GPIO.output(self.IN_3, False)
        GPIO.output(self.IN_4, True)
        print("Right")

    def stop(self):
        GPIO.output(self.IN_1, False)
        GPIO.output(self.IN_2, False)
        GPIO.output(self.IN_3, False)
        GPIO.output(self.IN_4, False)

    def reset(self):
        # pwma.stop()
        # pwmb.stop()
        GPIO.cleanup()

# try:
#     while True:
#         ch = getch()
#         print("Choice: ", ch, type(ch))
#         if ch in switcher():
#             switcher().get(ch, "0")()
#         else:
#             invalid()
#         time.sleep(0.5)
#
# except:
#     reset()
