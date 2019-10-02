import RPi.GPIO as GPIO
import termios
import sys, tty, time

GPIO.setmode(GPIO.BOARD)

EN_A = 7
IN_1 = 11
IN_2 = 12
IN_3 = 13
IN_4 = 15
EN_B = 16
GPIO.setup(EN_A, GPIO.OUT)
GPIO.setup(IN_1, GPIO.OUT, initial=False)
GPIO.setup(IN_2, GPIO.OUT, initial=False)
GPIO.setup(IN_3, GPIO.OUT, initial=False)
GPIO.setup(IN_4, GPIO.OUT, initial=False)
GPIO.setup(EN_B, GPIO.OUT)
pwma = GPIO.PWM(EN_A, 1000)
pwmb = GPIO.PWM(EN_B, 1000)

DUTY_STEPPER = 25
speed = 50
pwma.start(speed)
pwmb.start(speed)


# pwma.ChangeDutyCycle(0)
# pwmb.ChangeDutyCycle(0)
# stop()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def invalid():
    print("Invalid response")

def switcher():
    return {
        "8": forward,
        "4": left,
        "6": right,
        "2": backward,
        "1": speed_down,
        "3": speed_up,
        "5": stop,
        "\x1a": reset # ctrl + z
    }


def speed_up():
    global speed
    speed += DUTY_STEPPER
    if speed > 100:
        speed = 100
    pwma.ChangeDutyCycle(speed)
    pwmb.ChangeDutyCycle(speed)
    print("Speed+: ", speed)


def speed_down():
    global speed
    speed -= DUTY_STEPPER
    if speed < 0:
        speed = 0
    pwma.ChangeDutyCycle(speed)
    pwmb.ChangeDutyCycle(speed)
    print("Speed-: ", speed)


def forward():
    GPIO.output(IN_1, True)
    GPIO.output(IN_2, False)
    GPIO.output(IN_3, True)
    GPIO.output(IN_4, False)
    print("Forward")


def backward():
    GPIO.output(IN_1, False)
    GPIO.output(IN_2, True)
    GPIO.output(IN_3, False)
    GPIO.output(IN_4, True)
    print("Backward")


def left():
    GPIO.output(IN_1, False)
    GPIO.output(IN_2, True)
    GPIO.output(IN_3, True)
    GPIO.output(IN_4, False)
    print("Left")


def right():
    GPIO.output(IN_1, True)
    GPIO.output(IN_2, False)
    GPIO.output(IN_3, False)
    GPIO.output(IN_4, True)
    print("Right")


def stop():
    GPIO.output(IN_1, False)
    GPIO.output(IN_2, False)
    GPIO.output(IN_3, False)
    GPIO.output(IN_4, False)


def reset():
    # pwma.stop()
    # pwmb.stop()
    GPIO.cleanup()


try:
    while True:
        ch = getch()
        print("Choice: ", ch, type(ch))
        if ch in  switcher():
            switcher().get(ch, "0")()
        else:
            invalid()
        time.sleep(0.5)

except:
    reset()
