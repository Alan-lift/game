import pygame
from typing import List
from .camera import carom

class way:
    """背景类，管理多层背景元素"""
    def __init__(self, game_map, images_list: list[tuple[list[int], str, int]]):
        self.game_map = game_map
        self.carom = game_map.carom
        self.elements = []

        # 加载背景元素（格式：[[x,y], 图片路径, 图层]）
        for elem in images_list:
            pos, img_path, layer = elem
            try:
                image = pygame.image.load(img_path).convert_alpha()
                self.elements.append({
                    'pos': pos,
                    'image': image,
                    'layer': layer,
                    'rect': pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
                })
            except Exception as e:
                print(f"加载背景图片失败 {img_path}: {e}")

        # 按图层排序：图层值越大越靠下
        self.elements.sort(key=lambda x: -x['layer'])

    def draw(self, surface: pygame.Surface):
        """绘制背景（考虑相机偏移）"""
        for elem in self.elements:
            draw_pos = (elem['pos'][0] - self.carom.x, elem['pos'][1] - self.carom.y)
            surface.blit(elem['image'], draw_pos)