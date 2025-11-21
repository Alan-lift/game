import pygame
from typing import Tuple, Optional

class GUIComponent:
    """GUI组件基类，统一接口和基础属性"""
    def __init__(self, pos: Tuple[int, int] = (0, 0)):
        self.pos = pos  # 组件左上角坐标（窗口绝对位置）
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)  # 碰撞矩形
        self.visible = True  # 是否可见

    def set_pos(self, new_pos: Tuple[int, int]):
        """更新组件位置"""
        self.pos = new_pos
        self.rect.topleft = new_pos

    def set_visible(self, visible: bool):
        """设置组件是否可见"""
        self.visible = visible

    def draw(self, surface: pygame.Surface):
        """绘制组件（子类必须实现）"""
        raise NotImplementedError("子类必须实现draw方法")

    def update(self):
        """更新组件状态（子类可选实现）"""
        pass