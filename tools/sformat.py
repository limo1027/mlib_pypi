from .srandom import SimpleRNG
# ======== 转换成指定格式 ========
def to_UUID(obj):
    """任意对象转UUID"""
    return SimpleRNG(str(obj)).uuid()

def superscript(n):
    """数字转上标字符串"""
    n = int(n)
    if 0 <= n <= 9:
        return chr([8304, 185, 178, 179, 8308, 8309, 8310, 8311, 8312, 8313][n])
    result = ""
    for i in str(n):
        result += superscript(i)
    return result

def visual_len(t):
    t = str(t)
    return sum(2 if '\u4e00' <= c <= '\u9fff' else 1 for c in t)
    
def center(s, width):
    """按视觉宽度居中对齐（粗略版：中文算2，英文算1）"""
    s = str(s)
    s_len = visual_len(s)
    padding = width - s_len
    left = padding // 2
    right = padding - left
    return ' ' * left + s + ' ' * right

def table(data, header=True, border_style="unicode"):
    """精美表格"""
    if not data:
        return ""
    
    # 确定表头和数据
    if header:
        table_data = data
    else:
        table_data = [data[0]] if data else []
    
    # 计算列宽
    col_widths = []
    for col in range(len(table_data[0])):
        max_width = max(sum(visual_len(i) for i in row) for row in table_data)
        col_widths.append(max_width + 2)  # 左右各加1空格
    
    # 边框字符集
    styles = {
        "unicode": {
            "top_left": "┌", "top_mid": "┬", "top_right": "┐",
            "mid_left": "├", "mid_mid": "┼", "mid_right": "┤",
            "bottom_left": "└", "bottom_mid": "┴", "bottom_right": "┘",
            "hline": "─", "vline": "│", "header_mid": "┼"
        },
        "ascii": {
            "top_left": "+", "top_mid": "+", "top_right": "+",
            "mid_left": "+", "mid_mid": "+", "mid_right": "+",
            "bottom_left": "+", "bottom_mid": "+", "bottom_right": "+",
            "hline": "-", "vline": "|", "header_mid": "+"
        },
        "double": {
            "top_left": "╔", "top_mid": "╦", "top_right": "╗",
            "mid_left": "╠", "mid_mid": "╬", "mid_right": "╣",
            "bottom_left": "╚", "bottom_mid": "╩", "bottom_right": "╝",
            "hline": "═", "vline": "║", "header_mid": "╬"
        },
        "rounded": {
            "top_left": "╭", "top_mid": "┬", "top_right": "╮",
            "mid_left": "├", "mid_mid": "┼", "mid_right": "┤",
            "bottom_left": "╰", "bottom_mid": "┴", "bottom_right": "╯",
            "hline": "─", "vline": "│", "header_mid": "┼"
        }
    }
    
    s = styles.get(border_style, styles["unicode"])
    
    def make_line(left, mid, right, widths):
        """生成横线"""
        parts = [s["hline"] * w for w in widths]
        return left + mid.join(parts) + right
    
    lines = []
    
    header_cells = []
    widths = []
    for j, val in enumerate(table_data[0]):
        if j == 5:
            header_cells.append(f"{center('...', col_widths[j])}")
            widths.append(col_widths[j])
        if j >= 5 and j < len(table_data[0]) - 5:
            continue
        header_cells.append(f"{center(str(val),col_widths[j])}")
        widths.append(col_widths[j])
    lines.append(make_line(s["top_left"], s["top_mid"], s["top_right"], widths))
    
    lines.append(s["vline"] + s["vline"].join(header_cells) + s["vline"])
    
    lines.append(make_line(s["mid_left"], s["header_mid"], s["mid_right"], widths))
    
    for i, row in enumerate(table_data[1:]):
        cells = []
        if i == 5:
            string = s["vline"] + center(".....", sum(widths) + len(widths) - 1) + s["vline"]
            lines.append(string)
            continue
        elif i > 5 and i < (len(table_data) - 5):
            continue
        else:
            for j, val in enumerate(row):
                if j == 5:
                    cells.append(f"{'...'.center(col_widths[j])}")
                    continue
                if j > 5 and j < len(row) - 5:
                    continue
                cells.append(f"{center(str(val), col_widths[j])}")
        lines.append(s["vline"] + s["vline"].join(cells) + s["vline"])
        if i < len(table_data) - 2:
            lines.append(make_line(s["mid_left"], s["mid_mid"], s["mid_right"], widths))
            
    lines.append(make_line(s["bottom_left"], s["bottom_mid"], s["bottom_right"], widths))
    
    return "\n".join(lines)

