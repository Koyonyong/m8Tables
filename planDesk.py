import matplotlib
import matplotlib.pyplot as plt
import copy
plt.ioff()
class Desk(object):
    def __init__(self, l, w):
        self.l = l
        self.w = w

class ClassicDesk(Desk):
    def __init__(self):
        Desk.__init__(self, 2830 + 1350, 1550 + 1350)

class MiddleDesk(Desk):
    def __init__(self):
        Desk.__init__(self, 2630 + 1350, 1490 + 1350)

class SmallDesk(Desk):
    def __init__(self):
        Desk.__init__(self, 2375 + 1350, 1365 + 1350)

class Plan():
    def __init__(self, desk, is_up, point, direction):
        self.desk = desk
        self.is_up = is_up
        self.point = point
        self.direction = direction
        if self.is_up:
            self.w = self.desk.w
            self.l = self.desk.l
        else:
            self.w = self.desk.l
            self.l = self.desk.w

    def get_new_points(self):
        new_points = []
        if self.direction == "lu":
            new_points.append([self.point[0], self.point[1] + self.l])
            new_points.append([self.point[0] - self.w, self.point[1] + self.l])
            new_points.append([self.point[0] - self.w, self.point[1]])

        elif self.direction == "ld":
            new_points.append([self.point[0] - self.w, self.point[1]])
            new_points.append([self.point[0] - self.w, self.point[1] - self.l])
            new_points.append([self.point[0], self.point[1] - self.l])
        elif self.direction == "ru":
            new_points.append([self.point[0] + self.w, self.point[1]])
            new_points.append([self.point[0] + self.w, self.point[1] + self.l])
            new_points.append([self.point[0], self.point[1] + self.l])
        else:
            new_points.append([self.point[0], self.point[1] - self.l])
            new_points.append([self.point[0] + self.w, self.point[1] - self.l])
            new_points.append([self.point[0] + self.w, self.point[1]])
        return new_points


LIMIT_POINTS = [[0 + 775, 0 + 775], [0 + 775, 9500 - 775], [18300 - 775, 9500 - 775],
                [18300 - 775, 5100 + 775], [17500 - 775, 5100 + 775], [17500 - 775, 0 + 775]]
WALL_POINTS = [[0, 0], [0, 9500], [18300, 9500], [18300, 5100], [17500, 5100], [17500, 0]]

OPEN_POINTS = [[0 + 775, 0 + 775], [0 + 775, 9500 - 775], [18300 - 775, 9500 - 775],
                [18300 - 775, 5100 + 775], [17500 - 775, 5100 + 775], [17500 - 775, 0 + 775]]


global pic_id
pic_id = 0
def plot_plan_list(plan_list):
    plt.clf()
    # 绘制边界
    for i in range(0, len(WALL_POINTS) - 1):
        plt.plot([WALL_POINTS[i][0], WALL_POINTS[i + 1][0]], [WALL_POINTS[i][1], WALL_POINTS[i + 1][1]], color = 'red')
    plt.plot([WALL_POINTS[len(WALL_POINTS) - 1][0], WALL_POINTS[0][0]], [WALL_POINTS[len(WALL_POINTS) - 1][1], WALL_POINTS[0][1]], color = 'red')
    for i in range(0, len(LIMIT_POINTS) - 1):
        plt.plot([LIMIT_POINTS[i][0], LIMIT_POINTS[i + 1][0]], [LIMIT_POINTS[i][1], LIMIT_POINTS[i + 1][1]], color = 'red', linestyle = '--')
    plt.plot([LIMIT_POINTS[len(LIMIT_POINTS) - 1][0], LIMIT_POINTS[0][0]], [LIMIT_POINTS[len(LIMIT_POINTS) - 1][1], LIMIT_POINTS[0][1]],
             color = 'red', linestyle = '--')
    # 绘制所有的桌子
    for plan in plan_list:
        if type(plan.desk) == ClassicDesk:
            color = 'blue'
        elif type(plan.desk) == MiddleDesk:
            color = 'green'
        else:
            color = 'orange'
        plan_points = [plan.point]
        new_points = plan.get_new_points()
        plan_points += new_points
        for i in range(0, len(plan_points) - 1):
            plt.plot([plan_points[i][0], plan_points[i + 1][0]], [plan_points[i][1], plan_points[i + 1][1]],
                     color=color, linestyle = '--')
        plt.plot([plan_points[len(plan_points) - 1][0], plan_points[0][0]],
                 [plan_points[len(plan_points) - 1][1], plan_points[0][1]], color=color, linestyle = '--')


        inside_points = copy.deepcopy(plan_points)
        sorted_points = sorted(inside_points, key=lambda point: (point[0], point[1]))
        sorted_points[0][0] += 675
        sorted_points[0][1] += 675
        sorted_points[1][0] += 675
        sorted_points[1][1] -= 675
        sorted_points[2][0] -= 675
        sorted_points[2][1] += 675
        sorted_points[3][0] -= 675
        sorted_points[3][1] -= 675
        tmp = sorted_points[3]
        sorted_points[3] = sorted_points[2]
        sorted_points[2] = tmp
        for i in range(0, len(sorted_points) - 1):
            plt.plot([sorted_points[i][0], sorted_points[i + 1][0]], [sorted_points[i][1], sorted_points[i + 1][1]],
                     color=color)
        plt.plot([sorted_points[len(sorted_points) - 1][0], sorted_points[0][0]],
                 [sorted_points[len(sorted_points) - 1][1], sorted_points[0][1]], color=color)

    plt.axis('equal')
    global pic_id
    plt.savefig(f"fig/{len(plan_list)}_{pic_id}.png")
    pic_id += 1
    print(1)

