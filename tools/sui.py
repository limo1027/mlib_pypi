# sui.py - 极简UI组件（依赖sgeometry.Rect）
# 三个组件：Label, Button, Bar

from .sgeometry import Rect

class Label:
    """文本标签"""

    def __init__(self, x, y, width, height, text="", **kwargs):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = kwargs.get('color', (240, 240, 240))
        self.text_color = kwargs.get('text_color', (0, 0, 0))
        self.align = kwargs.get('align', 'left')  # left/center/right
        self.visible = True

    def render(self):
        """返回绘制指令"""
        if not self.visible:
            return []

        cmds = []

        # 背景
        cmds.append({
            'type': 'rect',
            'rect': self.rect,  # 直接传Rect对象
            'color': self.color
        })

        # 文字位置计算
        text_x = self.rect.x + 5  # 默认 left
        if self.align == 'center':
            text_x = self.rect.x + (self.rect.w - len(self.text) * 8) // 2
        elif self.align == 'right':
            text_x = self.rect.right - len(self.text) * 8 - 5

        cmds.append({
            'type': 'text',
            'text': self.text,
            'x': text_x,
            'y': self.rect.y + (self.rect.h - 12) // 2,
            'color': self.text_color
        })

        return cmds

    def destroy(self):
        self.visible = False

    def config(self, **kwargs):
        for k, v in kwargs.items():
            if k in ('x', 'y', 'width', 'height'):
                setattr(self.rect, k, v)
            elif hasattr(self, k):
                setattr(self, k, v)

    def enter(self, mouse_x, mouse_y):
        """鼠标是否进入"""
        return self.rect.collide_point(mouse_x, mouse_y)


class Button:
    """按钮"""

    def __init__(self, x, y, width, height, text="", **kwargs):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = kwargs.get('color', (200, 200, 200))
        self.hover_color = kwargs.get('hover_color', (220, 220, 220))
        self.press_color = kwargs.get('press_color', (160, 160, 160))
        self.text_color = kwargs.get('text_color', (0, 0, 0))
        self.border = kwargs.get('border', True)
        self.radius = kwargs.get('radius', 3)
        self.visible = True

        # 状态
        self.hover = False
        self.pressed = False

    def render(self):
        if not self.visible:
            return []

        cmds = []

        # 根据状态选颜色
        if self.pressed:
            bg = self.press_color
        elif self.hover:
            bg = self.hover_color
        else:
            bg = self.color

        # 背景
        cmds.append({
            'type': 'rect',
            'rect': self.rect,
            'color': bg,
            'radius': self.radius
        })

        # 边框
        if self.border:
            cmds.append({
                'type': 'outline',
                'rect': self.rect,
                'color': (100, 100, 100),
                'radius': self.radius
            })

        # 文字（居中）
        text_x = self.rect.x + (self.rect.w - len(self.text) * 8) // 2
        text_y = self.rect.y + (self.rect.h - 12) // 2
        cmds.append({
            'type': 'text',
            'text': self.text,
            'x': text_x,
            'y': text_y,
            'color': self.text_color
        })

        return cmds

    def destroy(self):
        self.visible = False

    def config(self, **kwargs):
        for k, v in kwargs.items():
            if k in ('x', 'y', 'width', 'height'):
                setattr(self.rect, k, v)
            elif hasattr(self, k):
                setattr(self, k, v)

    def enter(self, mouse_x, mouse_y):
        """更新悬停状态并返回是否进入"""
        was_hover = self.hover
        self.hover = self.rect.collide_point(mouse_x, mouse_y)
        return self.hover

    def press(self):
        """按下"""
        self.pressed = True

    def release(self):
        """释放"""
        self.pressed = False
        if self.hover:
            return True  # 点击完成
        return False


class Bar:
    """血量条/进度条"""

    def __init__(self, x, y, width, height, value=1.0, **kwargs):
        self.rect = Rect(x, y, width, height)
        self.value = max(0.0, min(1.0, value))  # 0-1
        self.bg_color = kwargs.get('bg_color', (60, 60, 60))
        self.fill_color = kwargs.get('fill_color', (255, 50, 50))
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        self.show_text = kwargs.get('show_text', True)
        self.orientation = kwargs.get('orientation', 'horizontal')
        self.visible = True

    def render(self):
        if not self.visible:
            return []

        cmds = []

        # 背景
        cmds.append({
            'type': 'rect',
            'rect': self.rect,
            'color': self.bg_color
        })

        # 填充部分
        if self.orientation == 'horizontal':
            fill_rect = Rect(
                self.rect.x,
                self.rect.y,
                int(self.rect.w * self.value),
                self.rect.h
            )
        else:  # 垂直
            fill_h = int(self.rect.h * self.value)
            fill_rect = Rect(
                self.rect.x,
                self.rect.y + self.rect.h - fill_h,
                self.rect.w,
                fill_h
            )

        cmds.append({
            'type': 'rect',
            'rect': fill_rect,
            'color': self.fill_color
        })

        # 显示百分比
        if self.show_text:
            text = f"{int(self.value * 100)}%"
            text_x = self.rect.x + (self.rect.w - len(text) * 8) // 2
            text_y = self.rect.y + (self.rect.h - 12) // 2
            cmds.append({
                'type': 'text',
                'text': text,
                'x': text_x,
                'y': text_y,
                'color': self.text_color
            })

        return cmds

    def destroy(self):
        self.visible = False

    def config(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'value':
                self.value = max(0.0, min(1.0, v))
            elif k in ('x', 'y', 'width', 'height'):
                setattr(self.rect, k, v)
            elif hasattr(self, k):
                setattr(self, k, v)

    def enter(self, mouse_x, mouse_y):
        """鼠标是否进入"""
        return self.rect.collide_point(mouse_x, mouse_y)

    def set_hp(self, current, max_hp):
        """快捷设置血量"""
        self.value = current / max_hp
