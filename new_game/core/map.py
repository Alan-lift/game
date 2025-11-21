class game_map:
    """游戏地图类：限制游戏世界边界，所有实体不得超出地图范围"""
    def __init__(self, carom: "carom", rize_x: int, rize_y: int):
        """
        初始化地图
        :param carom: 绑定的相机实例（字符串注解避免循环导入）
        :param rize_x: 地图x方向大小（宽度）
        :param rize_y: 地图y方向大小（高度）
        """
        self.carom = carom
        self.rize_x = rize_x  # 地图宽度边界
        self.rize_y = rize_y  # 地图高度边界

    def check_boundary(self, x: int, y: int, width: int, height: int) -> tuple[int, int]:
        """
        检查并修正坐标，确保实体不超出地图边界
        :param x: 实体x坐标
        :param y: 实体y坐标
        :param width: 实体宽度（用于右边界判断）
        :param height: 实体高度（用于下边界判断）
        :return: 修正后的 (x, y) 坐标
        """
        # 左边界：x ≥ 0
        x = max(0, x)
        # 右边界：x + 实体宽度 ≤ 地图宽度
        x = min(x, self.rize_x - width)
        # 上边界：y ≥ 0
        y = max(0, y)
        # 下边界：y + 实体高度 ≤ 地图高度
        y = min(y, self.rize_y - height)
        return x, y