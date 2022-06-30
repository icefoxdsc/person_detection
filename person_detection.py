
import time
from pynput import *
from window_capture import window_capture
from test import instancePrediction

class instanceListener():
    def __init__(self, st_pd_mv = mouse.Button.middle, exit_value = keyboard.Key.f6, jpg_file_path = "img/wc_3.jpg"):
        self.st_pd_mv = st_pd_mv
        self.exit_value = exit_value
        self.jpg_file_path = jpg_file_path
        self.pd_flag = False
        self.exit_flag = False
        self.instance_prediction = instancePrediction()
        self.instance_mouse = mouse.Controller()

    def mouse_move(self, x, y):
        pass

    # 更改 检测状态
    def mouse_click(self, x, y, button, pressed):
        if self.st_pd_mv == button and pressed:
            self.pd_flag = not self.pd_flag     # 检测开关
            self.exit_flag = True               # 检测停止
        
        print("button = ", button, " pressed = ", pressed, " ", x, y, self.pd_flag, "\n", self.st_pd_mv, type(button))

        if self.pd_flag:
            #print("开始 检测. ")
            #st_time = time.time()
            window_capture(self.jpg_file_path)
            #print("window capture done . start prediction .")
            time.sleep(0.030)
            pos_list = self.instance_prediction.predict(self.jpg_file_path)
            #print("prediction done . ")
            self.move_to_pos(pos_list)
            #print("移动鼠标")
            end_time = time.time()
            #print("检测整体时间： ", end_time - st_time)

        else:
            print("self.pd_flag = ", self.pd_flag, " 停止 目标检测.")

    def mouse_scroll(self, x, y, dx, dy):
        pass

    def move_to_pos(self, pos_list):
        x, y = self.instance_mouse.position
        ct = 1000000
        res = (600, 600)
        for x_, y_ in pos_list:
            tmp = ((x-x_)**2 + (y-y_)**2) ** 0.5
            if tmp < ct:
                ct = tmp
                res = (x_, y_)
        
        # 移动鼠标
        if ct != 1000000:
            self.instance_mouse.position = res
            print("新的位置: ", res)

        
    # 目标检测
    def run_pd(self):
        # with mouse.Listener(
        # on_move = self.mouse_move, 
        # on_click = self.mouse_click,
        # on_scroll = self.mouse_scroll
        # ) as listener:
        #     listener.join()
        # print("start_listener_mouse .")

        print("开始 检测. ")
        listener = mouse.Listener(
            on_move = self.mouse_move, 
            on_click = self.mouse_click,
            on_scroll = self.mouse_scroll
        )
        listener.start()

 
        while True:
            if self.exit_flag:
                listener.stop()
                print("检测停止 .")
                break

            #st_time = time.time()
            time.sleep(0.30)
            window_capture(self.jpg_file_path)
            #print("window capture done . start prediction .")
            time.sleep(0.30)
            pos_list = self.instance_prediction.predict(self.jpg_file_path)
            #print("prediction done . ")
            self.move_to_pos(pos_list)
            #print("移动鼠标")
            #end_time = time.time()
            #print("检测整体时间： ", end_time - st_time)
            

if __name__ == '__main__':
    instanceMouse = mouse.Controller()

    position = instanceMouse.position  # 获取当前的鼠标位置
    print('当前的鼠标位置:{}'.format(position))

    instanceMouse.position = (1017, 236)  # 设置鼠标的位置,移动鼠标到该位置
    print('移动鼠标到坐标点:{}'.format(instanceMouse.position))

    instanceMouse.move(5, -5)  # 相对于当前鼠标位置位置移动鼠标

    instanceMouse.press(mouse.Button.left)  # 按下鼠标左键
    instanceMouse.release(mouse.Button.left)  # 释放鼠标左键
    instanceMouse.press(mouse.Button.right)  # 按下鼠标右键
    instanceMouse.release(mouse.Button.right)  # 释放鼠标右键
    instanceMouse.press(mouse.Button.middle)  # 按下鼠标中键
    instanceMouse.release(mouse.Button.middle)  # 释放鼠标中键

    instanceMouse.click(mouse.Button.left, 2)  # 双击鼠标左键

    instanceMouse.scroll(0, 2)  # 向下滚动滚轮两次


