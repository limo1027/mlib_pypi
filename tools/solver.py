# solver.py - 解1-3次方程（支持复数）
# 依赖: smath (sqrt, cos, acos, pi, 复数支持)

from .smath import sqrt, cos, acos, pi

class NoSolutionError(Exception):
    pass

def solve_linear(a, b):
    """解一次方程 ax + b = 0"""
    if a == 0:
        if b == 0:
            return 'infinite'  # 无数解
        else:
            return []  # 无解
    return [(-b) / a]


def solve_quadratic(a, b, c):
    """解二次方程 ax² + bx + c = 0（支持复数）"""
    if a == 0:
        return solve_linear(b, c)
    
    delta = b*b - 4*a*c
    
    # 直接计算平方根（复数自动处理）
    sqrt_delta = sqrt(delta)
    x1 = (-b - sqrt_delta) / (2*a)
    x2 = (-b + sqrt_delta) / (2*a)
    
    if x1 == x2:
        return [x1]
    return [x1, x2]


def solve_cubic(a, b, c, d):
    if a == 0:
        return solve_quadratic(b, c, d)
    # 1. 计算 p, q
    p = (3*a*c - b*b) / (3*a*a)
    q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)
    
    # 2. 判别式
    delta = (q/2)**2 + (p/3)**3
    
    # 3. 计算 u, v
    u = (-q/2 + delta**0.5) ** (1/3)  # 主立方根
    v = (-q/2 - delta**0.5) ** (1/3)
    
    # 4. 关键：调整 v 使 u*v = -p/3
    if abs(u*v + p/3) > 1e-10:
        v = -p/(3*u)  # 强制满足关系
    
    # 5. 三个根
    omega = complex(-0.5, 0.8660254037844386)
    omega2 = omega * omega
    
    y1 = u + v
    y2 = u*omega + v*omega2
    y3 = u*omega2 + v*omega
    
    # 6. 还原 x
    x1 = y1 - b/(3*a)
    x2 = y2 - b/(3*a)
    x3 = y3 - b/(3*a)
    
    return [x1, x2, x3]


def _cbrt(x):
    """立方根（支持复数）"""
    # 用复数形式
    if isinstance(x, complex) or x < 0:
        return x ** (1/3)
    return x ** (1/3)


def _is_duplicate(x, roots, eps=1e-10):
    """检查是否重复（处理浮点误差）"""
    for r in roots:
        if abs(x - r) < eps:
            return True
    return False


def _deduplicate(roots, eps=1e-10):
    """去重"""
    result = []
    for x in roots:
        if not _is_duplicate(x, result, eps):
            result.append(x)
    return result


def _is_zero(x, eps=1e-10):
    """判断是否接近0"""
    return abs(x) < eps


# ========== 高阶函数 ==========

def solve_polynomial(coefficients):
    """自动选择解法"""
    # 去掉开头的0
    while len(coefficients) > 1 and _is_zero(coefficients[0]):
        coefficients.pop(0)
    
    n = len(coefficients) - 1  # 次数
    
    if n == 0:
        return 'infinite' if _is_zero(coefficients[0]) else []
    elif n == 1:
        return solve_linear(coefficients[0], coefficients[1])
    elif n == 2:
        return solve_quadratic(coefficients[0], coefficients[1], coefficients[2])
    elif n == 3:
        return solve_cubic(coefficients[0], coefficients[1], coefficients[2], coefficients[3])
    else:
        raise ValueError(f"不支持 {n} 次方程")


# ========== 便捷函数 ==========

def roots(coefficients):
    """求根（别名）"""
    return solve_polynomial(coefficients.copy())


def poly(val, coefficients):
    """计算多项式值（支持复数）"""
    result = 0
    for c in coefficients:
        result = result * val + c
    return result
