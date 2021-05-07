import time
import random
import copy

print("""

オセロです。黒がCPUで、白があなたです。
手番順はランダムです。

☆置く位置の指定の仕方
・縦→横 の順番にかく
・入力は一列で
・縦と横の間には空白を入れる

"""
)

board = [
    ["/","1","2","3","4","5","6","7","8"],
    ["1","-","-","-","-","-","-","-","-"],
    ["2","-","-","-","-","-","-","-","-"],
    ["3","-","-","-","-","-","-","-","-"],
    ["4","-","-","-","-","-","-","-","-"],
    ["5","-","-","-","-","-","-","-","-"],
    ["6","-","-","-","-","-","-","-","-"],
    ["7","-","-","-","-","-","-","-","-"],
    ["8","-","-","-","-","-","-","-","-"],
]

points_board = [
    [30,-12,0,-1,-1,0,-12,30],
    [-12,-15,-3,-3,-3,-3,-15,-12],
    [0,-3,0,-1,-1,0,-3,0],
    [-1,-3,-1,-1,-1,-1,-3,-1],
    [-1,-3,-1,-1,-1,-1,-3,-1],
    [0,-3,0,-1,-1,0,-3,0],
    [-12,-15,-3,-3,-3,-3,-15,-12],
    [30,-12,0,-1,-1,0,-12,30]
]


#初期設定
board[4][4] = "●"
board[5][5] = "●"
board[4][5] = "○"
board[5][4] = "○"

visited = [[True]*9]+[[False]*9 for _ in range(8)]
visited[4][4] = True
visited[5][5] = True
visited[4][5] = True
visited[5][4] = True

for i in range(9):
    visited[i][0] = True

def Pyin():

    q = check(player)
    print(q)

    while True:

        try:
            h,w = map(int,input("(縦横の間にはスペースを開けてください)\n縦と横の番号を入力：").split())
            try:
                if [h,w] not in q:
                    print()
                    print("そこには置けません")
                    print()
                elif visited[h][w]:
                    print()
                    print("そのマスにはすでに駒が置かれています")
                    print()
                else:
                    break
            except:
                print()
                print("1 ~ 8の数字を入力してください")
                print()
        except:
            if h == "!":
                exit()
            print("縦と横の間はスペースを開けてください")
        
    return h,w


def search(h,w,TorF):
    All_side = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
    stone = ["●","○"]
    if TorF:
        index = 1
    else:
        index = 0

    for i in range(8):
        d = [[h,w]]
        cnt = 0
        while d:
            x,y = d.pop(0)
            nx,ny = All_side[i][0]+x, All_side[i][1]+y
            if 1 <= nx <= 8 and 1 <= ny <= 8:
                if board[nx][ny] == stone[index]:
                    cnt += 1
                    d.append([nx,ny])
                elif cnt > 0 and board[nx][ny] == stone[index-1]:
                    return True
                else:
                    break

    return False


def check(TorF):

    place = []

    for i in range(1,9):
        for j in range(1,9):
            
            if visited[i][j]:
                continue
            else:
                if search(i,j,TorF):
                    place.append([i,j])
                    
    return place

def play():
    h,w = Pyin()
    change(h,w,player)


def cpu():
    l = check(player)
    h,w = l[random.randint(0,len(l)-1)]
    change(h,w,player)
    print("CPUは {} {} に置きました".format(h,w))
    time.sleep(1)


def change(h,w,TorF):
    visited[h][w] = True
    All_side = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
    stone = ["●","○"]
    if TorF:
        index = 1
    else:
        index = 0

    for i in range(8):
        d = [[h,w]]
        cnt = 0
        while d:
            x,y = d.pop(0)
            nx,ny = All_side[i][0]+x, All_side[i][1]+y
            if 1 <= nx <= 8 and 1 <= ny <= 8:
                if board[nx][ny] == stone[index]:
                    cnt += 1
                    d.append([nx,ny])
                elif cnt > 0 and board[nx][ny] == stone[index-1]:
                    while nx != h or ny != w:
                        nx -= All_side[i][0]
                        ny -= All_side[i][1]
                        board[nx][ny] = stone[index-1]
                    board[h][w] = stone[index-1]
                else:
                    break

