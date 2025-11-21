import pygame
from typing import Tuple, Optional, Union
from .base import GUIComponent

Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

class Text(GUIComponent):
    """文本组件，支持字体、颜色、背景自定义"""
    def __init__(self,
                 text: str = "",
                 pos: Tuple[int, int] = (0, 0),
                 size: int = 24,
                 color: Color = (255, 255, 255),
                 bg_color: Optional[Color] = None,
                 font_path: Optional[str] = None):
        """
        初始化文本组件
        :param text: 显示文本
        :param pos: 左上角坐标 (x, y)
        :param size: 字体大小
        :param color: 字体颜色（RGB/RGBA）
        :param bg_color: 背景颜色（None为透明）
        :param font_path: 自定义字体路径（None使用系统默认）
        """
        super().__init__(pos)
        self.text = text
        self.font_size = size
        self.color = color
        self.bg_color = bg_color
        self.font = self._load_font(font_path)
        self.surface = self._render_text()

    def _load_font(self, font_path: Optional[str]) -> pygame.font.Font:
        """加载字体"""
        try:
            if font_path:
                return pygame.font.Font(font_path, self.font_size)
            return pygame.font.SysFont(None, self.font_size)
        except Exception as e:
            print(f"字体加载失败：{e}，使用默认字体")
            return pygame.font.SysFont(None, self.font_size)

    def _render_text(self) -> pygame.Surface:
        """渲染文本表面"""
        if self.bg_color:
            surface = self.font.render(self.text, True, self.color, self.bg_color)
        else:
            surface = self.font.render(self.text, True, self.color)
        # 更新碰撞矩形
        self.rect.size = surface.get_size()
        return surface

    def set_text(self, new_text: str):
        """更新文本内容"""
        self.text = new_text
        self.surface = self._render_text()

    def set_color(self, new_color: Color):
        """更新字体颜色"""
        self.color = new_color
        self.surface = self._render_text()

    def set_font_size(self, new_size: int):
        """更新字体大小"""
        self.font_size = new_size
        self.font = self._load_font(None)
        self.surface = self._render_text()

    def draw(self, surface: pygame.Surface):
        """绘制文本"""
        if self.visible:
            surface.blit(self.surface, self.pos)