import copy
import datetime
import sys
class Team68():
    def __init__(self):
        self.infinity=10000000000
        self.board=[]
        self.maxDepth=0
        self.timeLimit=datetime.timedelta(seconds=15)
        self.startTime=0
        self.gameOver=False
        self.lastWinner='-'
        self.count=0
        self.transposition={}
    def checkDiam(self,player,opp,ind1,ind2,baseVal,bs):
      heur = 0
      countForDiam = {}
      countForDiam[player] = 0
      countForDiam[opp] = 0
      countForDiam['-'] = 0
      countForDiam['d'] = 0
      for i in range(0,4):
          countForDiam[bs[ind1[i]][ind2[i]]] = countForDiam[bs[ind1[i]][ind2[i]]] + 1
      if countForDiam[opp] == 0  and countForDiam[player] != 0 and countForDiam['d'] == 0:
              heur += baseVal**countForDiam[player]
      if countForDiam[player] == 0 and countForDiam[opp] != 0 and countForDiam['d'] == 0:
              heur -= baseVal**countForDiam[opp]
      return heur

    def calcHeuristicBlock(self,ply,opp,x,y):
        # calculate the heuristic of the given board state
        bs = self.board.board_status # This has to return the current smallblock somehow
        baseVal = 16    # The value which will the base for the exponent
        currHeur = 0
        for i in range(4):
            countPlyRow=0
            countPlyCol=0
            countOppRow=0
            countOppCol=0
            for j in range(4):
                if(bs[4*x+i][4*y+j]==ply):
                    countPlyRow+=1
                elif bs[4*x+i][4*y+j]==opp:
                    countOppRow+=1
                if(bs[4*x+j][4*y+i]==ply):
                    countPlyCol+=1
                elif bs[4*x+j][4*y+i]==opp:
                    countOppCol+=1
                
            if countPlyRow != 0 and countOppRow == 0:
                currHeur += baseVal**countPlyRow
            elif countOppRow != 0 and countPlyRow == 0:
                currHeur -=  baseVal**countOppRow

            if countPlyCol != 0 and countOppCol == 0:
                currHeur += baseVal**countPlyCol
            elif countOppCol != 0 and countPlyCol == 0:
                currHeur -=  baseVal**countOppCol
        # checking diamonds
        ind1 = [4*x+1,4*x+0,4*x+2,4*x+1]
        ind2 = [4*y+0,4*y+1,4*y+1,4*y+2]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [4*x+1,4*x+0,4*x+2,4*x+1]
        ind2 = [4*y+1,4*y+2,4*y+2,4*y+3]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [4*x+2,4*x+1,4*x+3,4*x+2]
        ind2 = [4*y+0,4*y+1,4*y+1,4*y+2]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [4*x+2,4*x+1,4*x+3,4*x+2]
        ind2 = [4*y+1,4*y+2,4*y+2,4*y+3]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)

        return currHeur

    def calcHeuristicBoard(self,ply,opp):
        # calculate the heuristic of the given board state
        bs = self.board.block_status 
        baseVal = 16    # The value which will the base for the exponent
        currHeur = 0
        for i in range(4):
            countPlyRow=0
            countPlyCol=0
            countDrawRow=0
            countDrawCol=0
            countOppRow=0
            countOppCol=0
            for j in range(4):
                if(bs[i][j]==ply):
                    countPlyRow+=1
                elif bs[i][j]==opp:
                    countOppRow+=1
                elif bs[i][j]=='d':
                    countDrawRow+=1
                if(bs[j][i]==ply):
                    countPlyCol+=1
                elif bs[j][i]==opp:
                    countOppCol+=1
                elif bs[j][i]=='d':
                    countDrawCol+=1
                
            if countPlyRow != 0  and countOppRow == 0 and countDrawRow == 0:
                currHeur += baseVal**countPlyRow
            elif countOppRow != 0 and countPlyRow == 0 and countDrawRow == 0:
                currHeur -=  baseVal**countOppRow

            if countPlyCol != 0 and countOppCol == 0 and countDrawCol == 0:
                currHeur += baseVal**countPlyCol
            elif countOppCol != 0 and countPlyCol == 0 and countDrawCol == 0:
                currHeur -=  baseVal**countOppCol
        # checking diamonds
        ind1 = [1,0,2,1]
        ind2 = [0,1,1,2]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [1,0,2,1]
        ind2 = [1,2,2,3]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [2,1,3,2]
        ind2 = [0,1,1,2]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)
        ind1 = [2,1,3,2]
        ind2 = [1,2,2,3]
        currHeur += self.checkDiam(ply,opp,ind1,ind2,baseVal,bs)

        return currHeur        

    def calcHeuristic(self,ply,opp):
        heur=0
        for i in range(4):
            for j in range(4):
                if(self.board.block_status[i][j]==ply):
                    heur+=100000000
                elif(self.board.block_status[i][j]==opp):
                    heur-=100000000
                else:
                    heur+=self.calcHeuristicBlock(ply,opp,i,j)
        heur+=(self.calcHeuristicBoard(ply,opp) * 200)
        return heur

    def checkBlockWon(self,move):
        x=move[0]/4
        y=move[1]/4
        if self.board.block_status[x][y]=='x' or self.board.block_status[x][y]=='o':
            return True
        return False

    def minimax(self,depth,ply,maxi,old_move,opp,alpha,beta,count):
        # if count==2:
        #     print count, self.board.board_status
        currTime = datetime.datetime.now()
        if currTime - self.startTime >=self.timeLimit:
            self.gameOver=True
            return self.infinity,old_move
        valid_moves=self.board.find_valid_move_cells(old_move)
        if maxi is True: 
            m=-self.infinity
            move=valid_moves[0]
            tempBlock=copy.deepcopy(self.board.block_status)
            for mv in range(len(valid_moves)):
                i=valid_moves[mv][0]
                j=valid_moves[mv][1]
                # for i in range (12,16):
                #     for j in range (4,8):
                #         print self.board.board_status[i][j],
                #     print
                # print "updating"

                self.board.update(old_move,(i,j),ply)
                # print self.board.board_status, depth, [i,j], 'asds '
                # print self.board.block_status, depth, [i,j], 'asds '
                # for i in range (12,16):
                #     for j in range (4,8):
                #         print self.board.board_status[i][j],
                #     print
                # print "updated"
                # print self.board.block_status, depth, [i,j]
                status = self.board.find_terminal_state()
                if (status[0]==ply):
                    move=[i,j]
                    mm= self.infinity
                    self.board.board_status[i][j]='-'
                    self.board.block_status=copy.deepcopy(tempBlock)
                    break
                elif (status[1]=='DRAW'):
                    # print("FDF")
                    x_count=0
                    o_count=0
                    for row in range(4):
                        for col in range (4):
                            if self.board.block_status[row][col]=='x':
                                x_count+=1
                            elif self.board.block_status[row][col]=='o':
                                o_count+=1
                    if x_count == o_count:
                        mm = 0
                    elif x_count>o_count:
                        mm = (self.infinity/2) + (100*(x_count-o_count))
                    else:
                        mm = (-self.infinity/2) - (100*(o_count-x_count))
                    # print(x_count,o_count, 'gg')
                elif status[0]==opp:
                    mm = -self.infinity
                elif(depth>=self.maxDepth):
                    # print self.board.board_status
                    mm = self.calcHeuristic(ply,opp)
                else:
                    if self.checkBlockWon([i,j])  and self.lastWinner=='-':
                        self.lastWinner='x'
                        next_ply=True
                    else:
                        self.lastWinner='-'
                        next_ply=False
                    # print(self.board.board_status)
                    mm=self.minimax(depth+1,ply,next_ply,[i,j],opp,alpha,beta,count)[0]
                if(mm>m):
                    m=mm
                    move=[i,j]
                alpha=max(alpha,m)
                self.board.board_status[i][j]='-'
                self.board.block_status=copy.deepcopy(tempBlock)
                if beta<=alpha:
                    break
            # if(m <= alpha):
            #     self.transposition[hashval] = [-self.infinity,m]
            # if(m > alpha and m < beta):
            #     self.transposition[hashval] = [m,m]
            # if(m>=beta):
            #     self.transposition[hashval] = [m,self.infinity]
            # print(m,move)
            return m,move
        else:
            m=self.infinity
            move=valid_moves[0]
            tempBlock=copy.deepcopy(self.board.block_status)
            for mv in range(len(valid_moves)):
                i=valid_moves[mv][0]
                j=valid_moves[mv][1]
                # for i in range (12,16):
                #     for j in range (4,8):
                #         print self.board.board_status[i][j],
                #     print
                # print "updating"
                self.board.update(old_move,(i,j),opp)
                # print self.board.board_status, depth, [i,j], 'asds '   
                # print self.board.block_status, depth, [i,j], 'asds '
                # for i in range (12,16):
                #     for j in range (4,8):
                #         print self.board.board_status[i][j],
                #     print
                # print "updated"
                # print self.board.block_status, depth, [i,j]
                # print self.board.board_status
                status = self.board.find_terminal_state()
                if (status[0]==opp):
                    move=[i,j]
                    mm= -self.infinity
                    self.board.board_status[i][j]='-'
                    self.board.block_status=copy.deepcopy(tempBlock)
                    break
                elif (status[1]=='DRAW'):
                    # print("FDF")
                    x_count=0
                    o_count=0
                    for row in range(4):
                        for col in range (4):
                            if self.board.block_status[row][col]=='x':
                                x_count+=1
                            elif self.board.block_status[row][col]=='o':
                                o_count+=1
                    if x_count == o_count:
                        mm = 0
                    elif x_count>o_count:
                        mm = (self.infinity/2) + (100*(x_count-o_count))
                    else:
                        mm = (-self.infinity/2) - (100*(o_count-x_count))
                elif status[0]==ply:
                    mm = self.infinity
                elif(depth>=self.maxDepth):
                    mm = self.calcHeuristic(ply,opp)
                else:
                
                    if self.checkBlockWon([i,j]) and self.lastWinner=='-':
                        self.lastWinner='o'
                        next_ply=False
                    else:
                        self.lastWinner='-'
                        next_ply=True
                    
                    mm=self.minimax(depth+1,ply,next_ply,[i,j],opp,alpha,beta,count)[0]
                # print(mm)
                if(mm<m):
                    m=mm
                    move=[i,j]
                beta=min(beta,m)
                self.board.board_status[i][j]='-'
                self.board.block_status=copy.deepcopy(tempBlock)
                if beta<=alpha:
                    break
            return m,move
    def move(self, board, old_move, flag):
        self.count+=1
        self.startTime = datetime.datetime.now()
        self.board=copy.deepcopy(board)
        self.gameOver=False
        if flag == 'x':
            opp = 'o'
        else:
            opp = 'x'
        
        move=self.board.find_valid_move_cells(old_move)[0]
        for depth in range (2,100):
            self.maxDepth=depth
            dsaa= self.minimax(1,flag,True,old_move,opp,-self.infinity,self.infinity,self.count)
            if self.gameOver is True:
                # print 'time khatam'
                break
            else:
                # print 'time hai'
                # print(dsaa)
                val=dsaa[0]
                move=dsaa[1]
        return move[0],move[1]
