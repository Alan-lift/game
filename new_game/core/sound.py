import pygame
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

# 初始化Pygame混音器（音效核心）
pygame.mixer.init()


@dataclass
class SoundEffect:
    """音效数据类：存储音频对象和播放配置"""
    sound: pygame.mixer.Sound  # 音频对象
    volume: float = 1.0  # 音量（0.0-1.0）
    loop: int = 0  # 循环次数（0=不循环，-1=无限循环）


class SoundSystem:
    """音效系统：支持触发条件控制、多音频管理、音量调节"""

    def __init__(self):
        self.sound_map: Dict[str, SoundEffect] = {}  # 音频缓存（key=音频标识，value=音效对象）
        self.master_volume: float = 1.0  # 主音量（0.0-1.0）
        self.current_playing: List[Tuple[str, pygame.mixer.Channel]] = []  # 正在播放的音频

    def load_sound(self, sound_id: str, audio_path: str, volume: float = 1.0, loop: int = 0) -> bool:
        """
        加载音频文件到缓存（建议游戏初始化时加载）
        :param sound_id: 音频唯一标识（用于后续调用）
        :param audio_path: 音频文件路径（支持wav/ogg等Pygame兼容格式）
        :param volume: 该音频的独立音量（0.0-1.0，最终音量=独立音量×主音量）
        :param loop: 循环次数（0=不循环，-1=无限循环）
        :return: 加载成功返回True，失败返回False
        """
        if sound_id in self.sound_map:
            print(f"警告：音频标识 {sound_id} 已存在，将覆盖原有音频")

        try:
            # 加载音频文件
            sound = pygame.mixer.Sound(audio_path)
            # 限制音量范围
            volume = max(0.0, min(1.0, volume))
            # 存入缓存
            self.sound_map[sound_id] = SoundEffect(
                sound=sound,
                volume=volume,
                loop=loop
            )
            print(f"成功加载音频：{sound_id}（路径：{audio_path}）")
            return True
        except Exception as e:
            print(f"错误：加载音频 {sound_id} 失败（路径：{audio_path}），错误信息：{e}")
            return False

    def play_sound(self, trigger: bool, sound_id: str) -> Optional[pygame.mixer.Channel]:
        """
        按触发条件播放指定音频（核心方法）
        :param trigger: 触发条件（True=播放，False=不播放）
        :param sound_id: 音频标识（必须已通过load_sound加载）
        :return: 播放成功返回音频通道对象，失败返回None
        """
        # 触发条件不满足，直接返回
        if not trigger:
            return None

        # 音频未加载，返回失败
        if sound_id not in self.sound_map:
            print(f"错误：播放音频失败，{sound_id} 未加载")
            return None

        # 获取音效配置
        sound_effect = self.sound_map[sound_id]
        # 计算最终音量（独立音量 × 主音量）
        final_volume = sound_effect.volume * self.master_volume

        # 播放音频（返回音频通道，用于后续控制）
        channel = sound_effect.sound.play(loops=sound_effect.loop)
        if channel is None:
            print(f"警告：音频通道不足，{sound_id} 播放失败")
            return None

        # 设置音量
        channel.set_volume(final_volume)
        # 记录正在播放的音频
        self.current_playing.append((sound_id, channel))
        print(f"音频播放成功：{sound_id}（音量：{final_volume:.2f}）")
        return channel

    def stop_sound(self, sound_id: Optional[str] = None):
        """
        停止播放音频
        :param sound_id: 音频标识（None=停止所有音频）
        """
        if sound_id is None:
            # 停止所有音频
            pygame.mixer.stop()
            self.current_playing.clear()
            print("已停止所有正在播放的音频")
        else:
            # 停止指定音频
            for idx, (sid, channel) in enumerate(self.current_playing[:]):
                if sid == sound_id and channel.get_busy():
                    channel.stop()
                    self.current_playing.pop(idx)
                    print(f"已停止音频：{sound_id}")

    def set_master_volume(self, volume: float):
        """
        设置主音量（影响所有音频）
        :param volume: 主音量（0.0-1.0）
        """
        self.master_volume = max(0.0, min(1.0, volume))
        # 更新正在播放的音频音量
        for sound_id, channel in self.current_playing:
            if channel.get_busy():
                sound_effect = self.sound_map[sound_id]
                channel.set_volume(sound_effect.volume * self.master_volume)
        print(f"主音量已设置为：{self.master_volume:.2f}")

    def set_sound_volume(self, sound_id: str, volume: float):
        """
        设置单个音频的独立音量（不影响主音量）
        :param sound_id: 音频标识
        :param volume: 独立音量（0.0-1.0）
        """
        if sound_id not in self.sound_map:
            print(f"错误：设置音量失败，{sound_id} 未加载")
            return

        # 限制音量范围
        volume = max(0.0, min(1.0, volume))
        self.sound_map[sound_id].volume = volume

        # 更新正在播放的该音频音量
        for sid, channel in self.current_playing:
            if sid == sound_id and channel.get_busy():
                channel.set_volume(volume * self.master_volume)
        print(f"音频 {sound_id} 独立音量已设置为：{volume:.2f}")

    def is_playing(self, sound_id: str) -> bool:
        """
        检查指定音频是否正在播放
        :param sound_id: 音频标识
        :return: 正在播放返回True，否则返回False
        """
        for sid, channel in self.current_playing:
            if sid == sound_id and channel.get_busy():
                return True
        return False

    def clean_up(self):
        """清理资源（游戏退出时调用）"""
        self.stop_sound()
        pygame.mixer.quit()
        print("音效系统资源已清理")