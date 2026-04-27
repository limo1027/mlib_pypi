from . import _roll
from .smath import floor, acos


class SimpleRNG:
    """简单随机数生成器"""

    def __init__(self, seed=None):
        """初始化随机数生成器"""
        if seed is None:
            if not hasattr(SimpleRNG, '_seed_counter'):
                SimpleRNG._seed_counter = 0
            else:
                SimpleRNG._seed_counter += 1
            seed = id(object()) + id(SimpleRNG._seed_counter) + SimpleRNG._seed_counter

        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = self.my_hash(seed)
        for i in range(20):
            self.next()

    def sum_until_one(self, n):
        """把一个数不断加各位直到剩一位"""
        m = n
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return (n * m) % 1000

    def my_hash(self, seed, moduli=None):
        """自定义哈希函数"""
        if moduli is None:
            moduli = [5, 7, 89, 97, 997, 991, 9963, 9971]

        if not str(seed):
            raise ValueError("种子不能为空")

        s = seed if isinstance(seed, str) else str(seed)
        parts = [str(ord(c) * place) for place, c in enumerate(s, start=1)]
        big_str = ''.join(parts)

        result = []
        for m in moduli:
            k = len(str(m))
            remainders = []
            for i in range(0, len(big_str), k):
                group = big_str[i:i+k]
                group_num = int(group)
                r = group_num % m
                remainders.append(r)
            total = sum(remainders)
            digit = self.sum_until_one(total)
            result.append(digit)

        return tuple(int(d) for d in result)
    
    def seed(self, seed):
        """重新设置种子"""
        self.a, self.b, self.c, self.d, self.e, self.f = self.my_hash(seed)
        for i in range(20):
            self.next()

    def next(self, a=0, b=9):
        """生成下一个随机数"""
        self.a = (self.a + self.h) % 10**16
        self.a ^= self.a >> 3
        self.b = (self.b + self.a) % 10**16
        self.b ^= self.b >> 1
        self.c = (self.c + self.b) % 10**16
        self.c ^= self.c >> 4
        self.d = (self.d + self.c) % 10**16
        self.d ^= self.d >> 1
        self.e = (self.e + self.d) % 10**16
        self.e ^= self.e >> 5
        self.f = (self.f + self.e) % 10**16
        self.f ^= self.f >> 9
        self.g = (self.g + self.f) % 10**16
        self.g ^= self.g >> 2
        self.h = (self.h + self.g) % 10**16
        self.h ^= self.h >> 6
        return a + self.h % (b - a + 1)

    def roll(self, expr):
        """掷骰子表达式"""
        parsed = _roll.parse_dice(expr)
        total = 0

        for part in parsed['parts']:
            if part['type'] == 'dice':
                total += _roll.roll_dice(part, self.randint)
            else:
                total += part['value']

        return total
    
    def randint(self, start, end):
        """生成范围内的随机整数"""
        if start > end:
            start, end = end, start
        return self.next(start, end)

    def random(self):
        """生成 0-1 之间的随机浮点数"""
        self.next()
        return self.h % 10 ** 16 / 10 ** 16

    def random_float(self, start, end):
        """生成指定范围内的随机浮点数"""
        return self.random() * (end - start) + start

    def choice(self, candidates):
        """从列表中随机选择一个元素"""
        if not candidates:
            raise ValueError("候选列表不能为空")
        return candidates[int(self.random() * len(candidates))]

    def shuffle(self, items):
        """打乱列表（原地修改）"""
        for i in range(len(items) - 1, 0, -1):
            j = self.randint(0, i)
            items[i], items[j] = items[j], items[i]
        return items

    def shuffle_copy(self, items):
        """返回打乱后的新列表（不修改原列表）"""
        items_copy = items.copy()
        return self.shuffle(items_copy)

    def sample(self, items, k):
        """从列表中随机抽取 k 个不重复的元素"""
        if k > len(items):
            raise ValueError("k 不能大于列表长度")

        items_copy = items.copy()
        self.shuffle(items_copy)

        return items_copy[:k]

    def choices(self, arr, weight=None):
        """加权随机选择"""
        if weight is None:
            return self.choice(arr)

        if len(arr) != len(weight):
            raise ValueError("arr 和 weight 长度不一致")

        if abs(sum(weight) - 1) > 1e-10:
            raise ValueError("权重和不为 1")

        su = 0
        num = self.random()
        for i, w in enumerate(weight):
            su += w
            if num < su:
                return arr[i]

        return arr[-1]

    def gauss(self, mu=0.0, sigma=1.0):
        """高斯分布（正态分布）随机数"""
        while True:
            u1 = self.random() * 2 - 1
            u2 = self.random() * 2 - 1
            r2 = u1 * u1 + u2 * u2
            if 0 < r2 < 1:
                break

        log_r2 = self._approx_log(r2)
        z = u1 * (-2 * log_r2) ** 0.5 / r2 ** 0.5
        return mu + sigma * z

    def sample_by_y(self, func, x_min, x_max, step=0.01, y_max=None):
        """按函数分布采样"""
        if y_max is None:
            y_max = max(func(x_min + i * step) for i in range(int((x_max - x_min) / step) + 1))
            y_min = min(func(x_min + i * step) for i in range(int((x_max - x_min) / step) + 1))
        else:
            y_min = min(func(x_min + i * step) for i in range(int((x_max - x_min) / step) + 1))

        while True:
            y = self.random() * (y_max - y_min) + y_min

            candidates = []
            x = x_min
            while x <= x_max:
                if func(x) >= y:
                    candidates.append(x)
                x += step

            if candidates:
                return round(candidates[int(self.random() * len(candidates))], 10)

    def _approx_log(self, x):
        """近似自然对数"""
        if x <= 0:
            return float('-inf')

        y = x - 1
        if abs(y) < 0.1:
            return y - y*y/2 + y*y*y/3 - y*y*y*y/4

        exponent = 0
        while x > 2:
            x /= 2
            exponent += 1
        while x < 1:
            x *= 2
            exponent -= 1

        y = x - 1
        log_x = y - y*y/2 + y*y*y/3 - y*y*y*y/4
        return log_x + exponent * 0.6931471805599453

    def uuid(self):
        """生成随机 UUID"""
        strings = "ABCDEF1234567890"
        length = len(strings) - 1
        result = ""
        for i in range(8):
            result += strings[self.randint(0, length)]
        result += "-"

        for i in range(3):
            for j in range(4):
                result += strings[self.randint(0, length)]
            result += "-"

        for i in range(12):
            result += strings[self.randint(0, length)]

        result = list(result)
        result[14] = "6"
        result = "".join(result)
        return result

    def uniform(self, a, b):
        """均匀分布随机浮点数"""
        return self.random_float(a, b)



def random(rng=None):
    """生成 0-1 随机数"""
    if rng is None:
        rng = SimpleRNG()
    return rng.random()


def randint(a, b, rng=None):
    """生成随机整数"""
    if rng is None:
        rng = SimpleRNG()
    return rng.randint(a, b)


def choice(seq, rng=None):
    """随机选择"""
    if rng is None:
        rng = SimpleRNG()
    return rng.choice(seq)


def shuffle(seq, rng=None):
    """打乱列表"""
    if rng is None:
        rng = SimpleRNG()
    return rng.shuffle(seq)


def sample(seq, k, rng=None):
    """随机抽样"""
    if rng is None:
        rng = SimpleRNG()
    return rng.sample(seq, k)
