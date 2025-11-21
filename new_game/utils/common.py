import math
from typing import List, Type, Any, Union, Tuple, Optional
from ..core.entity import EntityBase, player, noplayer
from ..core.camera import carom
from ..gui import Text, Button, Image


def clean_component(
        component: Any,
        carom: Optional[carom] = None,
        gui_list: Optional[List[Any]] = None
) -> bool:
    """
    安全清除游戏组件（实体/GUI），返回清除结果
    :param component: 待清除组件（EntityBase/Text/Button/Image）
    :param carom: 相机实例（清除实体时必填）
    :param gui_list: GUI组件列表（清除GUI时必填，即Windows_window.gui_components）
    :return: 清除成功返回True，失败返回False
    """
    # 清除实体组件
    if isinstance(component, EntityBase):
        if not carom:
            print("错误：清除实体必须传入carom参数")
            return False
        if component in carom.entities:
            component.active = False
            carom.entities.remove(component)
            print(f"成功清除实体：{type(component).__name__}（ID: {id(component)}）")
            return True
        else:
            print(f"警告：实体不在相机实体列表中，清除失败")
            return False

    # 清除GUI组件
    elif isinstance(component, (Text, Button, Image)):
        if not gui_list:
            print("错误：清除GUI必须传入gui_list参数")
            return False
        if component in gui_list:
            gui_list.remove(component)
            print(f"成功清除GUI组件：{type(component).__name__}（ID: {id(component)}）")
            return True
        else:
            print(f"警告：GUI组件不在列表中，清除失败")
            return False

    # 不支持的组件类型
    else:
        print(f"错误：不支持清除类型 {type(component).__name__} 的组件")
        return False


def check_entity_collision(entity_a: EntityBase, entity_b: EntityBase) -> bool:
    """
    检测两个实体是否碰撞（严格校验：同图层+均活跃+矩形重叠）
    :param entity_a: 实体A（player/noplayer）
    :param entity_b: 实体B（player/noplayer）
    :return: 碰撞返回True，否则返回False
    """
    # 类型校验
    if not (isinstance(entity_a, EntityBase) and isinstance(entity_b, EntityBase)):
        print("错误：碰撞检测参数必须是EntityBase子类实例")
        return False
    # 自身碰撞排除
    if entity_a is entity_b:
        return False
    # 核心碰撞条件
    return (entity_a.tuceng == entity_b.tuceng and
            entity_a.active and entity_b.active and
            entity_a.rect.colliderect(entity_b.rect))


def get_active_entities(carom: carom) -> List[EntityBase]:
    """
    获取所有活跃实体（过滤非活跃实体）
    :param carom: 相机实例
    :return: 活跃实体列表
    """
    if not isinstance(carom, carom):
        print("错误：参数必须是carom实例")
        return []
    return [entity for entity in carom.entities if entity.active]


def filter_entities_by_type(
        carom: carom,
        entity_type: Union[Type[player], Type[noplayer]],
        active_only: bool = True
) -> List[EntityBase]:
    """
    按类型筛选实体（支持玩家/非玩家实体）
    :param carom: 相机实例
    :param entity_type: 筛选类型（player/noplayer）
    :param active_only: 是否只保留活跃实体（默认True）
    :return: 筛选后的实体列表
    """
    # 类型校验
    if not isinstance(carom, carom):
        print("错误：carom参数必须是carom实例")
        return []
    if not issubclass(entity_type, EntityBase):
        print("错误：entity_type必须是player或noplayer")
        return []

    # 基础筛选（按类型）
    filtered = [entity for entity in carom.entities if isinstance(entity, entity_type)]
    # 活跃状态筛选
    if active_only:
        filtered = [entity for entity in filtered if entity.active]

    return filtered


def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    计算两个坐标点之间的直线距离（欧几里得距离）
    :param pos1: 坐标1 (x1, y1)
    :param pos2: 坐标2 (x2, y2)
    :return: 两点间的距离
    """
    if len(pos1) != 2 or len(pos2) != 2:
        print("错误：坐标必须是二元组 (x, y)")
        return 0.0
    return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])


def clamp_value(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """
    限制值在指定范围内（防止溢出）
    :param value: 待限制的值
    :param min_val: 最小值
    :param max_val: 最大值
    :return: 限制后的值
    """
    if min_val > max_val:
        print(f"警告：最小值 {min_val} 大于最大值 {max_val}，交换后限制")
        min_val, max_val = max_val, min_val
    return max(min_val, min(value, max_val))