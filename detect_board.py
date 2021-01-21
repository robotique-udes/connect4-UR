#!/usr/bin/env python 

# Created on January 18 2021
# @author: Simon Chamorro       simon.chamorro@usherbrooke.ca

"""
------------------------------------
Script to detect Connect 4 board state with opencv

"""

import cv2
import numpy as np 
from ConnectFour.GameBoard import GameBoard


CAMERA_INDEX = 0



class BoardDetector():
    def __init__(self):
        # Create camera object
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        # Viz params
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.thickness = 2


    def detect(self):

        # Init board
        board = None

        # Capture frame
        ret, img = self.cap.read()

        # Make conversions 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Detect circles
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 4.5, minDist=60, minRadius=25, maxRadius=35)

        # Check if circles were found
        if circles is not None:     
            # Convert the (x, y) and r of the circles to int
            circles = np.round(circles[0, :]).astype("int")

            spots = []
            for idx, circle in enumerate(circles):
                (x, y, r) = circle
                chip = '-'

                # Create a mask for circle
                circle_mask = np.zeros((hsv.shape[0], hsv.shape[1]), np.uint8) 
                cv2.circle(circle_mask,(x, y), int(r*0.3), (255,255,255), -1) 
                avg_hsv = np.array(cv2.mean(hsv, mask=circle_mask)[0:3])

                red = self.is_red(avg_hsv)
                yellow = self.is_yellow(avg_hsv)
                blue = self.is_blue(avg_hsv)
                if blue:
                    continue

                c = (255,255,255) if (red or yellow) else (0,0,0)
                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), c, -1)
                if red:
                    chip = 'X'
                    cv2.putText(img, 'R', (x,y), self.font, self.font_scale, (0,0,0), self.thickness, cv2.LINE_AA)
                if yellow:
                    chip = 'O'
                    cv2.putText(img, 'Y', (x,y), self.font, self.font_scale, (0,0,0), self.thickness, cv2.LINE_AA)

                spots.append((x, y, chip))

        if len(spots) == 42:
            board = []
            spots = sorted(spots, key=lambda x: x[1])
            for i in range(6):
                row = sorted(spots[i*7:i*7+7], key=lambda x: x[0])
                board.append([r[2] for r in row])

        return img, board
            

    def is_red(self, hsv):
        lower_1 = np.array([0,60,50])
        upper_1 = np.array([10,255,255])
        
        lower_2 = np.array([170,60,50])
        upper_2 = np.array([180,255,255])
            
        range_1 =  (hsv >= lower_1).all() and (hsv <= upper_1).all()
        range_2 =  (hsv >= lower_2).all() and (hsv <= upper_2).all()

        return range_1 or range_1


    def is_yellow(self, hsv):
        lower_1 = np.array([20,120,70])
        upper_1 = np.array([40,255,255])
               
        range_1 =  (hsv >= lower_1).all() and (hsv <= upper_1).all()
        return range_1


    def is_blue(self, hsv):
        lower_1 = np.array([90,120,70])
        upper_1 = np.array([150,255,255])
               
        range_1 =  (hsv >= lower_1).all() and (hsv <= upper_1).all()
        return range_1



def main():
    board_detector = BoardDetector()

    key = 0
    idx = 0
    while not key == ord('q'):
        img, board = board_detector.detect()

        if not board == None:
            game_board = GameBoard()
            game_board.board = board
            print('----------   ', idx, '   ----------')
            game_board.printBoard()

        # Show output image
        idx += 1
        cv2.imshow("img", img)
        key = cv2.waitKey(0)
    
    board_detector.cap.release()
    cv2.destroyAllWindows() 

    
if __name__ == '__main__':
    main()