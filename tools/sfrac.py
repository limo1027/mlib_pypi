from .smath import gcd as _gcd, log_fast
from .sradical import Radical
    
def is_int(floater):
    return abs(round(floater) - floater) < 1e-13

    
class Frac:
    """轻量分数类"""

    def __init__(self, numerator, denominator=None):
        """初始化分数"""
        if denominator is None:
             numerator, denominator = int(self._to_frac(numerator).n), int(self._to_frac(numerator).d)
        if denominator == 0:
            raise ValueError("分母不能为0")

        # 处理负号
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        # 自己约分，不用 math
        g = _gcd(numerator, denominator)
        self.n = numerator // g
        self.d = denominator // g

    def as_percent(self, precision=0):
        """准确的分数百分数显示"""
        # 用整数运算避免浮点误差
        percent_numerator = self.n * 100
        whole = percent_numerator // self.d
        remainder = percent_numerator % self.d

        if precision == 0:
            # 四舍五入
            if remainder * 2 >= self.d:
                whole += 1
            return f"{whole}%"

        # 小数部分
        result = f"{whole}."
        for i in range(precision):
            remainder *= 10
            digit = remainder // self.d
            result += str(digit)
            remainder = remainder % self.d

        return f"{result}%"

    def __pow__(self, other):
        """幂运算：self ** other"""
        other = self._to_frac(other)

        # 如果指数是整数，可以保持分数
        if other.d == 1:
            # 整数指数： (n/d)**m = n**m / d**m
            exp = other.n  # 可能是负数
            if exp >= 0:
                return Frac(self.n ** exp, self.d ** exp)
            else:
                # 负指数：倒数
                return Frac(self.d ** (-exp), self.n ** (-exp))


        # 指数是分数：开方，可能无法保持精确分数
        # 比如 (1/3)**(1/2) = 1/√3，无理数
        # 这种情况只能返回近似分数
        if is_int((self.d ** other.n) ** (1/other.d)) and is_int((self.n ** other.n) ** (1/other.d)):
            return Frac(round((self.n ** other.n) ** (1/other.d)), round((self.d ** other.n) ** (1/other.d)))
        return Radical(other.d, self ** other.n)

    def __rpow__(self, other):
        """右幂运算：other ** self"""
        return other ** self

    def __add__(self, other):
        """加法：self + other"""
        other = self._to_frac(other)
        return Frac(
            self.n * other.d + other.n * self.d,
            self.d * other.d
        )

    def __sub__(self, other):
        """减法：self - other"""
        other = self._to_frac(other)
        return Frac(
            self.n * other.d - other.n * self.d,
            self.d * other.d
        )

    def __mul__(self, other):
        """乘法：self * other"""
        other = self._to_frac(other)
        return Frac(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        """除法：self / other"""
        other = self._to_frac(other)
        if other.n == 0:
            raise ZeroDivisionError("除数不能为0")
        return Frac(self.n * other.d, self.d * other.n)
    
    def __eq__(self, other):
        """等于：self == other"""
        other = self._to_frac(other)
        return self.n == other.n and self.d == other.d

    def __lt__(self, other):
        """小于：self < other"""
        other = self._to_frac(other)
        # a/b < c/d  <=> a*d < c*b
        return self.n * other.d < other.n * self.d

    def __le__(self, other):
        """小于等于：self <= other"""
        return self == other or self <= other

    def __gt__(self, other):
        """大于：self > other"""
        return not self < other

    def __ge__(self, other):
        """大于等于：self >= other"""
        return not self < other or self == other


    def __radd__(self, other):
        """右加法：other + self"""
        return self + other  # 直接复用 __add__

    def __rsub__(self, other):
        """右减法：other - self"""
        # 注意顺序：other - self
        return -self + other

    def __rmul__(self, other):
        """右乘法：other * self"""
        return self * other

    def __rtruediv__(self, other):
        """右除法：other / self"""
        # other / self = other * (1/self)
        return self._to_frac(other) * ~self


    def __neg__(self):
        """负数：-self"""
        return Frac(-self.n, self.d)

    def __pos__(self):
        """正数：+self"""
        return self

    def __abs__(self):
        """绝对值：abs(self)"""
        return Frac(abs(self.n), self.d)

    def __invert__(self):
        """~frac 返回倒数"""
        return Frac(self.d, self.n)

    def __float__(self):
        """将分数转换为浮点数"""
        return self.n / self.d

    def __format__(self, spec):
        """支持格式化字符串"""
        if not spec:
            return str(self)
        
        
        spec = spec.strip()
        
        if spec.endswith('%'):
            return self.as_percent(int(spec[:-1]) if spec[:-1] else 0)

        if spec.startswith('.'):
            parts = spec[1:].split('f')
            if len(parts) == 2 and parts[1] == '':
                precision = int(parts[0]) if parts[0] else 6
                
                def fmt_num(x):
                    s = f"{x:.{precision}f}"
                    # 去掉末尾的 0 和小数点
                    s = s.rstrip('0').rstrip('.')
                    return s
                
                n_str = fmt_num(self.n)
                d_str = fmt_num(self.d)
                return f"({n_str}/{d_str})"
            
        if spec == 'l' or spec == 'latex':
            if self.d == 1:
                return str(self.n)
            return f"\\frac{{{self.n}}}{{{self.d}}}"
        
        if spec == 'm' or spec == 'mixed':
            if abs(self.n) >= self.d:
                whole = self.n // self.d
                remainder = abs(self.n % self.d)
                if remainder == 0:
                    return str(whole)
                sign = '-' if self.n < 0 else ''
                return f"{sign}{abs(whole)} + {remainder}/{self.d}"
            return str(self)
        
        if spec == '/' or spec == 'frac':
            return f"{self.n}/{self.d}"
        
        if spec.endswith('f'):
            precision = int(spec[:-1]) if spec[:-1] else 6
            return f"{self.n / self.d:.{precision}f}"
        
        if spec.endswith('e') or spec.endswith('E'):
            precision = int(spec[:-1]) if spec[:-1] else 6
            return f"{self.n / self.d:.{precision}{spec[-1]}}"
        
        return str(self)
        

    def __int__(self):
        return int(float(self))
    
    def __str__(self):
        """将分数转换为字符串"""
        # 尝试显示分数
        try:
            if self.d >= 10**1000 or self.n >= 10**1000:
                raise ValueError
            if self.d != 1:
                return f"{self.n}/{self.d}"
            return str(self.n)
        except ValueError:
            pass
        
        
        n, d = self.n, self.d
        
        # 计算指数（log10 返回整数）
        exp_n = log_fast(n)
        exp_d = log_fast(d)
        exp = exp_n - exp_d
        
        # 计算 mantissa = n / (10**exp) / d
        # 用整数运算：mantissa = n * 10**(-exp) / d
        if exp >= 0:
            # n / (10**exp) / d = n / (d * 10**exp)
            numerator = n
            denominator = d * (10 ** exp)
        else:
            # n / (10**exp) / d = n * (10**(-exp)) / d
            numerator = n * (10 ** (-exp))
            denominator = d
        
        # 调整到 [1, 10)
        while numerator >= denominator * 10:
            denominator *= 10
            exp += 1
        while numerator < denominator:
            numerator *= 10
            exp -= 1
        
        # 计算 mantissa 浮点值（此时 numerator 和 denominator 都很小）
        mantissa = Frac(numerator, denominator)
        self._mantissa = mantissa
        mantissa = repr(mantissa)
        self._exp = exp
        return f"{mantissa}e{exp}"        

    def __repr__(self):
        try:
            if self.d == 1:
                return f"Frac({self.n})"
            return f"Frac({self.n}, {self.d})"

        except:
            if not hasattr(self, '_exp'):
                str(self)
            mantissa = self._mantissa
            if mantissa < 1:
                mantissa.n = 10*mantissa.n
            else:
                self._exp += 1
            return f"Frac({mantissa.n} ** {'(' if self._exp < 0 else ''}{self._exp}{')' if self._exp < 0 else ''}, {mantissa.d})"
            
    
    def _to_frac(self, other):
        """将其他类型转换为分数"""
        if isinstance(other, Frac):
            return other
        if isinstance(other, str) and not "e" in other.lower():
            other = float(other)
        if isinstance(other, float) and is_int(other) and not "e" in str(other).lower():
            return Frac(other, 1)
        if isinstance(other, int):
            return Frac(other, 1)
        if isinstance(other, (float, int, str)):
            if isinstance(other, (float, str, int)):
                # 转成整数处理 (1.23 -> 123/100)
                s = str(other)

                if 'e' not in s.lower():  # 暂不考虑科学计数法
                    parts = s.split('.')
                    if len(parts) == 2:
                        whole, dec = parts
                        n = int(whole + dec)
                        d = 10 ** len(dec)
                        return Frac(n, d)
                else:
                    # 直接解析
                    coeff, exp = s.lower().split('e')
                    exp = int(exp)

                    # 把系数转成整数分子分母
                    if '.' in coeff:
                        whole, dec = coeff.split('.')
                        n = int(whole + dec)
                        d = 10 ** len(dec)
                    else:
                        n = int(coeff)
                        d = 1

                    # 根据指数调整
                    if exp >= 0:
                        n *= 10 ** exp
                    else:
                        d *= 10 ** (-exp)

                    return Frac(n, d)
                return Frac(other, 1)
        raise TypeError(f"不支持的类型: {type(other)}")