def ordinal(number):
    """数字转序数字符串"""
    try:
        number = int(number)
    except:
        raise ValueError(f"不支持的类型: {type(number)}")

    # 先处理 11,12,13
    if 10 <= number % 100 <= 20:
        return str(number) + "th"
    
    if number == 1:
        return str(number) + "st"
    elif number == 2:
        return str(number) + "nd"
    elif number == 3:
        return str(number) + "rd"
    elif number < 10:
        return str(number) + "th"
    else:
        return str(number)[:-1] + ordinal(str(number)[-1:])

def to_poly(expr, use_star=False):
    """表达式转多项式字符串"""
    if not expr:
        return expr

    expr = expr.replace("^", "**")
    expr = expr.replace(" ", "")

    terms = []
    current = ""
    for char in expr:
        if char == '+' and current:
            terms.append(current)
            current = ""
        elif char == '-' and current:
            terms.append(current)
            current = "-"
        else:
            current += char
    if current:
        terms.append(current)

    parsed_terms = {}  # 变量部分 -> 系数

    for term in terms:
        if not term:
            continue

        var_start = -1
        for i, char in enumerate(term):
            if char.isalpha():
                var_start = i
                break

        if var_start == -1:
            coeff = float(term) if '.' in term else int(term)
            parsed_terms[""] = parsed_terms.get("", 0) + coeff
            continue

        # 系数部分
        coeff_str = term[:var_start]
        if not coeff_str or coeff_str == '+':
            coeff = 1
        elif coeff_str == '-':
            coeff = -1
        else:
            coeff = float(coeff_str) if '.' in coeff_str else int(coeff_str)

        # 变量部分
        var_part = term[var_start:]

        # 处理 x10 的情况
        if len(var_part) > 1 and var_part[0].isalpha() and var_part[1:].isdigit():
            extra_coeff = int(var_part[1:])
            coeff *= extra_coeff
            var_part = var_part[0]

        parsed_terms[var_part] = parsed_terms.get(var_part, 0) + coeff

    result_terms = []

    for var in sorted(parsed_terms.keys()):
        if var == "":
            continue
        coeff = parsed_terms[var]
        if coeff == 0:
            continue

        if coeff == 1:
            coeff_str = ""
        elif coeff == -1:
            coeff_str = "-"
        else:
            coeff_str = str(coeff)

        if use_star:
            var_str = var.replace("**", "^")
        else:
            var_str = var

        if coeff_str:
            if use_star:
                result_terms.append(f"{coeff_str}{var_str}")
            else:
                result_terms.append(f"{coeff_str}*{var_str}")
        else:
            result_terms.append(var_str)

    if "" in parsed_terms and parsed_terms[""] != 0:
        result_terms.append(str(parsed_terms[""]))

    if not result_terms:
        return "0"

    result = result_terms[0]
    for term in result_terms[1:]:
        if term.startswith('-'):
            result += term
        else:
            result += "+" + term

    return result

# ============ 中英文转换 ===========

