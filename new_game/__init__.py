"""
一个较为简单的2D的创建游戏的库
"""
# 暴露核心类和函数，简化导入
from .core.camera import carom
from .core.map import game_map
from .core.entity import player, noplayer
from .core.window import Windows_window
from .core.background import way
from .core.sound import SoundSystem
from .gui.text import Text
from .gui.button import Button
from .gui.image import Image
from .utils.common import clean_component as clean

__all__ = [
    # 核心组件
    'carom',
    'game_map',
    'player',
    'noplayer',
    'Windows_window',
    'way',
    'SoundSystem',
    # GUI组件
    'Text',
    'Button',
    'Image',
    # 工具函数
    'clean'
]