import math

# Дано:
#   1. Координаты подключения стояка
#   2. Координаты подключения сливов
#   2. Координаты стен
# Нужно:
#   1. Определить пересечение стен - определить углы
#   2. Определить точку подхода стояка к ближайшей стене
#   3. Сделать проекцию всех точек (стояк, сливы, углы, подвод стояка) на "пол" XY
#   4. Построить дерево соединения между точками от самой ближней к самой дальней
#   5. Дополнить точки подключения высотой расположения (Z) с нужным уклоном (3см на 1м)
# Итого:
#   Основная трасса построенная на основе дерева - соединение между точками


class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


class Riser:
    # Стояк канализации
    def __init__(self, point: Point):
        self.point = point


class Drain:
    #  Слив канализации
    def __init__(self, point: Point):
        self.point = point


class Wall:
    # Стена
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2


def wall_intersection(wall1: Wall, wall2: Wall):
    xdiff = (wall1.point1.x - wall1.point2.x, wall2.point1.x - wall2.point2.x)
    ydiff = (wall1.point1.y - wall1.point2.y, wall2.point1.y - wall2.point2.y)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        # Отрезки параллельны или совпадают
        return None
    else:
        d = (
            det((wall1.point1.x, wall1.point1.y), (wall1.point2.x, wall1.point2.y)),
            det((wall2.point1.x, wall2.point1.y), (wall2.point2.x, wall2.point2.y)),
        )
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # Проверка, находится ли точка пересечения внутри обоих отрезков
        def is_point_on_segment(point, segment: Wall):
            x_min = min(segment.point1.x, segment.point2.x)
            x_max = max(segment.point1.x, segment.point2.x)
            y_min = min(segment.point1.y, segment.point2.y)
            y_max = max(segment.point1.y, segment.point2.y)

            return (x_min <= point[0] <= x_max) and (y_min <= point[1] <= y_max)

        if is_point_on_segment((x, y), wall1) and is_point_on_segment((x, y), wall2):
            return Point(x, y)
        else:
            # Точка пересечения не находится на обоих отрезках
            return None


# Определяет пересечение стен
def walls_intersections(walls: list) -> list:
    intersections = []
    processed = []
    for wall1 in walls:
        for wall2 in walls:
            if wall1 == wall2:
                continue
            key = [str(id(wall1)), str(id(wall2))]
            key.sort()
            key = '-'.join(key)
            if key in processed:
                continue
            processed.append(key)
            intersection = wall_intersection(wall1, wall2)
            if intersection:
                intersections.append(intersection)
    return intersections

# Возвращает точку примыкания стояка к стене
def construct_perpendicular(point: Point, wall: Wall) -> Point:
    x, y = point.x, point.y
    x1, y1 = wall.point1.x, wall.point1.y
    x2, y2 = wall.point2.x, wall.point2.y

    abx = x1 - x2
    aby = y1 - y2
    dacab = (x - x1) * abx + (y - y1) * aby
    dab = abx * abx + aby * aby
    t = dacab / dab

    return Point(x1 + abx * t, y1 + aby * t)


# Возвращает точку примыкания стояка с ближайшей стеной
def get_riser_contiguity(riser: Riser, walls: list) -> Wall:
    min_dist = 0.0
    nearest_wall = None
    for wall in walls:
        dist = distance_point_to_segment(
            (riser.point.x, riser.point.y),
            ((wall.point1.x, wall.point1.y), (wall.point2.x, wall.point2.y))
        )
        if dist <= 0.0:
            continue
        if (min_dist == 0.0) | (dist < min_dist):
            min_dist = dist
            nearest_wall = wall

    return nearest_wall

# Определение расстояния между точкой и стеной
def distance_point_to_segment(point, segment) -> float:
    x1, y1 = segment[0]
    x2, y2 = segment[1]
    x, y = point

    # Вычисляем вектора от точки к концам отрезка
    dx = x2 - x1
    dy = y2 - y1
    dx1 = x - x1
    dy1 = y - y1
    dx2 = x - x2
    dy2 = y - y2

    # Если точка лежит на отрезке, возвращаем ноль
    if (dx1 * dx + dy1 * dy <= 0) and (dx2 * dx + dy2 * dy >= 0):
        return 0.0

    # Иначе вычисляем расстояние до ближайшей точки на отрезке
    if dx * dx + dy * dy == 0:
        # Отрезок выродился в точку, возвращаем расстояние до этой точки
        return math.sqrt(dx1 * dx1 + dy1 * dy1)
    else:
        # Находим ближайшую точку на прямой, содержащей отрезок
        t = max(0, min(1, (dx1 * dx + dy1 * dy) / (dx * dx + dy * dy)))
        x_closest = x1 + t * dx
        y_closest = y1 + t * dy

        # Вычисляем расстояние между точкой и ближайшей точкой на прямой
        dist = math.sqrt((x - x_closest) ** 2 + (y - y_closest) ** 2)
        return dist


def distance_between_points(point1: Point, point2: Point) -> float:
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)


riser = Riser(Point(7, 3, 3))
drain1 = Drain(Point(1, 2, 3))
drain2 = Drain(Point(1, 2, 3))
drains = [drain1.point, drain2.point]

wall1 = Wall(Point(2, 2), Point(2, 13))
wall2 = Wall(Point(2, 2), Point(6, 2))
wall3 = Wall(Point(6, 5), Point(6, 2))
wall4 = Wall(Point(6, 5), Point(8, 5))
wall5 = Wall(Point(8, 13), Point(8, 5))

wall6 = Wall(Point(8, 13), Point(6, 13))
wall7 = Wall(Point(2, 13), Point(3, 13))

walls = [wall1, wall2, wall3, wall4, wall5, wall6, wall7]

# 1. Определить пересечение стен - определить углы
walls_intersections = walls_intersections(walls)

# 2. Определить точку подхода стояка к ближайшей стене
nearest_wall = get_riser_contiguity(riser, walls)
riser_contiguity = None
if nearest_wall:
    riser_contiguity = construct_perpendicular(riser.point, nearest_wall)

if riser_contiguity is None:
    exit(2)

# 3. Сделать проекцию всех точек (стояк, сливы, углы, подвод стояка) на "пол" XY

# 4. Построить дерево соединения между точками от самой ближней к самой дальней
corners_and_drains = walls_intersections + drains


def ccl(contiguity: Point, targets: list):
    for target in targets:
        dist = distance_between_points(contiguity, target)
        print(dist, target.x, target.y)


tree = ccl(riser_contiguity, corners_and_drains)

print(tree)

# Дано:
#   1. Основная трасса канализации
# Нужно:
#   1.
