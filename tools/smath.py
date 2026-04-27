# smath.py - 数学工具模块

pi = 3.141592653589793
e = 2.718281828459045
tau = 2 * pi
phi = 1.618033988749895

EPSILON = 1e-15
INF = float('inf')

                
def gcd(a, b):
    """最大公约数"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def log_fast(n, base=10):
    k = 1
    while True:
        try:
            if base ** k > n:
                break
            k *= 2
        except:
            break
    
    low, high = k // 2, k
    while low <= high:
        mid = (low + high) // 2
        if base ** mid <= n:
            low = mid + 1
        else:
            high = mid - 1
    
    return high

def lcm(a, b):
    """最小公倍数"""
    return abs(a * b) // gcd(a, b)


def factorial(n):
    """阶乘 n!"""
    if n < 0:
        raise ValueError("阶乘不支持负整数")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def comb(n, k):
    """组合数 C(n,k)"""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def perm(n, k):
    """排列数 P(n,k)"""
    return comb(n, k) * factorial(k)


def _exp(x, terms=30):
    """e^x 泰勒展开"""
    result = 1.0
    term = 1.0
    for n in range(1, terms):
        term *= x / n
        result += term
        if abs(term) < EPSILON:
            break
    return result


def _ln(x):
    """自然对数 ln(x)"""
    if x <= 0:
        raise ValueError("ln(x) 定义域为 x > 0")

    if abs(x - 1) < 0.1:
        y = x - 1
        result = 0
        term = y
        for n in range(1, 50):
            result += term / n
            term *= -y
            if abs(term / (n + 1)) < EPSILON:
                break
        return result

    exponent = 0
    while x > 2:
        x /= 2
        exponent += 1
    while x < 1:
        x *= 2
        exponent -= 1

    y = x - 1
    result = 0
    term = y
    for n in range(1, 50):
        result += term / n
        term *= -y
        if abs(term / (n + 1)) < EPSILON:
            break

    return result + exponent * 0.6931471805599453


def _log_complex(z):
    """复数自然对数 ln(z)"""
    if not isinstance(z, complex):
        return _ln(z)

    # 模长
    r = (z.real**2 + z.imag**2) ** 0.5
    if r == 0:
        return float("-inf")

    # 辐角 atan2(y, x)
    theta = _atan2(z.imag, z.real)
    result = complex(_ln(r), theta)
    if abs(result.imag) < EPSILON:  # 浮点数精度阈值
        return result.real
    return result


def _atan2(y, x):
    """辐角函数 atan2(y, x)"""
    if x > 0:
        return _atan(y / x)
    elif x < 0:
        if y >= 0:
            return _atan(y / x) + pi
        else:
            return _atan(y / x) - pi
    else:
        if y > 0:
            return pi / 2
        elif y < 0:
            return -pi / 2
        else:
            return 0.0



def _atan(x, terms=500):
    """反正切 arctan(x)"""
    if abs(x) > 1:
        return pi/2 - _atan(1/x, terms) if x > 0 else -pi/2 - _atan(1/x, terms)

    if abs(x) == 1:
        return pi / 4

    if x > 0.8:
        # atan(x) = π/4 - atan((1-x)/(1+x))
        return pi/4 - _atan((1 - x) / (1 + x), terms)
    
    result = 0.0
    x2 = x * x
    term = x
    for n in range(terms):
        result += term / (2 * n + 1)
        term *= -x2
        if abs(term / (2 * n + 3)) < EPSILON:
            break
    return result


def log(z, base=None):
    """任意底数的对数"""
    if base is None:
        return _log_complex(z)
    ln_z = _log_complex(z)
    ln_base = _log_complex(base)
    if isinstance(ln_z, complex) or isinstance(ln_base, complex):
        return ln_z / ln_base
    return ln_z / ln_base

def exp(z):
    return _exp(z)

def log10(z):
    """以 10 为底的对数"""
    return log(z, 10)


def log2(z):
    """以 2 为底的对数"""
    return log(z, 2)


def ln(z):
    """自然对数"""
    return _log_complex(z)


def cos(x):
    """余弦函数"""
    if isinstance(x, complex):
        ix = complex(-x.imag, x.real)
        return (_exp(ix) + _exp(-ix)) / 2

    x = x % (2 * pi)
    x2 = x * x
    result = 1.0
    term = 1.0
    for n in range(1, 50):
        term *= -x2 / ((2 * n - 1) * (2 * n))
        result += term
        if abs(term) < EPSILON:
            break
    return result


def sin(x):
    """正弦函数"""
    if isinstance(x, complex):
        ix = complex(-x.imag, x.real)
        return (_exp(ix) - _exp(-ix)) / complex(0, 2)

    x = x % (2 * pi)
    x2 = x * x
    result = 0.0
    term = x
    for n in range(50):
        result += term
        term *= -x2 / ((2 * n + 2) * (2 * n + 3))
        if abs(term) < EPSILON:
            break
    return result


def tan(x):
    """正切函数"""
    c = cos(x)
    if abs(c) < EPSILON:
        raise ValueError("tan(x) 在 x = {:.6f} 处无定义".format(x))
    return sin(x) / c


def cot(x):
    """余切函数"""
    s = sin(x)
    if abs(s) < EPSILON:
        raise ValueError("cot(x) 在 x = {:.6f} 处无定义".format(x))
    return cos(x) / s


def sec(x):
    """正割函数"""
    c = cos(x)
    if abs(c) < EPSILON:
        raise ValueError("sec(x) 在 x = {:.6f} 处无定义".format(x))
    return 1.0 / c


def csc(x):
    """余割函数"""
    s = sin(x)
    if abs(s) < EPSILON:
        raise ValueError("csc(x) 在 x = {:.6f} 处无定义".format(x))
    return 1.0 / s


def asin(x):
    """反正弦函数"""
    if isinstance(x, complex):
        return complex(0, -1) * _log_complex(complex(0, 1) * x + (1 - x * x) ** 0.5)
    if abs(x) > 1:
        return complex(0, -1) * _log_complex(complex(0, 1) * x + (1 - x * x) ** 0.5)
    if x == 1:
        return pi / 2
    if x == -1:
        return -pi / 2
    return _atan(x / (1 - x * x) ** 0.5)


def acos(x):
    """反余弦函数"""
    if isinstance(x, complex):
        return complex(0, -1) * _log_complex(x + complex(0, 1) * (1 - x * x) ** 0.5)
    if abs(x) > 1:
        return complex(0, -1) * _log_complex(x + complex(0, 1) * (1 - x * x) ** 0.5)
    return pi / 2 - asin(x)


def atan(x):
    """反正切函数"""
    if isinstance(x, complex):
        return (complex(0, 1) / 2) * _log_complex((complex(0, 1) + x) / (complex(0, 1) - x))
    return _atan(x)


def atan2(y, x):
    """双参数反正切"""
    if isinstance(y, complex) or isinstance(x, complex):
        raise ValueError("atan2 不支持复数")
    return _atan2(y, x)


def cosh(x):
    """双曲余弦"""
    return (_exp(x) + _exp(-x)) / 2


def sinh(x):
    """双曲正弦"""
    return (_exp(x) - _exp(-x)) / 2


def tanh(x):
    """双曲正切"""
    return sinh(x) / cosh(x)


def coth(x):
    """双曲余切"""
    return cosh(x) / sinh(x)


def acosh(x):
    """反双曲余弦"""
    if x < 1:
        raise ValueError("acosh(x) 定义域为 x >= 1")
    return _ln(x + (x * x - 1) ** 0.5)


def asinh(x):
    """反双曲正弦"""
    return _ln(x + (x * x + 1) ** 0.5)


def atanh(x):
    """反双曲正切"""
    if abs(x) >= 1:
        raise ValueError("atanh(x) 定义域为 |x| < 1")
    return 0.5 * _ln((1 + x) / (1 - x))


def round(x):
    """四舍五入"""
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


def floor(x):
    """向下取整"""
    i = int(x)
    return i - 1 if x < 0 and x != i else i


def ceil(x):
    """向上取整"""
    i = int(x)
    return i + 1 if x > 0 and x != i else i


def trunc(x):
    """截断取整"""
    return int(x)


def root(x, n=2):
    """n 次方根"""
    if n == 0:
        raise ValueError("0 次方根无定义")
    if x < 0:
        return -((-x) ** (1.0 / n))
    return x ** (1.0 / n)


def sqrt(x):
    """平方根"""
    return x ** 0.5


def cbrt(x):
    """立方根"""
    if x < 0:
        return -((-x) ** (1.0 / 3))
    return x ** (1.0 / 3)


def hypot(*args):
    """欧几里得范数（距离）"""
    if not args:
        return 0.0
    return sum(x * x for x in args) ** 0.5


sign = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
rad = lambda x: x * pi / 180
deg = lambda x: x * 180 / pi
fract = lambda x: x - floor(x) if x >= 0 else fract(-x)


def wrap(x, a, b):
    """将 x 限制在 [a, b) 范围内循环"""
    if a >= b:
        raise ValueError("a 必须小于 b")
    range_len = b - a
    return a + (x - a) % range_len


def clamp(x, min_val, max_val):
    """将 x 限制在 [min_val, max_val] 范围内"""
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x


def lerp(a, b, t):
    """线性插值"""
    return a + (b - a) * t


def inv_lerp(a, b, v):
    """反向线性插值"""
    if a == b:
        return 0.0
    return (v - a) / (b - a)


def map(x, in_min, in_max, out_min, out_max, clamp_result=False):
    """将 x 从 [in_min, in_max] 映射到 [out_min, out_max]"""
    if in_max == in_min:
        raise ValueError("in_max 不能等于 in_min")
    value = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if clamp_result:
        return clamp(value, out_min, out_max)
    return value


def correlation(x_arr, y_arr):
    """皮尔逊相关系数"""
    if len(x_arr) != len(y_arr):
        raise ValueError("数组长度必须相同")
    if len(x_arr) < 2:
        return 0.0

    x_mean = mean(x_arr)
    y_mean = mean(y_arr)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_arr, y_arr))
    x_var = sum((x - x_mean) ** 2 for x in x_arr)
    y_var = sum((y - y_mean) ** 2 for y in y_arr)

    denominator = (x_var * y_var) ** 0.5
    if denominator < EPSILON:
        return 0.0

    return numerator / denominator


def is_prime(n):
    """判断素数"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def prime_factors(n):
    """质因数分解"""
    if n < 2:
        return []

    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def fibonacci(n):
    """第 n 个斐波那契数"""
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def abs(x):
    """绝对值"""
    return x.__abs__()

