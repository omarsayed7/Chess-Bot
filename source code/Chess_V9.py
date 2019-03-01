#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 12:20:44 2018

@author: omar
"""


import chess
import numpy as np 
import random
import chess.svg
import math
import copy
from IPython.display import SVG
from collections import Counter 

global white_history
global black_history
global a

global counter1
global counter2
global flat_board
global final_flat_board
global flatboardlist
a = 1


color = ''
egn = []
last = []
final = []
white_history = []
black_history = []
board = chess.Board()


def gethistory():  # make a list of white's moves and black's moves and store it as a history for the match
    white_history_moves = white_history
    black_history_moves = black_history
    total_number_moves = len(white_history_moves)+len(black_history_moves)
    return total_number_moves

def getPieces(board):  #get all white's and black's pieces during the match in list 
    flatboard = []
    ref_white_pieces = ['P','K','Q','N','R','B']
    ref_back_pieces = [x.lower() for x in ref_white_pieces]
    now_white_pieces = []
    now_black_pieces = []
    global now_board 
    now_board= str(board)
    for piece in now_board :
        if piece in ref_white_pieces :
            now_white_pieces.append(piece)
        elif piece in ref_back_pieces :
            now_black_pieces.append(piece)
    return now_white_pieces, now_black_pieces

def flatboard(board): #flatten the board into (1,64) vector contains the pieces in the game (updated) ,,, gridBoard convert the vector to 8*8 matrix
    global cc
    flat_board = []
    final_flat_board = []
    cc = 0
    for x in str(board):
        flat_board.append(x)
    
    for y in range(64) :
        final_flat_board.append(flat_board[cc])
        cc = cc + 2
        
    global gridBoard
    gridBoard = np.reshape(final_flat_board,(8,8))
    
    #print(final_flat_board)
    #print(cc)    
    return final_flat_board

def lookfor(board,piece = 'ALL',color= None):  #look for the pieces and get the coordinates of it in 8*8 matrix
    
    ref_white_pieces = ['P','K','Q','N','R','B']
    ref_back_pieces = [x.lower() for x in ref_white_pieces]
    ref_all_pieces = ref_white_pieces + ref_back_pieces
    lookfor_flatboard = flatboard(board)
    lookfor_flatboard = [lookfor_flatboard[0:63]]
    listoflocations = []

    if color == None and piece == 'ALL' : 
        for row in range(8):
            for col in range(8):
                if gridBoard[row][col] in ref_all_pieces:
                    x = col 
                    y = row 
                    listoflocations.append((x,y))

    elif color == None :
        for row in range(8):
            for col in range(8):
                if gridBoard[row][col] == piece:
                    x = col 
                    y = row
                    listoflocations.append((x,y))


    if color == 'white' and piece == 'ALL':
        for row in range(8):
            for col in range(8):
                if gridBoard[row][col] in ref_white_pieces:
                    x = col 
                    y = row 
                    listoflocations.append((x,y))

    elif color == 'black' and piece == 'ALL':
        for row in range(8):
            for col in range(8):
                if gridBoard[row][col] in ref_back_pieces:
                    x = col 
                    y = row 
                    listoflocations.append((x,y))

    return listoflocations

def getfrontposition(board,position,color):
    if color == 'white':
        x_cord = position[0]
        y_cord = position[1]
        if y_cord == 0 :
            pass
        else :
            y_cord = y_cord +1
        tupleposition = (x_cord,y_cord)

    elif color == 'black':
        x_cord = position[0]
        y_cord = position[1]
        y_cord = y_cord -1
        tupleposition = (x_cord,y_cord)
    return tupleposition

def SearchonBoardForBlocking(board,position,color):
    lookforAllBoard = lookfor(board,'ALL',color)
    getthePositionInFront = getfrontposition(board,position,color)
    if getthePositionInFront in lookforAllBoard:
        return True

    return False
    
def Evaluate(board):
    if isCheckmate(board,'white'):
        #Major advantage to black
        return -20000
    if isCheckmate(board,'black'):
        #Major advantage to white
        return 20000 
    getboard = getPieces(board)
    c = Counter(now_board)
    Q = c['Q']
    B = c['B']
    N = c['N']
    R = c['R']
    P = c['P']
    q = c['q']
    b = c['b']
    n = c['n']
    r = c['r']
    p = c['p']
    

    whiteMaterial =9*Q + 5*R + 3*N + 3*B + 1*P
    blackMaterial = 9*q + 5*r + 3*n + 3*b + 1*p
    numofmoves = gethistory()
    gamephase = 'opening'
    if numofmoves >40 or (whiteMaterial <14 and blackMaterial< 14):
        gamephase = 'ending'

    Dw = doubledPawns(board,'white')
    Db = doubledPawns(board,'black')
    Sw = blockedPawns(board,'white')
    Sb = blockedPawns(board,'black')
    Iw = isolatedPawns(board,'white')
    Ib = isolatedPawns(board,'black')
        
    evaluate1 = 900*(Q - q) + 500*(R - r) +330*(B-b)+320*(N - n) +100*(P - p)+-30*(Dw-Db + Sw-Sb + Iw- Ib)
    evaluate2 = pieceSquareTable(board,gamephase)
    #print('score',evaluate2)
    evaluation = evaluate2+evaluate1
    return evaluation

def pieceSquareTable(board,gamephase):
    score = 0
    flatboardlist = flatboard(board)
    #print(flatboardlist)
    for i in range(64):
        if flatboardlist[i] == '.':
            continue
        
        piecea = flatboardlist[i]
        if piecea == 'p' :
            sign = -1
            score += sign*pawn_table[i]
        elif piecea == 'n' :
            sign = -1
            score += sign*knight_table[i]
        elif piecea == 'b' :
            sign = -1
            score += sign*bishop_table[i]
        elif piecea == 'r' :
            sign = -1
            score += sign*rook_table[i]
        elif piecea == 'q' :
            sign = -1
            score += sign* queen_table[i]
        elif piecea == 'k' :
            sign = -1
            if gamephase == 'opening' :
                sign = -1
                score+=sign*king_table[i]
            else :
                sign = -1
                score+=sign*king_endgame_table[i]

        if piecea == 'P' :
            sign = +1
            score += sign*pawn_table[i]
        elif piecea == 'N' :
            sign = +1
            score += sign*knight_table[i]
        elif piecea == 'B' :
            sign = +1
            score += sign*bishop_table[i]
        elif piecea == 'R' :
            sign = +1
            score += sign*rook_table[i]
        elif piecea == 'Q' :
            sign = +1
            score += sign* queen_table[i]
        elif piecea == 'K' :
            if gamephase == 'opening' :
                sign = +1
                score+=sign*king_table[i]
            else :
                sign = +1
                score+=sign*king_endgame_table[i]
    return score

def doubledPawns(board,color): # returns the number of doubled pawns of the both  sides by checking the x axis and stor it in (temp list)
    if color =='white':
        listofpawns = lookfor(board,'P')
    elif color == 'black':
        listofpawns = lookfor(board,'p')
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else :
            temp.append(pawnpos[0])
                
    
                    
        return repeats

def blockedPawns(board,color): #returns the number of blocking pieces for both sides by checking the y axis and store it in blocked integer
    if color =='white':
        listofpawns = lookfor(board,'P')
    elif color == 'black':
        listofpawns = lookfor(board,'p')
    blocked = 0
    for pawnpos in listofpawns:
        if((color == 'white' and SearchonBoardForBlocking(board,pawnpos,'black')) or (color == 'black' and SearchonBoardForBlocking(board,pawnpos,'white'))):
            blocked = blocked +1 
    return blocked

def isolatedPawns(board,color):
    if color =='white':
        listofpawns = lookfor(board,'P')
    elif color == 'black':
        listofpawns = lookfor(board,'p')
    isolated = 0
    xlist = [x for (x,y) in listofpawns]
    for x in xlist:
        if x!=0 and x!=7:
            #For non-edge cases:
            if x-1 not in xlist and x+1 not in xlist:
                isolated+=1
        elif x==0 and 1 not in xlist:
            #Left edge:
            isolated+=1
        elif x==7 and 6 not in xlist:
            #Right edge:
            isolated+=1
    return isolated

def isCheckmate(board,color):
    if color == 'white' and board.turn:
        return board.is_checkmate()
    elif color == 'black' and not board.turn :
        return board.is_checkmate()
    elif color == 'white' and not board.turn :
        return False 
    elif color == 'black' and board.turn :
        return False







def negamax(board,depth,alpha,beta,color):
    if depth == 0 or board.is_game_over() :
        return color * Evaluate(board)

    maxVal = float('-inf')
    for move in board.legal_moves :
        temp_board = board.copy()
        temp_board.push(move)
        value = -negamax(temp_board,depth-1,-beta,-alpha,-color)
        print("nega",move,value)
        if value > maxVal :
            maxVal = value
        alpha = max(alpha,maxVal)
        if alpha >= beta :
            break
    return maxVal
        


            

        
        
        





    
pawn_table = [  0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]
knight_table =[-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-90,-30,-30,-30,-30,-90,-50]
bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-90,-10,-10,-90,-10,-20]
rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, 70, -5,-10,-10,-20]
king_table = [-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20]
king_endgame_table = [-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50]

if __name__ == "__main__":
    gameBoard = chess.Board()
    while True:
        print(gameBoard)
        print(gameBoard.legal_moves)
        userMove = raw_input("Enter the move you want to make: ")
        userMove = str(userMove)
        gameBoard.push_uci(userMove)

        if gameBoard.is_checkmate():
            print(gameBoard)
            print("User wins!")
            break
        elif gameBoard.is_game_over():
            print(gameBoard)
            print("Tie game")
            break

        minValue = float("inf")
        minMove = None
        print(gameBoard.legal_moves)
        for move in gameBoard.legal_moves:
            experimentBoard = gameBoard.copy()
            experimentBoard.push(move)
            value = negamax(experimentBoard, 3, float("-inf"), float("inf"), 1)
            print(move,minMove,value)

            if value < minValue:
                minValue = value
                minMove = move

        print("eval:",minValue)
        gameBoard.push(minMove)
        if gameBoard.is_checkmate():
            print(gameBoard)
            print("Computer wins")
            break
        elif gameBoard.is_game_over():
            print(gameBoard)
            print("Tie game")
            break


