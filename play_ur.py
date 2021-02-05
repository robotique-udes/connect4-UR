#!/usr/bin/env python 

# Created on February 1st 2021
# @author: Simon Chamorro       simon.chamorro@usherbrooke.ca

"""
------------------------------------
Script to play Connect 4 against UR5 bot using camera

"""

import cv2
import time
import rtde_io
import rtde_receive
import numpy as np 
from ConnectFour.GameBoard import GameBoard
from detect_board import BoardDetector
from ConnectFour.AIClass import AI


CAMERA_INDEX = 0


def check_board(board):
    occupation = [True, True, True, True, True, True, True]
    for i in range(6):
        for column in range(7):
            if board[5-i][column] != '-':
                if not occupation[column]:
                    return False
                occupation[column] = True
            else:
                occupation[column] = False
    return True


def count_chips(chip, board):
    count = 0
    for c in board:
        count += c.count(chip)
    return count


def main():
    # Create rtde objects to communicate with UR5
    rtde_io_ = rtde_io.RTDEIOInterface("169.254.151.102")
    rtde_receive_ = rtde_receive.RTDEReceiveInterface("169.254.151.102")

    # Create board detector and bot
    board_detector = BoardDetector()
    bot = AI()
    bot.setDifficulty(6)

    # Wait for user to be ready
    print('Bot (RED) is ready')
    print('Game started')
    done = False
    num_red_chips = 0
    num_yellow_chips = 0
    first_red_pass = False
    first_yellow_pass = False
    while not done:
        img, board = board_detector.detect()
        game_board = GameBoard()
        game_board.board = board

        # Pass if no board detected
        if board == None:
            continue

        # Check if board is legit
        legit_board = check_board(board)
        if not legit_board:
            continue

        # Check if bot played
        red_chips = count_chips('X', board)
        if red_chips == num_red_chips + 1 or not first_red_pass:
            first_red_pass = True
            num_red_chips = red_chips
            
            # Check if bot wins
            game_board.printBoard()
            bot_win = game_board.isWinner('X')
            if bot_win:
                print('Bot wins!')
                done = True
                continue

        # Check if opponent played
        yellow_chips = count_chips('O', board)
        if yellow_chips == num_yellow_chips + 1 or not first_yellow_pass:
            first_yellow_pass = True
            num_yellow_chips = yellow_chips

            # Check if player wins
            player_win = game_board.isWinner('O')
            if player_win:
                print('Opponent wins!')
                done = True
                continue

            # Play bot's turn
            print('Bot is playing')
            move = bot.playTurn(game_board)
            game_board.printBoard()

            # Send command to UR
            print('Bot plays column ', move[1])
            column = move[1] + 1
            rtde_io_.setStandardDigitalOut(column, True)
            time.sleep(0.5)
            rtde_io_.setStandardDigitalOut(column, False)

        # Show image
        cv2.imshow("img", img)

        # Check if user wants to quit
        key = cv2.waitKey(10)
        if key == ord('q'):
            done = True
    
    board_detector.cap.release()
    cv2.destroyAllWindows() 

    
if __name__ == '__main__':
    main()