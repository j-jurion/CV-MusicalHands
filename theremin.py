import cv2 as cv
import math

from handdetector import HandDetector
from sound import Sound

cap = cv.VideoCapture(0)

hand = HandDetector()
sound = Sound()

def volume_map(volume):
  if volume > 200:
    return 10
  elif volume < 15:
    return 0
  return volume/200*10

def frequency_map(frequency):
  if frequency > 200:
    return 850
  elif frequency < 15:
    return 100
  return frequency/200*800+50

while True:
  success, img = cap.read()
  img = cv.flip(img, 1)
  hand.findHands(img)
  #f4 = hand.findPosition(img, 4)
  #f8 = hand.findPosition(img, 8)
  
  #TODO test
  frequency_handpos_4 = hand.findPosition(img, False, 4)
  frequency_handpos_8 = hand.findPosition(img, False, 8)
  volume_handpos_4 = hand.findPosition(img, True, 4)
  volume_handpos_8 = hand.findPosition(img, True, 8)
  #print(f"frequency:    {frequency_handpos}          |    volume:    {volume_handpos}")

  try: 
    cv.line(img, (frequency_handpos_4[0][0], frequency_handpos_4[0][1]), (frequency_handpos_8[0][0], frequency_handpos_8[0][1]), (0, 255, 0), thickness=3, lineType=8)
    frequency = math.sqrt((frequency_handpos_8[0][0] - frequency_handpos_4[0][0])**2 + (frequency_handpos_8[0][1] - frequency_handpos_4[0][1])**2)
  except IndexError:
    frequency = 0
    volume = 0
  try: 
    cv.line(img, (volume_handpos_4[0][0], volume_handpos_4[0][1]), (volume_handpos_8[0][0], volume_handpos_8[0][1]), (0, 255, 0), thickness=3, lineType=8)
    volume = math.sqrt((volume_handpos_8[0][0] - volume_handpos_4[0][0])**2 + (volume_handpos_8[0][1] - volume_handpos_4[0][1])**2)
  except IndexError:
    volume = 0



  #sound_param = [] ;#Frequency, volume
  frequency = frequency_map(frequency)
  volume = volume_map(volume)
  cv.putText(img, text=str("{:.2f}".format(frequency)), org=(500,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255,0,0),thickness=1)
  cv.putText(img, text=str("{:.2f}".format(volume)), org=(100,100), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0,0,255),thickness=1)

  if volume != 0:
    sound.play(frequency)

  cv.imshow('image', img)
  cv.waitKey(1)
  