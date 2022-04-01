import cv2
import mediapipe as mp
import math

class HandDetector:
    
    def __init__(self, mode=True, maxHands=2, detectionCon=0.5, minTrackCon=0.5, model_complexity=0):
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.model_complexity = model_complexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.minTrackCon,
            model_complexity=self.model_complexity
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.tipIds = [4, 8, 16, 20]
        self.fingers = []
        self.lmList = []



    def findHands(self, img, draw=True, flipType=True):
        
        img.flags.writeable = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        img.flags.writeable = True
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        allHands = []
        h, w, c = img.shape

        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}

                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)
                

                if draw:
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, myHand):

        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1) 
                else:
                    fingers.append(0)
            
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers


    def findDistance(self, p1, p2, img=None):

        x1, y1 = p1 
        x2. y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (X1 , Y1 , X2 , Y2 , cx , cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info 

    
    def main():
        cap = cv2.VideoCapture()
        detector = HandDetector(detectionCon=0.5, maxHands=2)
        while True:
            success, img = caap.read()
            hands, img = detector.findHands(img)

            if hands:

                hand1 = hands[0]
                lmList1 = hand1["lmList"]
                bbox1 = hand1["bbox"]
                centerPoint1 = hand1["center"]
                handType1 = hand1["type"]

                fingers1 = detector.fingersUp(hand1)



                if len(hands) == 2:
                    hand2 = hands[1]
                    lmList2 = hand2["lmList"]
                    bbox2 = hand2["bbox"]
                    centerPoint2 = hand2["center"]
                    handType2 = hand2["type"]

                    fingers2 = detector.fingersUp(hand2)

                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)
            
            cv2.imshow("HTM", img)
            cv2.waitKey(1)
if __name__ == "__main__":
    main()
