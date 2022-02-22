import cv2
import mediapipe as mp
import time


class HandDetector():
  def __init__(self):
    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands()
    self.mpDraw = mp.solutions.drawing_utils
  
  def findHands(self, img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)
    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

    return img

  def findPosition(self, img, fingerNo):
    lmList = []
    if self.results.multi_hand_landmarks:
      for hand in self.results.multi_hand_landmarks:
        for id, lm in enumerate(hand.landmark):
          if id == fingerNo:
            h, w, ch = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h) ;#center coordinates
            lmList.append([cx, cy])
            cv2.circle(img, (cx, cy), 7, (255,0,255), cv2.FILLED)
    
    return lmList

  