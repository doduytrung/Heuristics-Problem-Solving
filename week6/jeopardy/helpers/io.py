import socket
from hunter import Hunter
from prey import Prey
from coordinate import Coordinate
from wall import Wall

class IO:
    HOST = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teamname = 'jeopardy'
    def __init__(self, port):
        self.flag = 0
        self.portNo = port
        self.s.connect((self.HOST, self.portNo))

    def start(self):
        prev = ""
        while 1:
            resp = self.s.recv(1024) + prev

            if '\n' not in resp:
                prev = resp
                continue

            resp = resp.split('\n')

            currResp = resp[0]
            resp.pop(0)

            prev = '\n'.join(resp)
            # print currResp

            if 'done' in currResp:
                break

            if 'sendname' in currResp:
                self.sendOutput(self.teamname)
                continue

            if 'hunter' in currResp:
                self.playerType = 'hunter'
                self.flag = 0
                continue
            elif 'prey' in currResp:
                self.playerType = 'prey'
                self.flag = 0
                continue

            currResp = currResp.split(' ')

            currResp = self.parseInput(currResp)

            if self.flag == 0:
                self.flag = 1
                self.player = Hunter(currResp) if self.playerType == 'hunter' else Prey(currResp)

            self.sendOutput(self.parseOutput(self.player.move(currResp)))

        self.s.close()

    def parseInput(self, resp):
        info = {};

        info['timeLeft'] = resp[0]
        info['gameNum'] = resp[1]
        info['tickNum'] = resp[2]

        info['maxWalls'] = int(resp[3])
        info['wallPlacementDelay'] = resp[4]
        info['boardSizeX'] = int(resp[5])
        info['boardSizeY'] = int(resp[6])

        info['currentWallTimer'] = resp[7]
        info['hunter'] = Coordinate(resp[8], resp[9], resp[10], resp[11])
        info['prey'] = Coordinate(resp[12], resp[13])

        info['numWalls'] = int(resp[14])

        info['walls'] = []

        for i in range(0, info['numWalls']):
            info['walls'].append(Wall(int(resp[15 + i * 4]), int(resp[16 + i * 4]), int(resp[17 + i * 4]), int(resp[18 + i * 4])))

        return info

    def parseOutput(self, infoMap):
        output = []

        output.append(infoMap['gameNum'])
        output.append(infoMap['tickNum'])

        if self.playerType == 'hunter':

            # 0 for none, 1 for horizontal, 2 for vertical
            # Wall will be created for whole axes until other wall is encountered
            # or board's end is reached
            output.append(str(infoMap['wallAdd']))

            # wallDelete should be a list
            for i in infoMap['wallDelete']:
                output.append(str(i))

        else:
            # prey
            # x and y should 0, -1, 1
            output.append(str(infoMap['x']))
            output.append(str(infoMap['y']))

        return " ".join(output)

    def sendOutput(self, out):
        self.s.sendall(out + "\n")