def tryPlan(plan, plan_list, open_list):
    refresh = False
    tmp_open_list = copy.deepcopy(open_list)
    tmp_plan_list = copy.deepcopy(plan_list)
    if is_plan_legal(plan, open_list):
        open_list = update_open_list(open_list, plan)
        plan_list.append(plan)
        planDesk(plan_list, open_list)
        refresh = True
    open_list = copy.deepcopy(tmp_open_list)
    plan_list = copy.deepcopy(tmp_plan_list)
    '''
    if refresh:
        plot_plan_list(plan_list)
        a = 1
    '''
    return open_list, plan_list, refresh


plan_list = []
open_list = [0, 0]
def planDesk(plan_list, open_list):
    # plot_plan_list(plan_list)

    foundFlag = False
    # 尝试三种桌子
    for i in range(0, 3):
        if i == 0:
            desk = ClassicDesk()
        elif i == 1:
            desk = MiddleDesk()
        else:
            desk = SmallDesk()

        # 尝试所有可选点
        for point in open_list:
            for is_up in [True, False]:
                for dirction in ["lu", "ld", "ru", "rd"]:
                    open_list, plan_list, refresh = tryPlan(Plan(desk, is_up, point, dirction), plan_list, open_list)
                    if refresh:
                        foundFlag = True
    if not foundFlag:
        plot_plan_list(plan_list)


def is_line_legal(point, next_point, point_list):
    if point[0] == next_point[0]:
        if point[1] < next_point[1]:
            for y in range(point[1], next_point[1] + 50, 50):
                if not is_point_in_polygon([point[0], y], point_list):
                    return False
        if point[1] >= next_point[1]:
            for y in range(point[1], next_point[1] - 50, -50):
                if not is_point_in_polygon([point[0], y], point_list):
                    return False
    if point[1] == next_point[1]:
        if point[0] < next_point[0]:
            for x in range(point[0], next_point[0] + 50, 50):
                if not is_point_in_polygon([x, point[1]], point_list):
                    return False
        if point[0] >= next_point[0]:
            for x in range(point[1], next_point[1] - 50, -50):
                if not is_point_in_polygon([x, point[1]], point_list):
                    return False
    return True

# 判断一个plan是否合法，是否可以放在这个地方
def is_plan_legal(plan, point_list):

    new_points = plan.get_new_points()
    i = 0
    while i < len(new_points) - 1:
        point = new_points[i]
        next_point = new_points[i + 1]
        if not is_line_legal(point, next_point, point_list):
            return False
        i += 1

    point = new_points[len(new_points) - 1]
    next_point = plan.point
    if not is_line_legal(point, next_point, point_list):
        return False

    point = new_points[0]
    next_point = plan.point
    if not is_line_legal(point, next_point, point_list):
        return False

    return True

# 判断一个点是否在一个闭环内
# TODO 虽然一个矩形，可能四个点都在范围里，但是可能边不在
def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    # 遍历多边形的每条边
    for i in range(n):
        # 当前边的两个顶点
        p1x, p1y = polygon[i]
        p2x, p2y = polygon[(i + 1) % n]  # 下一个顶点，注意闭环

        # 检查点是否在边的 y 范围内
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                # 检查点是否在边的 x 范围内
                if x <= max(p1x, p2x):
                    # 计算交点的 x 坐标
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside

    return inside




def is_point_legal(point):
    1

def update_open_list(open_list, plan):
    print(f"open_list: {open_list}")
    print(f"plan: {plan.point}, new_points: {plan.get_new_points()}, is_up:{plan.is_up}, {plan.direction}")
    plan_point = plan.point
    plan_point_index = open_list.index(plan_point)
    open_list.pop(plan_point_index)
    new_points = plan.get_new_points()
    for i in range(0, 3):
        open_list.insert(plan_point_index + i, new_points[i])


    if open_list[plan_point_index][0] != open_list[plan_point_index - 1][0] \
        and open_list[plan_point_index][1] != open_list[plan_point_index - 1][1]:
        open_list.insert(plan_point_index, plan_point)
        open_list.insert(plan_point_index + 4, plan_point)

    changeFlag = True
    while changeFlag:
        changeFlag = False
        i = 0
        while i < len(open_list) - 1:
            if open_list[i][0] == open_list[i + 1][0] and open_list[i - 1][0] == open_list[i][0]:
                open_list.pop(i)
                changeFlag = True
                i -= 1
            i += 1

        lastI = len(open_list) - 1
        if open_list[lastI][0] == open_list[0][0] and open_list[lastI][0] == open_list[lastI - 1][0]:
            open_list.pop(i)
            changeFlag = True

        i = 0
        while i < len(open_list) - 1:
            if open_list[i][1] == open_list[i + 1][1] and open_list[i - 1][1] == open_list[i][1]:
                open_list.pop(i)
                changeFlag = True
                i -= 1
            i += 1

        lastI = len(open_list) - 1
        if open_list[lastI][1] == open_list[0][1] and open_list[lastI][1] == open_list[lastI - 1][1]:
            open_list.pop(i)
            changeFlag = True

    print(f"open_list: {open_list}")

    for i in range(len(open_list) - 1):
        if open_list[i][0] != open_list[i + 1][0] and open_list[i][1] != open_list[i + 1][1]:
            print("wrong")
            exit(0)

    return open_list

planDesk([], OPEN_POINTS)