import pygame
from typing import Tuple, Optional, Union
from .base import GUIComponent

class Image(GUIComponent):
    """图片组件，支持缩放、透明度调整"""
    def __init__(self,
                 img_path: str,
                 pos: Tuple[int, int] = (0, 0),
                 size: Optional[Tuple[int, int]] = None,
                 alpha: int = 255):
        """
        初始化图片组件
        :param img_path: 图片路径
        :param pos: 左上角坐标 (x, y)
        :param size: 缩放大小 (宽, 高)（None使用原图大小）
        :param alpha: 透明度（0-255）
        """
        super().__init__(pos)
        self.img_path = img_path
        self.alpha = alpha
        self.image = self._load_and_process_image(size)

    def _load_and_process_image(self, size: Optional[Tuple[int, int]]) -> pygame.Surface:
        """加载并处理图片（缩放+透明度）"""
        try:
            # 加载图片（支持透明）
            img = pygame.image.load(self.img_path).convert_alpha()
            # 缩放图片
            if size:
                img = pygame.transform.scale(img, size)
            # 设置透明度
            img.set_alpha(self.alpha)
            # 更新碰撞矩形
            self.rect.size = img.get_size()
            return img
        except Exception as e:
            print(f"图片加载失败 {self.img_path}: {e}")
            # 生成红色占位图
            placeholder_size = size or (64, 64)
            placeholder = pygame.Surface(placeholder_size, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 0, 0, 128), placeholder.get_rect())
            self.rect.size = placeholder_size
            return placeholder

    def set_size(self, new_size: Tuple[int, int]):
        """缩放图片"""
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect.size = new_size

    def set_alpha(self, new_alpha: int):
        """调整透明度（0-255）"""
        self.alpha = max(0, min(255, new_alpha))
        self.image.set_alpha(self.alpha)

    def draw(self, surface: pygame.Surface):
        """绘制图片"""
        if self.visible:
            surface.blit(self.image, self.pos)