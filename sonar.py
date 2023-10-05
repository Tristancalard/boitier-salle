import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER1 = 23
GPIO_ECHO1 = 24
GPIO_TRIGGER2 = 8
GPIO_ECHO2 = 25

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

#set personne count
personne = 0

def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def write_in_file():
    fichier = open("info_salle.txt", "w")
    fichier.write("Il y a {} personne dans la salle".format(personne))
    fichier.flush()
    fichier.close()

if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(GPIO_TRIGGER1, GPIO_ECHO1)
            dist2 = distance(GPIO_TRIGGER2, GPIO_ECHO2)
            if (dist1 < 20 and dist2 > 20):
                personne+=1
                write_in_file()
                time.sleep(1)
            else :
                if (dist2 < 20 and dist1 > 20):
                    personne-=1
                    write_in_file()
                    time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()