#!/usr/bin/env python 

# Created on January 18 2021
# @author: Simon Chamorro       simon.chamorro@usherbrooke.ca

"""
------------------------------------
Script to play Connect 4 against bot using camera only

"""

import cv2
import numpy as np 
from ConnectFour.GameBoard import GameBoard
from detect_board import BoardDetector
from ConnectFour.AIClass import AI


CAMERA_INDEX = 0


def main():
    board_detector = BoardDetector()
    bot = AI()
    bot.setDifficulty(6)

    print('Bot (RED) is ready to start.')

    idx = 0
    key = cv2.waitKey(0)
    while not key == ord('q'):

        img, board = board_detector.detect()
        if not board == None:
            game_board = GameBoard()
            game_board.board = board

            # Play bot's turn
            print('----------   ', idx, '   ----------')
            move = bot.playTurn(game_board)
            game_board.printBoard()
            print('Bot plays column ', move[1])

            # Check if winner
            bot_win = game_board.isWinner('X')
            player_win = game_board.isWinner('O')
            if bot_win:
                print('Bot Wins!')
            if player_win:
                print('Player Wins!')

            # Show output image
            cv2.imshow("img", img)

        key = cv2.waitKey(1)
        idx += 1
    
    board_detector.cap.release()
    cv2.destroyAllWindows() 

    
if __name__ == '__main__':
    main()