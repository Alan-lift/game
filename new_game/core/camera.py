class carom:
    """相机类，定义拍摄范围及跟随逻辑"""
    def __init__(self, x: int, y: int, rize_x: int, rize_y: int):
        self.entities = []  # 存储所有实体
        self.x = x  # 拍摄范围左上角x坐标
        self.y = y  # 拍摄范围左上角y坐标
        self.width = rize_x  # 拍摄宽度
        self.height = rize_y  # 拍摄高度
        self.target = None  # 跟随目标

    def follow(self, target):
        """设置相机跟随目标（玩家）"""
        self.target = target

    def update(self):
        """更新相机位置，使目标保持在中心"""
        if self.target:
            self.x = self.target.x - self.width // 2
            self.y = self.target.y - self.height // 2