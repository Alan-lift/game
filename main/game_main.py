import keyboard
import threading
#from game.game import carom, Windows_window, way, player, noplayer, map
from game.new_game import *
from game.new_game import game_map

zy1, zy2 = 'move_sound.mp3', 'attack_sound.mp3'
icon = 'icon.ico'
w1, w2 = 'w_1.png', 'w_2.png'
left = ['left_1.png', 'left_2.png']
back = ['back_1.png', 'back_2.png']
forword = ['forword_1.png', 'forword_2.png']
right = ['right_1.png', 'right_2.png']
stop = ['stop_1.png', 'stop_2.png']
eforword = ['e_forword_1.png', 'e_forword_2.png']
eback = ['e_back_1.png', 'e_back_2.png']
eleft = ['e_left_1.png', 'e_left_2.png']
eright = ['e_right_1.png', 'e_right_2.png']
estop = ['e_stop_1.png', 'e_stop_2.png']

# 4.判断触发事件
def start_listening(player):
    # 使用玩家的按键响应方法
    keyboard.on_press_key('w', player.forword_key(step=5, images=forword))
    keyboard.on_press_key('a', player.left_key(step=5, images=left))
    keyboard.on_press_key('s', player.back_key(step=5, images=back))
    keyboard.on_press_key('d', player.right_key(step=5, images=right))
    SoundSystem.play_sound(trigger=player.is_attacking, sound_id="attack")
    keyboard.wait()


if __name__ == '__main__':
    # 1.创建相机
    c = carom(x=0, y=0, rize_x=1920, rize_y=1080)
    m = game_map(carom=c, rize_x=1000, rize_y=1000)
    # 2.创建窗口
    root = Windows_window(icon=icon, text='game', carom=c)

    # 加载音效（示例）
    root.sound_system.load_sound('move', zy1)
    root.sound_system.load_sound('attack', zy2)

    # 3.创建背景
    w_list: list[tuple[list[int], str, int]] = [([0, 0], w1, 1),([395, 203], w2, 1)]
    w = way(game_map=m, images_list=w_list)
    root.set_background(w)

    # 3.创建玩家
    images_list = [
        forword,  # 向前
        back,  # 向后
        left,  # 向左
        right,  # 向右
        stop  # 停止
    ]
    player = player(
        game_map=m,
        images=images_list,
        to_time=100,
        tuceng=1,
        down=1,
        lift=100
    )
    root.add_entity(player)
    """
    # 4.创建实体（示例）
    enemy_images = [
        eforword,
        eback,
        eleft,
        eright,
        estop,
    ]
    enemy = noplayer(
        game_map=m,
        images=enemy_images,
        to_time=150,
        down=1,
        tuceng=1,
        lift=50
    )
    enemy.x = 500  # 设置初始位置
    enemy.y = 500
    enemy.q(can_attack=True, attack_damage=10, attack_range=100)  # 设置攻击属性
    enemy.AI(player, behavior=False)  # 追踪玩家
    # 也可以设置动作队列：enemy.wait([('right', 2, 1000), ('forword', 2, 1000)])
    enemy.wait([('right', 2, 1000), ('forword', 2, 1000)])
    root.add_entity(enemy)
    """

    # 启动监听线程
    listener_thread = threading.Thread(
        target=start_listening,
        args=(player,),
        daemon=True
    )
    listener_thread.start()

    # 5.循环窗口
    root.windowloop()