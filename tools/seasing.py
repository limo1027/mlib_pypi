from .smath import pi, sin
# ========== 基本缓动 ==========

def linear(t):
    """匀速"""
    return t

def quad_in(t):
    """加速 - t²"""
    return t * t

def quad_out(t):
    """减速 - t*(2-t)"""
    return t * (2 - t)

def quad_in_out(t):
    """先加速后减速"""
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

# ========== 三次缓动 ==========

def cubic_in(t):
    return t * t * t

def cubic_out(t):
    t -= 1
    return t * t * t + 1

def cubic_in_out(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        t = 2 * t - 2
        return 0.5 * t * t * t + 1

# ========== 弹性缓动 ==========

def back_in(t):
    """先回拉再前进"""
    s = 1.70158
    return t * t * ((s + 1) * t - s)

def back_out(t):
    s = 1.70158
    t -= 1
    return t * t * ((s + 1) * t + s) + 1

# ========== 弹跳缓动 ==========

def bounce_out(t):
    """落地弹跳效果"""
    if t < 1/2.75:
        return 7.5625 * t * t
    elif t < 2/2.75:
        t -= 1.5/2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:
        t -= 2.25/2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625/2.75
        return 7.5625 * t * t + 0.984375

# ========== 弹性缓动 ==========

def elastic_in(t):
    """橡皮筋拉伸效果"""
    if t == 0 or t == 1:
        return t
    p = 0.3
    s = p / 4
    t -= 1
    return -(2 ** (10 * t)) * sin((t - s) * (2 * pi) / p)

# ========== 工具函数 ==========

def tween(start, end, duration, elapsed, easing=linear):
    """实际补间计算"""
    if elapsed >= duration:
        return end
    if elapsed <= 0:
        return start

    t = elapsed / duration
    return start + (end - start) * easing(t)


class Tween:
    """简单的补间动画类"""

    def __init__(self, start, end, duration, easing=linear):
        self.start = start
        self.end = end
        self.duration = duration
        self.easing = easing
        self.elapsed = 0
        self.completed = False

    def update(self, dt):
        if self.completed:
            return self.end

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.completed = True
            return self.end

        t = self.elapsed / self.duration
        return self.start + (self.end - self.start) * self.easing(t)

    def reset(self):
        self.elapsed = 0
        self.completed = False


# ========== 常用缓动字典 ==========

EASING = {
    'linear': linear,
    'quad_in': quad_in,
    'quad_out': quad_out,
    'quad_in_out': quad_in_out,
    'cubic_in': cubic_in,
    'cubic_out': cubic_out,
    'cubic_in_out': cubic_in_out,
    'back_in': back_in,
    'back_out': back_out,
    'bounce_out': bounce_out,
    'elastic_in': elastic_in,
}


# ========== 快捷函数 ==========

def ease(t, type='linear'):
    """用字符串指定缓动类型"""
    return EASING.get(type, linear)(t)