def min(*args):
    """最小值"""
    if len(args) == 1:
        args = args[0]
    if not args:
        raise ValueError("min() 至少需要一个参数")
    result = args[0]
    for arg in args[1:]:
        if arg < result:
            result = arg
    return result


def max(*args):
    """最大值"""
    if len(args) == 1:
        args = args[0]
    if not args:
        raise ValueError("max() 至少需要一个参数")
    result = args[0]
    for arg in args[1:]:
        if arg > result:
            result = arg
    return result


def sum(arr):
    """求和"""
    result = 0
    for x in arr:
        result += x
    return result


def product(arr):
    """求积"""
    if not arr:
        return 1
    result = 1
    for x in arr:
        result *= x
    return result


def normalize_angle(angle):
    """将角度归一化到 [-pi, pi]"""
    angle = angle % (2 * pi)
    if angle > pi:
        angle -= 2 * pi
    return angle


def distance(p1, p2):
    """两点间距离"""
    if len(p1) != len(p2):
        raise ValueError("点的维度必须相同")
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5


def angle_between(v1, v2):
    """两向量间夹角（弧度）"""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = sum(a * a for a in v1) ** 0.5
    norm2 = sum(b * b for b in v2) ** 0.5
    if norm1 < EPSILON or norm2 < EPSILON:
        return 0.0
    cos_angle = clamp(dot / (norm1 * norm2), -1, 1)
    return acos(cos_angle)
