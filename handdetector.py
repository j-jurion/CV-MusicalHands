import cv2 as cv
import mediapipe as mp
import time


class HandDetector():
  def __init__(self) -> None:
    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands()
    self.mpDraw = mp.solutions.drawing_utils
  
  def findHands(self, img):
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)
    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

    return img

  def findPosition(self, img, leftHand: bool, fingerNo: int) -> list:
    if leftHand: handstr, coordinates, color = "L", (50,100), (0,0,255)
    else:  handstr, coordinates, color = "R", (450,100),(255,0,0)

    lmList = []
    if self.results.multi_hand_landmarks:
      hand = self.findHand(leftHand)
      if hand:
        cv.putText(img, text=handstr, org=coordinates, fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=3, color=color,thickness=3)
        for id, lm in enumerate(hand.landmark):
          if id == fingerNo:
            h, w, ch = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h) ;#center coordinates
            lmList.append([cx, cy])
            cv.circle(img, (cx, cy), 7, color, cv.FILLED)

    return lmList

  def findHand(self, left: bool):
    hands = self.results.multi_hand_landmarks

    # Only one hand detected
    if len(hands) == 1:
      if left:
        if hands[0].landmark[8].x > hands[0].landmark[20].x:
          return hands[0]
        else: return None
      else:
        if hands[0].landmark[8].x < hands[0].landmark[20].x:
          return hands[0]
        else: return None

    # Two hands detected
    else:
      if left:
        if hands[0].landmark[0].x < hands[1].landmark[0].x:
          return hands[0]
        else: return hands[1]
      else:
        if hands[0].landmark[0].x < hands[1].landmark[0].x:
          return hands[1]
        else: return hands[0]

  