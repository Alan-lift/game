import pygame
from typing import Optional, List, Any
from .camera import carom
from .background import way
from .entity import EntityBase, player
from .sound import SoundSystem
# from ..gui.text import Text
from ..gui.button import Button
# from ..gui.image import Image
# from ..utils.common import clean_component

# 初始化Pygame核心模块
pygame.init()
pygame.font.init()


class Windows_window:
    """窗口类，管理游戏主循环、渲染管道、事件处理和所有组件生命周期"""

    def __init__(self, icon: str, text: str, carom: carom):
        # 核心绑定
        self.carom = carom
        self.carom.entities = []  # 统一管理所有实体（玩家+非玩家）

        # 窗口属性
        self.window_width = carom.width  # 窗口宽度=相机拍摄宽度
        self.window_height = carom.height  # 窗口高度=相机拍摄高度
        self.window_title = text

        # 创建窗口（支持后续切换全屏）
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_title)

        # 设置窗口图标
        try:
            icon_surface = pygame.image.load(icon).convert_alpha()
            pygame.display.set_icon(icon_surface)
        except Exception as e:
            print(f"警告：窗口图标加载失败（路径：{icon}），错误信息：{e}")

        # 游戏循环控制
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60  # 默认帧率
        self.refresh_interval = 0  # 动态刷新间隔（由玩家to_time决定）

        # 组件存储
        self.background: Optional[way] = None  # 背景组件
        self.player: Optional[player] = None  # 玩家实例（单独存储方便调用）
        self.gui_components: List[Any] = []  # GUI组件（文本、按钮、图片）

        # 全屏状态标记
        self.is_fullscreen = False

        # 初始化音效系统（新增）
        self.sound_system = SoundSystem()

    def set_background(self, background: way):
        """设置游戏背景（支持多层背景叠加）"""
        self.background = background

    def add_entity(self, entity: EntityBase):
        """添加实体到游戏世界（自动处理玩家相机跟随）"""
        if entity not in self.carom.entities:
            self.carom.entities.append(entity)
            # 若为玩家实体，自动绑定相机跟随
            if isinstance(entity, player):
                self.player = entity
                self.carom.follow(entity)
                # 用玩家的to_time设置全局刷新间隔
                self.refresh_interval = entity.to_time / 1000  # 转换为秒

    def add_gui(self, gui_component: Any):
        """添加GUI组件（文本、按钮、图片）"""
        if gui_component not in self.gui_components:
            self.gui_components.append(gui_component)

    def remove_gui(self, gui_component: Any):
        """移除指定GUI组件"""
        if gui_component in self.gui_components:
            self.gui_components.remove(gui_component)

    def toggle_fullscreen(self):
        """切换全屏/窗口模式"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.FULLSCREEN | pygame.HWSURFACE
            )
        else:
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def handle_events(self):
        """处理游戏事件（窗口关闭、键盘、鼠标等）"""
        for event in pygame.event.get():
            # 窗口关闭事件
            if event.type == pygame.QUIT:
                self.running = False

            # 键盘按键事件
            elif event.type == pygame.KEYDOWN:
                # ESC键切换全屏
                if event.key == pygame.K_ESCAPE:
                    self.toggle_fullscreen()
                # F11键强制全屏切换（备用）
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()

            # 鼠标事件（传递给GUI按钮）
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 遍历所有按钮组件，检查是否点击
                for gui in self.gui_components:
                    if isinstance(gui, Button):
                        gui.check_click(mouse_pos)

    def update_components(self):
        """更新所有组件状态（实体、GUI、相机）"""
        # 1. 更新相机位置（跟随玩家）
        self.carom.update()

        # 2. 更新实体状态（玩家+非玩家）
        for entity in self.carom.entities[:]:  # 切片遍历避免删除元素报错
            if entity.active:
                entity.update()
            # 移除死亡实体（生命值≤0）
            else:
                self.carom.entities.remove(entity)
                if entity == self.player:
                    self.player = None

        # 3. 更新GUI组件（文本位置、按钮状态等）
        for gui in self.gui_components:
            if hasattr(gui, 'update'):
                gui.update()

    def draw_components(self):
        """绘制所有组件（按层级：背景→实体→GUI）"""
        # 1. 清屏（黑色背景）
        self.screen.fill((0, 0, 0))

        # 2. 绘制背景（考虑相机偏移）
        if self.background:
            self.background.draw(self.screen)

        # 3. 绘制实体（按图层排序：图层值小的在上方）
        sorted_entities = sorted(self.carom.entities, key=lambda e: e.tuceng, reverse=True)
        for entity in sorted_entities:
            if entity.active:
                entity.draw(self.screen)

        # 4. 绘制GUI组件（始终在最上层，不随相机移动）
        for gui in self.gui_components:
            gui.draw(self.screen)

    def windowloop(self):
        """游戏主循环（核心运行逻辑）"""
        self.running = True
        print(f"游戏启动成功！帧率：{self.fps}，窗口大小：{self.window_width}x{self.window_height}")

        while self.running:
            # 1. 事件处理
            self.handle_events()

            # 2. 组件状态更新
            self.update_components()

            # 3. 组件绘制
            self.draw_components()

            # 4. 刷新屏幕
            pygame.display.flip()

            # 5. 控制帧率（根据刷新间隔动态调整）
            if self.refresh_interval > 0:
                self.clock.tick(1 / self.refresh_interval)
            else:
                self.clock.tick(self.fps)

        # 循环结束，清理资源
        self.sound_system.clean_up()  # 新增：清理音效资源
        pygame.font.quit()
        pygame.quit()
        print("游戏已退出，资源清理完成")