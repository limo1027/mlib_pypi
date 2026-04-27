from .svector import vec2
from .srandom import SimpleRNG


# ========== A* 寻路算法 ==========

def _heuristic(a, b, method='manhattan'):
    """计算启发式距离"""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])

    if method == 'manhattan':
        return dx + dy
    elif method == 'euclidean':
        return (dx**2 + dy**2) ** 0.5
    elif method == 'chebyshev':
        return max(dx, dy)
    elif method == 'octile':
        return max(dx, dy) + (1.41421356 - 1) * min(dx, dy)
    else:
        return dx + dy


def astar(grid, start, end, heuristic='manhattan', allow_diagonal=False):
    """A* 寻路算法 - 启发式最短路径搜索"""
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    if not _is_passable(grid, start) or not _is_passable(grid, end):
        return None

    open_set = [start]
    came_from = {start: None}

    g_score = {start: 0}
    f_score = {start: _heuristic(start, end, heuristic)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

        if current == end:
            return _reconstruct_path(came_from, start, end)

        open_set.remove(current)

        x, y = current

        if allow_diagonal:
            neighbors = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
            ]
        else:
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for neighbor in neighbors:
            if not _is_passable(grid, neighbor):
                continue

            dx = abs(neighbor[0] - current[0])
            dy = abs(neighbor[1] - current[1])

            if allow_diagonal and dx == 1 and dy == 1:
                move_cost = 1.41421356
            else:
                move_cost = 1

            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + _heuristic(neighbor, end, heuristic)

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None


def astar_weighted(grid, start, end, weight=1.0, heuristic='manhattan', allow_diagonal=False):
    """加权 A*算法 - 通过权重平衡速度和最优性"""
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    if not _is_passable(grid, start) or not _is_passable(grid, end):
        return None

    open_set = [start]
    came_from = {start: None}

    g_score = {start: 0}
    f_score = {start: g_score[start] + weight * _heuristic(start, end, heuristic)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

        if current == end:
            return _reconstruct_path(came_from, start, end)

        open_set.remove(current)

        x, y = current

        if allow_diagonal:
            neighbors = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
            ]
        else:
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for neighbor in neighbors:
            if not _is_passable(grid, neighbor):
                continue

            dx = abs(neighbor[0] - current[0])
            dy = abs(neighbor[1] - current[1])

            if allow_diagonal and dx == 1 and dy == 1:
                move_cost = 1.41421356
            else:
                move_cost = 1

            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + weight * _heuristic(neighbor, end, heuristic)

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None


# ========== Dijkstra 算法 ==========

def dijkstra(grid, start, end, weights=None, allow_diagonal=False):
    """Dijkstra 算法 - 带权图的最短路径"""
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    if not _is_passable(grid, start) or not _is_passable(grid, end):
        return None

    open_set = [start]
    came_from = {start: None}
    dist = {start: 0}

    while open_set:
        current = min(open_set, key=lambda x: dist.get(x, float('inf')))

        if current == end:
            return _reconstruct_path(came_from, start, end)

        open_set.remove(current)

        x, y = current

        if allow_diagonal:
            neighbors = [
                (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
            ]
        else:
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for neighbor in neighbors:
            if not _is_passable(grid, neighbor):
                continue

            dx = abs(neighbor[0] - current[0])
            dy = abs(neighbor[1] - current[1])

            if weights and neighbor in weights:
                move_cost = weights[neighbor]
            elif allow_diagonal and dx == 1 and dy == 1:
                move_cost = 1.41421356
            else:
                move_cost = 1

            new_dist = dist[current] + move_cost

            if neighbor not in dist or new_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = new_dist

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None


# ========== 双向 BFS ==========

def bidirectional_bfs(grid, start, end):
    """双向 BFS 寻路 - 从起点和终点同时搜索"""
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    if not _is_passable(grid, start) or not _is_passable(grid, end):
        return None

    forward_queue = [start]
    backward_queue = [end]

    forward_visited = {start: None}
    backward_visited = {end: None}

    meeting_point = None

    while forward_queue and backward_queue:
        if forward_queue:
            current = forward_queue.pop(0)

            if current in backward_visited:
                meeting_point = current
                break

            x, y = current
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                neighbor = (x + dx, y + dy)

                if _is_passable(grid, neighbor) and neighbor not in forward_visited:
                    forward_visited[neighbor] = current
                    forward_queue.append(neighbor)

        if backward_queue:
            current = backward_queue.pop(0)

            if current in forward_visited:
                meeting_point = current
                break

            x, y = current
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                neighbor = (x + dx, y + dy)

                if _is_passable(grid, neighbor) and neighbor not in backward_visited:
                    backward_visited[neighbor] = current
                    backward_queue.append(neighbor)

    if meeting_point is None:
        return None

    path = []
    current = meeting_point
    while current is not None:
        path.append(current)
        current = forward_visited.get(current)
    path.reverse()

    current = backward_visited.get(meeting_point)
    while current is not None:
        path.append(current)
        current = backward_visited.get(current)

    return [vec2(x, y) for x, y in path]

def bfs(grid, start, end):
    """广度优先搜索寻路 - 保证最短路径"""
    # 转成元组好处理
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    # 检查起点终点
    if not _is_passable(grid, start) or not _is_passable(grid, end):
        return None

    # 手动实现队列：列表 + 头尾指针
    queue = [start]          # 队列
    queue_head = 0           # 队头指针

    # 记录路径
    came_from = {start: None}

    # BFS主循环
    while queue_head < len(queue):
        current = queue[queue_head]
        queue_head += 1

        # 到达终点
        if current == end:
            return _reconstruct_path(came_from, start, end)

        x, y = current
        # 4方向探索
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            # 如果可走且没访问过
            if _is_passable(grid, neighbor) and neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return None  # 没找到路径

def dfs_maker(width, height, start=(1,1), seed=None):
    """深度优先搜索生成迷宫"""
    # 确保尺寸为奇数（保证墙壁厚度）
    random = SimpleRNG(seed)
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # 初始化全墙迷宫
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # 起点
    sx, sy = start
    maze[sy][sx] = 0

    # 栈
    stack = [(sx, sy)]

    # 方向（每次移动2格，保持墙壁厚度）
    dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    while stack:
        x, y = stack[-1]

        # 找未访问的邻居
        neighbors = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if (0 < nx < width-1 and 0 < ny < height-1 and
                maze[ny][nx] == 1):
                neighbors.append((nx, ny, dx//2, dy//2))

        if neighbors:
            # 随机选一个邻居
            nx, ny, wx, wy = random.choice(neighbors)

            # 打通墙壁和邻居
            maze[y + wy][x + wx] = 0  # 中间的墙
            maze[ny][nx] = 0           # 邻居格子

            stack.append((nx, ny))
        else:
            # 回溯
            stack.pop()

    return maze

def _is_passable(grid, pos):
    """检查位置是否可通行"""
    x, y = pos
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == 0


def _reconstruct_path(came_from, start, end):
    """重建路径"""
    path = []
    current = end

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    # 转成vec2列表
    return [vec2(x, y) for x, y in path]



