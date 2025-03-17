import matplotlib
import matplotlib.pyplot as plt
import copy
import pickle

plt.ioff()
MODE = "PROD"
# MODE = "PROD"

TABLE_SPACE = 1350


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

        self.middle_point = self.get_middle_point()

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

    def get_middle_point(self):
        new_points = self.get_new_points()
        new_points.append(self.point)

        middlePoint = [0, 0]
        for point in new_points:
            middlePoint[0] += point[0]
            middlePoint[1] += point[1]

        middlePoint[0] = int(middlePoint[0] / 4 * 10)
        middlePoint[1] = int(middlePoint[1] / 4 * 10)
        return middlePoint

    def is_same(self, plan):
        if type(self.desk) == type(plan.desk) and\
            self.is_up == plan.is_up and\
            self.point == plan.point and\
            self.direction == plan.direction:
            return True



LIMIT_POINTS = [[0 + 775, 0 + 775], [0 + 775, 9500 - 775], [18300 - 775, 9500 - 775],
                [18300 - 775, 5100 + 775], [17735 - 775, 5100 + 775], [17735 - 775, 4865 + 775],
                [17500 - 775, 4865 + 775], [17500 - 775, 0 + 775]]

WALL_POINTS = [[0, 0], [0, 9500], [18300, 9500], [18300, 5100], [17735, 5100], [17735, 4865],
               [17500, 4865], [17500, 0]]

OPEN_POINTS = [[0 + 775, 0 + 775], [0 + 775, 9500 - 775], [18300 - 775, 9500 - 775],
               [18300 - 775, 5100 + 775], [17735 - 775, 5100 + 775], [17735 - 775, 4865 + 775],
               [17500 - 775, 4865 + 775], [17500 - 775, 0 + 775]]

global pic_id
pic_id = 0


def plot_plan_list(plan_list, open_list, final):
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
                     color=color, linestyle='--')
        plt.plot([plan_points[len(plan_points) - 1][0], plan_points[0][0]],
                 [plan_points[len(plan_points) - 1][1], plan_points[0][1]], color=color, linestyle='--')

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

    for i in range(len(open_list)):
        plt.text(open_list[i][0], open_list[i][1], f'{open_list[i][0], open_list[i][1]}', fontsize=7, ha='left')

    plt.axis('equal')
    global pic_id
    plt.savefig(f"fig/{len(plan_list)}_{pic_id}_{final}.png")
    #if pic_id == 216:
        #saveStatus(open_list, plan, plan_list)
    if MODE == "TEST":
        plt.show()
    pic_id += 1
    print(1)


# 排序键函数
def sort_key(plan):
    # 定义 desk 类型的优先级
    desk_priority = {
        ClassicDesk: 1,
        MiddleDesk: 2,
        SmallDesk: 3
    }
    # 获取 desk 类型的优先级
    desk_type_priority = desk_priority.get(type(plan.desk), float("inf"))

    # 获取 point 的 x 和 y 坐标
    x, y = plan.middle_point

    # is_up 的排序，True 排在前面，False 排在后面
    is_up_priority = 0 if plan.is_up else 1

    # 返回一个元组，按照优先级排序
    return (desk_type_priority, x, y, is_up_priority)

# 根据plan，计算出桌子类型+中心位置（*10的位数）+方向
def get_plan_set_value(plan):
    if type(plan.desk) == ClassicDesk:
        desk_type = "classic"
    elif type(plan.desk) == MiddleDesk:
        desk_type = "middle"
    else:
        desk_type = "small"

    middlePoint = plan.middle_point

    return f"{desk_type}_[{middlePoint[0]},{middlePoint[1]}]_{plan.is_up}+"


# 根据plan_list计算出这个状态的set value
def get_plan_list_set_value(plan_list, plan):
    tmp_plan_list = copy.deepcopy(plan_list)
    tmp_plan_list.append(plan)

    sorted_plans = sorted(tmp_plan_list, key=sort_key)

    value = ""
    for plan in sorted_plans:
        value += get_plan_set_value(plan)
    return value

