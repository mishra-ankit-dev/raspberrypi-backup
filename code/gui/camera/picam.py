import picamera
from time import sleep

camera = picamera.PiCamera()
camera.rotation = 180
camera.start_preview()
sleep(5) # hang for preview for 5 seconds
camera.capture('/home/pi/Documents/cam/image.jpg')
camera.stop_preview()