import random

grid = {}
for i in range(3):
    for j in range(4):
        grid[(i, j)] = 0.0


class AI:
    def __init__(self):
        self.WinCoordinate = (2, 3)
        self.LoseCoordinate = (1, 3)
        self.StartCoordinate = (0, 0)
        self.Block = (1, 1)
        grid[(2, 3)] = 1.00
        grid[(1, 3)] = -1.00
        grid[(1, 1)] = "BLK"
        self.position = (0, 0)
        self.gameOver = False
        self.reward = 0.0
        self.positionsList = []
        self.actionsList = ["up", "left", "down", "right"]
        self.alpha = 0.2

    def takeReward(self, pos):
        if pos == self.WinCoordinate:
            return 1.0
        elif pos == self.LoseCoordinate:
            return -1.0
        else:
            return 0.0

    def reset(self):
        self.gameOver = False
        self.position = (0, 0)
        self.positionsList = []

    def isGameOver(self):
        if self.position == self.WinCoordinate or self.position == self.LoseCoordinate:
            self.gameOver = True

    def possibleMove(self, action):
        global possibleposition
        if action == "up":
            possibleposition = (self.position[0] - 1, self.position[1])
        elif action == "down":
            possibleposition = (self.position[0] + 1, self.position[1])
        elif action == "right":
            possibleposition = (self.position[0], self.position[1] + 1)
        elif action == "left":
            possibleposition = (self.position[0], self.position[1] - 1)
        if 0 <= possibleposition[0] <= 2:
            if 0 <= possibleposition[1] <= 3:
                if possibleposition != self.Block:
                    self.position = possibleposition
        return self.position

    def chooseAction(self):
        global action
        maxpossiblereward = 0
        if random.uniform(0.0, 1.0) <= 0.3:
            action = random.choice(self.actionsList)
        else:
            for a in self.actionsList:
                possiblereward = grid[self.possibleMove(a)]
                if possiblereward >= maxpossiblereward:
                    action = a
                    maxpossiblereward = possiblereward
        return action

    def makeAMove(self, action):
        position = self.possibleMove(action)
        # self.positionsList.append(position)
        return position

    def Reverse(self, list):
        list.reverse()
        return list

    def play(self, runs):
        while runs > 0:
            if self.gameOver:
                #print("GAMEOVER POSITION {}".format(self.position))
                reward = self.takeReward(self.position)
                grid[self.position] = reward
                self.positionsList = self.Reverse(self.positionsList)
                # print("{}".format(self.positionsList))
                for position in range(0, len(self.positionsList)):
                    reward = grid[self.positionsList[position]] + self.alpha * (reward - grid[self.positionsList[position]])
                    grid[self.positionsList[position]] = round(reward, 3)
                    #print(reward, grid[self.positionsList[position]])
                self.reset()
                runs = runs - 1
                #print("_______________________________________")
            else:
                action = self.chooseAction()
                #print("Current position: {} , Action: {}".format(self.position, action))
                self.position = self.makeAMove(action)
                self.positionsList.append(self.position)
                self.isGameOver()
                #print("Now, position is: {}".format(self.position))
                #print("___________________________")

    def printGridValues(self):
        for i in range(0, 3):
            print("----------------------------------")
            line = "| "
            for j in range(0, 4):
                line = line + str(grid[(i, j)]) + " | "
            print(line)
        print("----------------------------------")


if __name__ == "__main__":
    AI().play(50)
    AI().printGridValues()