def tryPlan(plan, plan_list, open_list, plan_set):
    refresh = False
    tmp_open_list = copy.deepcopy(open_list)
    tmp_plan_list = copy.deepcopy(plan_list)

    # 如果这个方案之前过过了
    plan_list_set_value = get_plan_list_set_value(plan_list, plan)
    if plan_list_set_value in plan_set:
        print("already done this")
        return open_list, plan_list, plan_set, refresh

    for current_plan in plan_list:
        if plan.is_same(current_plan):
            return open_list, plan_list, plan_set, refresh
    if is_plan_legal(plan, open_list):
        open_list = update_open_list(open_list, plan, plan_list)
        plan_list.append(plan)
        plan_set.add(plan_list_set_value)
        planDesk(plan_list, open_list, plan_set)
        refresh = True
    open_list = copy.deepcopy(tmp_open_list)
    plan_list = copy.deepcopy(tmp_plan_list)
    '''
    if refresh:
        plot_plan_list(plan_list)
        a = 1
    '''
    return open_list, plan_list, plan_set, refresh


plan_list = []
plan_set = set()
# "desk_mid_isUp+"
open_list = [0, 0]


def planDesk(plan_list, open_list, plan_set):
    if MODE == "TEST":
        plot_plan_list(plan_list, open_list, "notfinal")

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
                    open_list, plan_list, plan_set, refresh = tryPlan(Plan(desk, is_up, point, dirction), plan_list, open_list, plan_set)
                    if refresh:
                        foundFlag = True
    if not foundFlag and MODE == "PROD":
        plot_plan_list(plan_list, open_list, "FINAL")


def is_line_legal(point, next_point, point_list):
    if point[0] == next_point[0]:
        if point[1] < next_point[1]:
            for y in range(point[1], next_point[1] + 5, 5):
                if not is_point_in_polygon([point[0], y], point_list):
                    return False
        if point[1] >= next_point[1]:
            for y in range(point[1], next_point[1] - 5, -5):
                if not is_point_in_polygon([point[0], y], point_list):
                    return False
    if point[1] == next_point[1]:
        if point[0] < next_point[0]:
            for x in range(point[0], next_point[0] + 5, 5):
                if not is_point_in_polygon([x, point[1]], point_list):
                    return False
        if point[0] >= next_point[0]:
            for x in range(point[0], next_point[0] - 5, -5):
                if not is_point_in_polygon([x, point[1]], point_list):
                    return False
    return True




# 判断一个plan是否合法，是否可以放在这个地方
def is_plan_legal(plan, point_list):
    middle_point = copy.deepcopy(plan.middle_point)
    middle_point[0] /= 10
    middle_point[1] /= 10
    if not is_point_in_polygon(middle_point, point_list):
        return False
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

        # 判断在不在边界上
        if p1x == p2x:
            if x == p1x:
                if y <= max(p1y, p2y) and y >= min(p1y, p2y):
                    return True

        if p1y == p2y:
            if y == p1y:
                if x <= max(p1x, p2x) and x >= min(p1x, p2x):
                    return True

        # |
        if p1y != p2y and max(p1y, p2y) > y > min(p1y, p2y):
            if x < p1x:
                inside = not inside
        elif p1y == p2y == y:
            if x < p1x:
                # 还需要判断这段横线，左右两边的竖线是同一方向还是不同方向
                p0x, p0y = polygon[i - 1]
                p3x, p3y = polygon[(i + 2) % n]

                # 不是同向 （同向 |__|）
                if not ((p0y > p1y and p2y < p3y) or (p0y < p1y and p2y > p3y)):
                    inside = not inside

    return inside


def is_point_legal(point):
    1


def update_open_list(open_list, plan, plan_list):
    if plan.point == [11095, 4955] and plan.direction == "ru":
        #plot_plan_list(plan_list, open_list)
        print(1)
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

    for i in range(len(open_list)):
        if open_list[i][0] != open_list[(i + 1) % len(open_list)][0] and open_list[i][1] != open_list[(i + 1) % len(open_list)][1]:
            print("wrong")
            saveStatus(open_list, plan, plan_list)
            exit(0)

    return open_list

def saveStatus(open_list, plan, plan_list):
    with open("tables.pkl", "wb") as file:
        pickle.dump([open_list, plan, plan_list], file)
        print("对象已序列化到文件")

if __name__ == "__main__":
    planDesk([], OPEN_POINTS, set())

    print(is_point_in_polygon([3, 3], [[3, 1], [3, 5], [50, 5]]))
