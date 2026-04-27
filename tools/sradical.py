# sradical.py - 嵌套根式表达式系统
from .sformat import superscript
class Radical:
    """
    嵌套根式类
    
    表示法：
        - 常数: Radical(5)
        - 根式: Radical(2, 2, 5)  → 5√2
        - 根式: Radical(2, 2)     → √2（系数默认1）
        - 嵌套: Radical(2, Radical(2, 2) + 1, 2) → 2√(√2+1)
    """
    
    def __init__(self, *args):
        if len(args) == 1:
            # 常数
            self._type = 'const'
            self._value = args[0]
            self._degree = None
            self._inner = None
            self._coeff = None
            self._terms = None
            
        elif len(args) == 2:
            # 根式（系数默认1）
            degree, inner = args
            self._type = 'radical'
            self._degree = degree
            self._inner = inner if isinstance(inner, Radical) else Radical(inner)
            self._coeff = 1.0
            self._value = None
            self._terms = None
            
        elif len(args) == 3:
            # 根式（指定系数）
            degree, inner, coeff = args
            self._type = 'radical'
            self._degree = degree
            self._inner = inner if isinstance(inner, Radical) else Radical(inner)
            self._coeff = float(coeff)
            self._value = None
            self._terms = None
            
        else:
            raise ValueError("参数数量错误")
        
        self._hash_cache = None
        self._simplify()
    
    
    def __hash__(self):
        """使 Radical 可哈希"""
        if self._hash_cache is None:
            self._hash_cache = hash(self._to_hashable())
        return self._hash_cache
    
    def _to_hashable(self):
        """转换为可哈希的类型"""
        if self._type == 'const':
            return ('const', self._value)
        if self._type == 'radical':
            return ('radical', self._degree, self._inner, self._coeff)
        if self._type == 'sum':
            # 加法需要排序后转元组
            return ('sum', tuple(sorted((t._to_hashable() for t in self._terms), key=str)))
        return None

    def __pow__(self, other):
        # 支持整数、分数、小数
        if isinstance(other, (int, float)):
            # 小数转分数
            frac = self._float_to_frac(other)
            # a^(p/q) = (a^p) 再开 q 次方
            if frac.d != 1:
                return Radical(frac.d, self ** frac.n)
            # 整数指数走原来的逻辑
            return self._int_pow(frac.n)
        
        if isinstance(other, Frac):
            return Radical(other.d, self ** other.n)
        
        raise ValueError("不支持无理数次幂")

    def _float_to_frac(self, f):
        """0.5 -> Frac(1,2), 1.5 -> Frac(3,2)"""
        from .sfrac import Frac
        return Frac(f)
            
    def _int_pow(self, other):
        if other == 0:
            if self._is_zero():
                raise ValueError("0^0 无意义")
            return Radical(1)
        
        if other == 1:
            return self
        
        if self._is_zero():
            return Radical(0)
        
        if other > 0:
            result = self
            for _ in range(other - 1):
                result = result * self
            return result
        
        if other < 0:
            if self._type == 'sum':
                raise ValueError("不支持表达式负指数")
            # 负指数：倒数再正指数
            return self / self ** (-other+1)
        
    
    def _integer_root(self, n, degree):
        """检查 n 是否为整数的 degree 次方，返回那个整数，否则返回 None"""
        n = int(n)
        if n < 0:
            if degree % 2 == 1:
                root = self._integer_root(-n, degree)
                return -root if root else None
            return None
        
        # 二分查找整数根
        low, high = 0, n + 1
        while low <= high:
            mid = (low + high) // 2
            power = mid ** degree
            if power == n:
                return mid
            elif power < n:
                low = mid + 1
            else:
                high = mid - 1
        return None
    
    def _simplify_radicand(self, n, degree):
        """化简根号内的数字：√(a^degree · b) → a·√b，返回 b"""
        if n <= 0:
            return n
        
        n = int(n)
        best_factor = 1
        i = 2
        while i ** degree <= n:
            while n % (i ** degree) == 0:
                best_factor *= i
                n //= (i ** degree)
            i += 1
        
        return n
    
    def _simplify(self):
        """化简自身"""
        
        if self._type == 'const':
            return
        
        if self._type == 'radical':
            if self._inner:
                self._inner._simplify()
            
            if self._inner._is_zero():
                self._type = 'const'
                self._value = 0.0
                self._hash_cache = None
                return
            
            if abs(self._coeff) < 1e-12:
                self._type = 'const'
                self._value = 0.0
                self._hash_cache = None
                return
            
            if self._inner._type == 'const':
                inner_val = self._inner._value
                if inner_val < 0 and self._degree % 2 == 0:
                    pass
                elif abs(inner_val) < 1e-12:
                    self._type = 'const'
                    self._value = 0.0
                    self._hash_cache = None
                    return
                return
        
        if self._type == 'sum':
            new_terms = []
            for term in self._terms:
                term._simplify()
                if term._is_zero():
                    continue
                if term._type == 'sum':
                    # 扁平化
                    new_terms.extend(term._terms)
                else:
                    new_terms.append(term)
            
            merged = {}
            for term in new_terms:
                key = term._key()
                if key in merged:
                    merged[key] = self._add_terms(merged[key], term)
                else:
                    merged[key] = term
            
            # 过滤零
            result = [v for v in merged.values() if not v._is_zero()]
            
            if len(result) == 0:
                self._type = 'const'
                self._value = 0.0
                self._hash_cache = None
            elif len(result) == 1:
                r = result[0]
                self._type = r._type
                self._value = r._value
                self._degree = r._degree
                self._inner = r._inner
                self._coeff = r._coeff
                self._terms = r._terms
                self._hash_cache = None
            else:
                self._terms = result
                self._hash_cache = None
                
        if isinstance(self._inner, (int, float)) or (hasattr(self._inner, "_type") and self._inner._type == 'const'):
            if isinstance(self._inner, (int, float)):
                inner_val = self._inner
                
            else:
                inner_val = self._inner._value
            
            if inner_val < 0 and self._degree % 2 == 0:
                return
            
            if inner_val >= 0:
                root_val = self._integer_root(inner_val, self._degree)
                if not root_val is None:

                    constant = root_val * self._coeff
                    self._type = 'const'
                    self._value = float(constant)
                    self._hash_cache = None
                    return
            
            simplified = self._simplify_radicand(inner_val, self._degree)
            if simplified != inner_val:
                self._inner = Radical(simplified)
                self._coeff = self._coeff * (inner_val / simplified) ** (1 / self._degree)
                self._simplify()
                return
            
    def _key(self):
        """返回合并用的键（可哈希）"""
        if self._type == 'const':
            return ('const',)
        if self._type == 'radical':
            return ('radical', self._degree, self._inner,)
        return None
    
    def _add_terms(self, a, b):
        """合并两个同类项"""
        if a._type == 'const' and b._type == 'const':
            return Radical(a._value + b._value)
        
        if a._type == 'radical' and b._type == 'radical':
            if a._degree == b._degree and a._inner == b._inner:
                return Radical(a._degree, a._inner, a._coeff + b._coeff)
        
        return a
    
    def _is_zero(self):
        if self._type == 'const':
            return abs(self._value) < 1e-12
        if self._type == 'sum':
            return len(self._terms) == 0
        if self._type == 'radical':
            return abs(self._coeff) < 1e-12
        return False
    
    def _is_one(self):
        if self._type == 'const':
            return abs(self._value - 1.0) < 1e-12
        return False
    
    def _is_const(self):
        return self._type == 'const'
    
    def _is_radical(self):
        return self._type == 'radical'
    
    def _is_sum(self):
        return self._type == 'sum'
    
    def _const_value(self):
        return self._value if self._type == 'const' else 0.0
    
    
    def __add__(self, other):
        if not isinstance(other, Radical):
            other = Radical(other)
        
        if self._is_zero():
            return other
        if other._is_zero():
            return self
        
        return Radical._make_sum([self, other])
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return self.__add__(-other)
    
    def __rsub__(self, other):
        return Radical(other) - self
    
    def __neg__(self):
        if self._type == 'const':
            return Radical(-self._value)
        if self._type == 'radical':
            return Radical(self._degree, self._inner, -self._coeff)
        if self._type == 'sum':
            return Radical._make_sum([-t for t in self._terms])
        return Radical(0)
    
    def __mul__(self, other):
        """乘法"""
        if not isinstance(other, Radical):
            other = Radical(other)
        
        if self._is_zero() or other._is_zero():
            return Radical(0)
        
        if self._is_one():
            return other
        if other._is_one():
            return self
        
        if self._is_const() and other._is_const():
            return Radical(self._value * other._value)
        
        if self._is_const():
            if other._type == 'radical':
                return Radical(other._degree, other._inner, self._value * other._coeff)
            if other._type == 'sum':
                multiplied = [self * t for t in other._terms]
                return Radical._make_sum(multiplied)
            if other._type == 'power':
                r = Radical(0)
                r._type = 'power'
                r._base = other._base
                r._coeff = self._value * other._coeff if hasattr(other, '_coeff') else self._value
                return r
        
        if other._is_const():
            return other * self
        
        if self._is_radical() and other._is_radical() and self._degree == other._degree:
            inner_prod = self._inner * other._inner
            return Radical(self._degree, inner_prod, self._coeff * other._coeff)
        
        if self._is_radical() and other._is_radical():
            return Radical._make_mul(self, other)
        
        if self._is_sum() and other._is_sum():
            results = []
            for a in self._terms:
                for b in other._terms:
                    results.append(a * b)
            return Radical._make_sum(results)

        if self._is_sum():
            multiplied = [t * other for t in self._terms]
            return Radical._make_sum(multiplied)
        
        if other._is_sum():
            return self * other  # 会走到上面的分支
        
        # 根式 * 其他
        if self._is_radical():
            return Radical._make_mul(self, other)
        
        # 默认情况
        return Radical._make_mul(self, other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def _distribute(self, a, b):
        if a._is_sum():
            terms = a._terms
        else:
            terms = [a]
        
        results = []
        for term in terms:
            results.append(term * b)
        
        return Radical._make_sum(results)
    
    def __truediv__(self, other):
        """除法 self / other"""
        if not isinstance(other, Radical):
            other = Radical(other)
        
        if other._is_zero():
            raise ZeroDivisionError("division by zero")
        
        if self._is_zero():
            return Radical(0)
        
        if other._is_one():
            return self
        
        if self._is_const() and other._is_const():
            return Radical(self._value / other._value)
        
        if self._is_const():
            return self * (other ** -1)
        
        if other._is_const():
            if self._type == 'radical':
                return Radical(self._degree, self._inner, self._coeff / other._value)
            if self._type == 'sum':
                return Radical._make_sum([t / other for t in self._terms])
        
        if self._is_radical() and other._is_radical() and self._degree == other._degree:

            inner_div = self._inner / other._inner
            new_coeff = self._coeff / other._coeff
            return Radical(self._degree, inner_div, new_coeff)
        
        return self * (other ** -1)
    
    def __rtruediv__(self, other):
        """右除法 other / self"""
        return Radical(other) / self
    
    def __eq__(self, other):
        if not isinstance(other, Radical):
            other = Radical(other)
        return self._to_hashable() == other._to_hashable()
    
    # ========== 静态方法 ==========
    
    @staticmethod
    def _make_sum(terms):
        """创建加法表达式"""
        r = Radical(0)
        r._type = 'sum'
        r._terms = list(terms)
        r._simplify()
        return r
    
    @staticmethod
    def _make_mul(a, b):
        """创建乘法表达式"""
        r = Radical(0)
        r._type = 'mul'
        r._left = a
        r._right = b
        return r
    
    # ========== 字符串 ==========
    
    def __repr__(self, child=False):
        if self._type == 'const':
            if abs(self._value - int(self._value)) < 1e-12:
                return repr(int(self._value))
            s = f"{self._value:.10f}".rstrip('0').rstrip('.')
            return s
        
        if self._type == 'radical':
            inner_str = repr(self._inner)
            if self._inner._type in ('sum', 'radical'):
                inner_str = f"({inner_str})"
            
            if self._degree == 2:
                root_symbol = "√"
            else:
                root_symbol = f"{' · ' if child else ''}{superscript(self._degree)}√"
            
            root = f"{root_symbol}{inner_str}"
            
            if abs(self._coeff - 1.0) < 1e-12:
                return root
            if abs(self._coeff + 1.0) < 1e-12:
                return f"-{root}"
            
            # 系数显示为整数或浮点
            if abs(self._coeff - int(self._coeff)) < 1e-12:
                coeff_str = repr(int(self._coeff))
            else:
                coeff_str = f"{self._coeff:.6f}".rstrip('0').rstrip('.')
            
            return f"{coeff_str}{root}"
        if self._type == 'mul':
            left_val = self._left._approx_value()
            right_val = self._right._approx_value()
            return left_val * right_val
        
        if self._type == 'sum':
            # 加法表达式，逐项显示
            terms_str = []
            for term in self._terms:
                try:
                    term_str = term.__repr__(child=True)
                except:
                    term_str = repr(term)
                # 如果项是负数，已经带了负号
                if term_str.startswith('-'):
                    terms_str.append(term_str)
                else:
                    terms_str.append(f"+ {term_str}")
            
            # 第一项不加加号
            if terms_str[0].startswith("+ "):
                result = terms_str[0][2:]
            else:
                result = terms_str[0]
            if result.startswith(" · "):
                result = result[3:]
                
            for ts in terms_str[1:]:
                if ts.startswith('+ '):
                    result += f" {ts}"
                else:
                    result += f" {ts}"
            return result
        
        return "?"
    
    # ========== 近似值 ==========
    
    def approx(self, digits=None):
        """计算数值近似"""
        result = self._approx_value()
        
        if digits is not None:
            return round(result, digits)
        return result


    def _approx_value(self):
        """递归计算内部值"""
        
        if self._type == 'const':
            return self._value
        
        if self._type == 'radical':
            inner_val = self._inner._approx_value()
            
            sign = 1
            if inner_val < 0:
                sign = -1
                inner_val = -inner_val
            
            try:
                from .smath import exp, log
            except:
                from smath import exp, log
            root_val = exp(log(inner_val) / self._degree)
            
            # 恢复符号
            root_val = sign * root_val
            
            # 乘以系数
            return root_val * self._coeff
        
        if self._type == 'sum':
            # 求和
            total = 0.0
            for term in self._terms:
                total += term._approx_value()
            return total


    def __float__(self):
        """支持 float() 转换"""
        return self._approx_value()


    def __int__(self):
        """支持 int() 转换"""
        return int(self._approx_value())


    def __abs__(self):
        """绝对值"""
        val = self._approx_value()
        if val < 0:
            return -self
        return self
        
