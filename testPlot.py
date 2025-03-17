from planDesk import *
MODE = "TEST"

plan_list = []
open_list = [[15275, 775], [15275, 7855], [11095, 7855], [11095, 4955], [9135, 4955], [9135, 7855], [775, 7855], [775, 8725], [17525, 8725], [17525, 5875], [16960, 5875], [16960, 5640], [16725, 5640], [16725, 8540], [12545, 8540], [12545, 5640], [16725, 5640], [16725, 8540], [12545, 8540]]

LIMIT_POINTS = [[0 + 775, 0 + 775], [0 + 775, 9500 - 775], [18300 - 775, 9500 - 775],
                [18300 - 775, 5100 + 775], [17735 - 775, 5100 + 775], [17735 - 775, 4865 + 775],
                [17500 - 775, 4865 + 775], [17500 - 775, 0 + 775]]

WALL_POINTS = [[0, 0], [0, 9500], [18300, 9500], [18300, 5100], [17735, 5100], [17735, 4865],
               [17500, 4865], [17500, 0]]

n = len(open_list)
for i in range(n):
    point = open_list[i]
    next_point = open_list[(i + 1) % n]
    if point[0] != next_point[0] and point[1] != next_point[1]:
        print(point, next_point)


def plot_open_points(plan_list, open_list):
    plt.clf()
    # 绘制边界
    for i in range(0, len(WALL_POINTS) - 1):
        plt.plot([WALL_POINTS[i][0], WALL_POINTS[i + 1][0]], [WALL_POINTS[i][1], WALL_POINTS[i + 1][1]], color='red')
    plt.plot([WALL_POINTS[len(WALL_POINTS) - 1][0], WALL_POINTS[0][0]],
             [WALL_POINTS[len(WALL_POINTS) - 1][1], WALL_POINTS[0][1]], color='red')
    for i in range(0, len(LIMIT_POINTS) - 1):
        plt.plot([LIMIT_POINTS[i][0], LIMIT_POINTS[i + 1][0]], [LIMIT_POINTS[i][1], LIMIT_POINTS[i + 1][1]],
                 color='red', linestyle='--')
    plt.plot([LIMIT_POINTS[len(LIMIT_POINTS) - 1][0], LIMIT_POINTS[0][0]],
             [LIMIT_POINTS[len(LIMIT_POINTS) - 1][1], LIMIT_POINTS[0][1]],
             color='red', linestyle='--')

    for i in range(len(open_list)):
        plt.text(open_list[i][0], open_list[i][1], f'{open_list[i][0], open_list[i][1]}', fontsize=7, ha='left')

    n = len(open_list)
    for i in range(n):
        plt.plot([open_list[i][0], open_list[(i + 1) % n][0]], [open_list[i][1], open_list[(i + 1) % n][1]],
                 color='blue')

    plt.axis('equal')
    global pic_id
    plt.savefig(f"fig/{len(plan_list)}_{pic_id}.png")
    #if MODE == "TEST":
    plt.show()
    pic_id += 1
    print(1)

plot_open_points(plan_list, open_list)