def number_to_english(n):
    """把整数转成英语单词形式，适合对话文本"""
    if n == 0:
        return "zero"

    # 1-19 特殊形式
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
             "seventeen", "eighteen", "nineteen"]

    # 整十
    tens = ["", "", "twenty", "thirty", "forty", "fifty",
            "sixty", "seventy", "eighty", "ninety"]

    # 千以上单位
    thousands = ["", "thousand", "million", "billion", "trillion",
                 "quadrillion", "quintillion", "sextillion", "septillion",
                 "octillion", "nonillion", "decillion"]

    def _convert_three_digits(num):
        """处理 1-999"""
        if num == 0:
            return ""
        if num < 20:
            return units[num]
        if num < 100:
            ten = tens[num // 10]
            unit = units[num % 10]
            return ten + ("-" + unit if unit else "")
        # 100-999
        hundred = units[num // 100] + " hundred"
        rest = num % 100
        if rest == 0:
            return hundred
        return hundred + " and " + _convert_three_digits(rest)

    if n < 0:
        return "negative " + number_to_english(-n)

    result = []
    group_index = 0
    while n > 0:
        group = n % 1000
        if group != 0:
            group_str = _convert_three_digits(group)
            if thousands[group_index]:
                group_str += " " + thousands[group_index]
            result.insert(0, group_str)
        n //= 1000
        group_index += 1

    return " ".join(result).strip()

def english_to_number(s):
    """把英语单词形式转成整数，适合解析对话文本"""
    if not s or s.strip() == "":
        return 0

    s = s.strip().lower().replace("-", " ").replace(" and ", " ")

    # 处理负数
    if s.startswith("negative "):
        return -english_to_number(s[9:])

    if s == "zero":
        return 0

    # 单词映射表
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19
    }

    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }

    scales = {
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        "billion": 1000000000,
        "trillion": 1000000000000,
        "quadrillion": 1000000000000000,
        "quintillion": 1000000000000000000,
        "sextillion": 10**21,
        "septillion": 10**24,
        "octillion": 10**27,
        "nonillion": 10**30,
        "decillion": 10**33
    }

    words = s.split()
    total = 0
    current = 0

    i = 0
    while i < len(words):
        word = words[i]

        # 处理 1-19
        if word in units:
            current += units[word]

        # 处理整十
        elif word in tens:
            current += tens[word]

        # 处理 hundred
        elif word == "hundred":
            current *= 100

        # 处理千以上单位
        elif word in scales:
            if current == 0:
                current = 1
            total += current * scales[word]
            current = 0

        # 处理带连字符的 twenty-one 之类的（已经替换成空格）
        i += 1

    return total + current

def insert(base_str, place, insert_str):
    """在字符串位置插入子字符串"""
    pos = place
    new_s = base_str[:pos] + insert_str + base_str[pos:]
    return new_s



# ============ 编码/解码 ===========

def encode(string):
    """编码（将字符串转换为数字序列）"""
    if not string:
        return ""
    codes = []
    for char in string:
        code = ord(char)
        code_str = str(code)
        length_param = len(code_str)
        codes.append(str(length_param))
        codes.append(code_str)
    return ''.join(codes)

def decode(encoded):
    """解码（即使被截断也能尽量恢复）"""
    result = ""
    i = 0
    chars_decoded = 0
    warning = None
    while i < len(encoded):
        # 检查是否还有足够长度读长度标记
        if i + 1 > len(encoded):
            warning = f"警告: 长度标记被截断，已解码 {chars_decoded} 个字符"
            break

        length_param = int(encoded[i])
        i += 1

        # 检查是否还有足够长度读数据
        if i + length_param > len(encoded):
            warning = f"警告: 第{chars_decoded+1}个字符的数据被截断"
            break

        code_str = encoded[i:i + length_param]
        if not code_str.isdigit():
            warning = "检测到编码意外被修改 - 不是全数字"
            break
        i += length_param
        if not int(code_str) <= 1114111:
            warning = "检测到编码意外被修改 - 数字过大"
            break
        result += chr(int(code_str))
        chars_decoded += 1
    if warning:
        return result, warning
    else:
        return result

