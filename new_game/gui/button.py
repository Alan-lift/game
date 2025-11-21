import pygame
from typing import Tuple, Optional, Callable, Union
from .base import GUIComponent
from .text import Text

Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

class Button(GUIComponent):
    """按钮组件，支持点击事件、状态切换"""
    def __init__(self,
                 text: str = "按钮",
                 pos: Tuple[int, int] = (0, 0),
                 size: Tuple[int, int] = (100, 40),
                 text_size: int = 20,
                 text_color: Color = (255, 255, 255),
                 normal_bg: Color = (60, 130, 246),
                 hover_bg: Color = (90, 160, 255),
                 press_bg: Color = (30, 100, 220),
                 callback: Optional[Callable] = None):
        """
        初始化按钮组件
        :param text: 按钮文本
        :param pos: 左上角坐标 (x, y)
        :param size: 按钮大小 (宽, 高)
        :param text_size: 文本大小
        :param text_color: 文本颜色
        :param normal_bg: 正常状态背景色
        :param hover_bg: 悬停状态背景色
        :param press_bg: 按压状态背景色
        :param callback: 点击回调函数（无参数）
        """
        super().__init__(pos)
        self.text = text
        self.size = size
        self.callback = callback
        self.rect.size = size  # 更新碰撞矩形

        # 颜色配置
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.press_bg = press_bg

        # 状态标记
        self.is_hover = False
        self.is_pressed = False

        # 文本组件（居中显示）
        self.text_comp = Text(
            text=text,
            pos=(pos[0] + size[0]//2 - (len(text)*text_size//4),
                 pos[1] + size[1]//2 - text_size//2),
            size=text_size,
            color=text_color
        )

    def _get_current_bg(self) -> Color:
        """获取当前状态的背景色"""
        if self.is_pressed:
            return self.press_bg
        elif self.is_hover:
            return self.hover_bg
        return self.normal_bg

    def check_event(self, event: pygame.event.Event):
        """处理事件（外部调用，用于检测点击）"""
        if not self.visible:
            return

        # 鼠标移动事件（检测悬停）
        if event.type == pygame.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)

        # 鼠标按压事件
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        # 鼠标释放事件（触发回调）
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                if self.callback and callable(self.callback):
                    self.callback()
            self.is_pressed = False

    def set_text(self, new_text: str):
        """更新按钮文本"""
        self.text = new_text
        self.text_comp.set_text(new_text)
        # 重新居中文本
        self.text_comp.set_pos((
            self.pos[0] + self.size[0]//2 - (len(new_text)*self.text_comp.font_size//4),
            self.pos[1] + self.size[1]//2 - self.text_comp.font_size//2
        ))

    def set_callback(self, new_callback: Callable):
        """更新点击回调"""
        self.callback = new_callback

    def draw(self, surface: pygame.Surface):
        """绘制按钮"""
        if self.visible:
            # 绘制背景矩形
            pygame.draw.rect(surface, self._get_current_bg(), self.rect)
            # 绘制文本
            self.text_comp.draw(surface)