def cpu2():
    l = cpu3()
    if len(l) == 0:
        return 1
    answers = []
    # print(l)

    for j in range(len(l)):
        board_cp = copy.deepcopy(board)
        visited_cp = copy.deepcopy(visited)
        h,w = l[j][0],l[j][1]
        visited_cp[h][w] = True
        All_side = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
        stone = ["●","○"]

        for i in range(8):
            d = [[h,w]]
            cnt = 0

            while d:
                x,y = d.pop(0)
                nx,ny = All_side[i][0]+x, All_side[i][1]+y
                if 1 <= nx <= 8 and 1 <= ny <= 8:
                    if board_cp[nx][ny] == stone[0]:
                        cnt += 1
                        d.append([nx,ny])
                    elif cnt > 0 and board_cp[nx][ny] == stone[1]:
                        while nx != h or ny != w:
                            nx -= All_side[i][0]
                            ny -= All_side[i][1]
                            board_cp[nx][ny] = stone[1]
                        board_cp[h][w] = stone[1]
                    else:
                        break
        
            place = 0

            for k in range(1,9):
                for j in range(1,9):
                    if visited_cp[k][j]:
                        continue
                    else:
                        task = False

                        for i in range(8):
                            if task:
                                break
                            d = [[k,j]]
                            cnt = 0
                            while d:
                                x,y = d.pop(0)
                                nx,ny = All_side[i][0]+x, All_side[i][1]+y
                                if 1 <= nx <= 8 and 1 <= ny <= 8:
                                    if board_cp[nx][ny] == stone[1]:
                                        cnt += 1
                                        d.append([nx,ny])
                                    elif cnt > 0 and board_cp[nx][ny] == stone[0]:
                                        task = True
                                        break
                                    else:
                                        break
                        if task:
                            place += 1

        answers.append(place)

    print(answers)

    h,w = l[answers.index(min(answers))]
    change(h,w,player)
    print("CPUは {} {} に置きました".format(h,w))
    time.sleep(1)

def cpu3():
    l = check(player)
    if len(l) == 0:
        return 1
    answers = []
    # print(l)

    for j in range(len(l)):
        board_cp = copy.deepcopy(board)
        visited_cp = copy.deepcopy(visited)
        h,w = l[j][0],l[j][1]
        visited_cp[h][w] = True
        All_side = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
        stone = ["●","○"]

        for i in range(8):
            d = [[h,w]]
            cnt = 0

            while d:
                x,y = d.pop(0)
                nx,ny = All_side[i][0]+x, All_side[i][1]+y
                if 1 <= nx <= 8 and 1 <= ny <= 8:
                    if board_cp[nx][ny] == stone[0]:
                        cnt += 1
                        d.append([nx,ny])
                    elif cnt > 0 and board_cp[nx][ny] == stone[1]:
                        while nx != h or ny != w:
                            nx -= All_side[i][0]
                            ny -= All_side[i][1]
                            board_cp[nx][ny] = stone[1]
                        board_cp[h][w] = stone[1]
                    else:
                        break
        
        CPUs_point = 0
        points_board_cp = copy.deepcopy(points_board)

        if board_cp[8][8] == stone[1]:
            points_board_cp[7][6],points_board_cp[6][7],points_board_cp[6][6] = 20,20,20
        if board_cp[8][1] == stone[1]:
            points_board_cp[7][1],points_board_cp[6][0],points_board_cp[6][1] = 20,20,20
        if board_cp[1][1] == stone[1]:
            points_board_cp[0][1],points_board_cp[1][0],points_board_cp[1][1] = 20,20,20
        if board_cp[1][8] == stone[1]:
            points_board_cp[0][6],points_board_cp[1][7],points_board_cp[1][6] = 20,20,20

        for k in range(1,9):
            for j in range(1,9):
                if visited_cp[k][j] and board_cp[k][j] == stone[1]:
                    CPUs_point += points_board_cp[k-1][j-1]

        answers.append(CPUs_point)
    
    mx = max(answers)
    q = []
    for i in range(len(answers)):
        if answers[i] == mx:
            q.append(l[i])
    return q
    # h,w = l[answers.index(max(answers))]
    # change(h,w,player)
    
    
    # print("CPUは {} {} に置きました".format(h,w))
    # time.sleep(1)


#黒が先行か白が先行かを決める
player = random.randint(0,1)
if player == 0:
    player = True
else:
    player = False

for i in range(9):
    print(*board[i])
#メインループ

log = [0]*64
for i in range(60):

    if len(check(player)) == 0:
        if player:
            print("白は置ける場所がないので黒の手番に移ります。")
            # log[i+4] = -1
            # if log[i+3] == -1:
            #     break
            player = False
        else:
            print("黒は置ける場所がないので白の手番に移ります。")
            # log[i+4] = -1
            # if log[i+3] == -1:
            #     break
            player = True

    #各手番の処理を記述
    if player:
        print()
        print("白の番です。")
        print()
        time.sleep(1)
        play()
        #cpu()
        player = False
    else:
        print()
        print("黒の番です。")
        print()
        time.sleep(1)
        cpu2()
        #cpu()
        player = True

    for i in range(9):
        print(*board[i])

white = 0
black = 0
for i in range(1,9):
    for j in range(1,9):
        if board[i][j] == "●":
            white += 1
        else:
            black += 1

print()
print("白：{} VS {}：黒".format(white,black))
if white > black:
    print('白の勝ち！')
elif black > white:
    print("黒の勝ち！")
else:
    print('引き分け！')