import pygame
import time
import math
from typing import List, Callable, Optional, Tuple
from .camera import carom
from .map import game_map

class EntityBase:
    """实体基类，封装玩家和非玩家实体的共同功能"""
    def __init__(self, game_map: game_map, images: list[list[str]], to_time: int,
                 tuceng: int = 1, down: int = 1, lift: int = 100):
        self.game_map = game_map
        self.carom = game_map.carom
        self.to_time = to_time  # 动画刷新间隔（毫秒）
        self.tuceng = tuceng  # 图层（默认1）
        self.down = down  # 自动移动速度（每秒x减down像素）
        self.lift = lift  # 当前生命值
        self.max_lift = lift  # 最大生命值
        self.active = True  # 是否活跃

        # 初始位置（地图中心）
        self.x = game_map.rize_x // 2
        self.y = game_map.rize_y // 2
        self.direction = 'stop'  # 当前方向（forword/back/left/right/stop）
        self.frame_index = 0  # 动画帧索引
        self.last_update = pygame.time.get_ticks()  # 上次动画更新时间
        self.last_auto_move = time.time()  # 上次自动移动时间

        # 加载动画帧（images格式：[前进,后退,向左,向右,静止]）
        self.images = {
            'forword': self._load_images(images[0]),
            'back': self._load_images(images[1]),
            'left': self._load_images(images[2]),
            'right': self._load_images(images[3]),
            'stop': self._load_images(images[4])
        }

        # 碰撞矩形（基于静止帧大小）
        self.width = self.images['stop'][0].get_width() if self.images['stop'] else 32
        self.height = self.images['stop'][0].get_height() if self.images['stop'] else 32
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def _load_images(self, image_paths: List[str]) -> List[pygame.Surface]:
        """加载单方向的动画帧图片"""
        images = []
        for path in image_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
                images.append(img)
            except Exception as e:
                print(f"加载实体图片失败 {path}: {e}")
        return images

    def _update_frame(self):
        """更新动画帧"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.to_time:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.images[self.direction])

    def _update_rect(self):
        """更新碰撞矩形位置"""
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2

    def _check_collision(self) -> bool:
        """检查与同图层其他实体的碰撞"""
        for entity in self.carom.entities:
            if (entity != self and entity.active and entity.tuceng == self.tuceng and
                    self.rect.colliderect(entity.rect)):
                return True
        return False

    def auto_move(self):
        """自动移动逻辑：无碰撞时每秒x坐标减down像素"""
        now = time.time()
        if now - self.last_auto_move >= 1.0:
            self.x -= self.down
            # 边界检测
            if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
                self._update_rect()
            else:
                self.x += self.down  # 超出边界则回退
            self.last_auto_move = now

    def forword(self, step: int = 1, images: Optional[List[str]] = None):
        """向前移动（y减小），支持自定义动作图片"""
        if images:
            self.images['forword'] = self._load_images(images)
        self.y -= step
        if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
            self.direction = 'forword'
            self._update_rect()
        else:
            self.y += step  # 超出边界回退

    def back(self, step: int = 1, images: Optional[List[str]] = None):
        """向后移动（y增大），支持自定义动作图片"""
        if images:
            self.images['back'] = self._load_images(images)
        self.y += step
        if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
            self.direction = 'back'
            self._update_rect()
        else:
            self.y -= step

    def left(self, step: int = 1, images: Optional[List[str]] = None):
        """向左移动（x减小），支持自定义动作图片"""
        if images:
            self.images['left'] = self._load_images(images)
        self.x -= step
        if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
            self.direction = 'left'
            self._update_rect()
        else:
            self.x += step

    def right(self, step: int = 1, images: Optional[List[str]] = None):
        """向右移动（x增大），支持自定义动作图片"""
        if images:
            self.images['right'] = self._load_images(images)
        self.x += step
        if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
            self.direction = 'right'
            self._update_rect()
        else:
            self.x -= step

    def stop(self):
        """停止移动，切换到静止动画"""
        self.direction = 'stop'
        self.frame_index = 0

    def get_lift(self) -> int:
        """返回当前生命值（避免与属性名冲突）"""
        return self.lift

    def get_x_y(self) -> tuple[int, int]:
        """返回当前位置（x,y）（避免与方法名冲突）"""
        return (self.x, self.y)

    def set_x_y(self, x: int, y: int):
        """修改位置到指定坐标"""
        self.x = x
        self.y = y
        if self.game_map.check_boundary(self.x, self.y, self.width, self.height):
            self._update_rect()

    def set_lift(self, new_lift: int):
        """修改生命值"""
        self.lift = max(0, min(new_lift, self.max_lift))
        if self.lift <= 0:
            self.active = False

    def draw(self, surface: pygame.Surface):
        """绘制实体和生命值条"""
        if not self.active:
            return

        self._update_frame()
        current_img = self.images[self.direction][self.frame_index]
        draw_pos = (self.x - self.width//2 - self.carom.x, self.y - self.height//2 - self.carom.y)
        surface.blit(current_img, draw_pos)

        # 绘制生命值条
        self._draw_health_bar(surface, draw_pos)

    def _draw_health_bar(self, surface: pygame.Surface, draw_pos: tuple[int, int]):
        """绘制生命值条（实体上方）"""
        bar_width = self.width
        bar_height = 3
        bar_x = draw_pos[0]
        bar_y = draw_pos[1] - 8

        # 红色背景条
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # 绿色生命值条
        health_ratio = self.lift / self.max_lift
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    def update(self):
        """更新实体状态（需被子类重写）"""
        pass

class player(EntityBase):
    """玩家类，支持键盘控制"""
    def __init__(self, game_map: game_map, images: list[list[str]], to_time: int = 100,
                 tuceng: int = 1, down: int = 1, lift: int = 100):
        super().__init__(game_map, images, to_time, tuceng, down, lift)

    def forword_key(self, step: int = 1, images: Optional[List[str]] = None) -> Callable:
        """键盘控制向前移动的回调函数"""
        def action(_):
            self.forword(step, images)
        return action

    def back_key(self, step: int = 1, images: Optional[List[str]] = None) -> Callable:
        """键盘控制向后移动的回调函数"""
        def action(_):
            self.back(step, images)
        return action

    def left_key(self, step: int = 1, images: Optional[List[str]] = None) -> Callable:
        """键盘控制向左移动的回调函数"""
        def action(_):
            self.left(step, images)
        return action

    def right_key(self, step: int = 1, images: Optional[List[str]] = None) -> Callable:
        """键盘控制向右移动的回调函数"""
        def action(_):
            self.right(step, images)
        return action

    def update(self):
        """更新玩家状态：检测碰撞+自动移动"""
        if not self._check_collision():
            self.auto_move()

class noplayer(EntityBase):
    """非玩家实体类，支持AI控制和动作队列"""
    def __init__(self, game_map: game_map, images: List[List[str]], to_time: int = 100,
                 down: int = 1, tuceng: int = 1, lift: int = 100):
        super().__init__(game_map, images, to_time, tuceng, down, lift)
        self.ai_target = None  # AI目标（玩家或其他实体）
        self.ai_behavior = None  # True=远离，False=靠近
        self.can_attack = False  # 是否可攻击
        self.attack_damage = 0  # 攻击力
        self.attack_range = 0  # 攻击范围（像素）
        self.attack_interval = 1000  # 攻击间隔（毫秒）
        self.last_attack = 0  # 上次攻击时间
        self.action_queue = []  # 动作队列：[(动作名,步长,持续时间), ...]
        self.current_action = None  # 当前执行的动作
        self.action_timer = 0  # 动作计时器

    def q(self, can_attack: bool, attack_damage: int = 0, attack_range: int = 0, attack_interval: int = 1000):
        """设置攻击属性：can_attack（是否可攻击）、attack_damage（伤害）、attack_range（范围）、attack_interval（间隔）"""
        self.can_attack = can_attack
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.attack_interval = attack_interval

    def AI(self, target: EntityBase, behavior: bool):
        """设置AI目标和行为模式：target（目标实体）、behavior（True=远离，False=靠近）"""
        self.ai_target = target
        self.ai_behavior = behavior

    def wait(self, action_sequence: List[Tuple[str, int, int]]):
        """设置动作队列：动作名(forword/back/left/right)、步长、持续时间（毫秒）"""
        self.action_queue = action_sequence
        self.current_action = None
        self.action_timer = 0

    def _distance_to(self, target: EntityBase) -> float:
        """计算与目标的直线距离"""
        return math.hypot(self.x - target.x, self.y - target.y)

    def _ai_attack(self):
        """AI攻击逻辑：满足条件时对目标造成伤害"""
        now = pygame.time.get_ticks()
        if (self.can_attack and self.ai_target and self.ai_target.active and
                self._distance_to(self.ai_target) <= self.attack_range and
                now - self.last_attack >= self.attack_interval):
            self.ai_target.set_lift(self.ai_target.get_lift() - self.attack_damage)
            self.last_attack = now

    def _ai_move(self):
        """AI移动逻辑：根据行为模式靠近/远离目标"""
        if not self.ai_target or self.ai_behavior is None:
            return

        distance = self._distance_to(self.ai_target)
        move_step = 2  # AI移动步长

        # 保持50像素的安全距离，超出则移动
        if distance > 50:
            if not self.ai_behavior:  # 靠近目标
                # x轴调整
                if self.x < self.ai_target.x:
                    self.right(move_step)
                elif self.x > self.ai_target.x:
                    self.left(move_step)
                # y轴调整
                if self.y < self.ai_target.y:
                    self.back(move_step)
                elif self.y > self.ai_target.y:
                    self.forword(move_step)
            else:  # 远离目标
                # x轴调整
                if self.x < self.ai_target.x:
                    self.left(move_step)
                elif self.x > self.ai_target.x:
                    self.right(move_step)
                # y轴调整
                if self.y < self.ai_target.y:
                    self.forword(move_step)
                elif self.y > self.ai_target.y:
                    self.back(move_step)
        else:
            self.stop()

    def _execute_action_queue(self):
        """执行动作队列：按顺序执行预设动作"""
        now = pygame.time.get_ticks()

        # 无当前动作时，从队列取新动作
        if not self.current_action and self.action_queue:
            self.current_action = self.action_queue.pop(0)
            action_name, step, duration = self.current_action
            self.action_timer = now + duration  # 设置动作持续时间
            # 执行动作
            if hasattr(self, action_name):
                getattr(self, action_name)(step)

        # 当前动作超时，切换到静止
        elif self.current_action and now > self.action_timer:
            self.stop()
            self.current_action = None

    def update(self):
        """更新非玩家实体状态：动作队列→AI行为→碰撞检测→自动移动"""
        if not self.active:
            return

        # 优先执行动作队列
        if self.action_queue or self.current_action:
            self._execute_action_queue()
        # 动作队列为空时执行AI行为
        elif self.ai_target and self.ai_behavior is not None:
            self._ai_attack()
            self._ai_move()

        # 无碰撞时执行自动移动
        if not self._check_collision():
            self.auto_move()