# -*- encoding=utf-8 -*-
import os
import time
import tkinter
from tkinter.filedialog import askopenfilename

from PIL import Image
from PIL import ImageTk
import time
from .Wicket import Wicket
from time import sleep


image = None
img = None
imgCorp=None
fin_path=None
class Crop(Wicket):
    def __init__(self):
        super().__init__()
        self.left_mouse_down_x = 0
        self.left_mouse_down_y = 0
        self.left_mouse_up_x = 0
        self.left_mouse_up_y = 0
        self.sole_rectangle = None
        self.save_folder = os.path.abspath('media\image')
        self.provisional_folder = os.path.abspath('provisional')

        self.img_entry = None
        self.img_path = None
        self.img_canvas = None
        self.sole_img = None
        self.fin_path=None
        self.create_folder(self.save_folder)
        self.create_folder(self.provisional_folder)

    @staticmethod
    def create_folder(folder):
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print('创建文件夹成功:{}'.format(folder))
            except Exception as e:
                print('创建文件夹失败:{}'.format(e))

    @staticmethod
    def get_now():
        return time.strftime('%Y%m%d%H%M%S', time.localtime())

    def choose_img(self,img1):
        # 选择图片的Frame
        print("self.win.winfo_screenwidth()",self.win.winfo_screenwidth())
        print("self.win.winfo_screenwidth()",self.win.winfo_screenheight())

        img_frame = tkinter.Frame(self.win,bg="red")
 ##       img_frame.grid(column=0, row=0)
        self.put(img1)
        ##self.img_canvas=tkinter.Canvas(img_frame) 
        print("1frame:",img_frame)
        l=tkinter.Canvas(img_frame)
        canvas_width = l.winfo_width()
        canvas_height = l.winfo_height()

##        img_button = tkinter.Button(img_frame, text='使用剪裁', command=self.set_image)

##        img_button.grid(row=0, column=2)
        img_frame.pack()
##        print("self.img_path=",self.img_path)
        # 显示图片的画布
        
        
        canvas_frame = tkinter.Frame(self.win)
        print("canvas_frame",canvas_frame.winfo_width)
        screen_width, screen_height = self.get_screen()
        zoom = 8 / 9
        canvas_width = int(screen_width * zoom)
        canvas_height = int(screen_height * zoom)
        self.img_canvas = tkinter.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
        canvas_width = self.img_canvas.winfo_width()
        canvas_height = self.img_canvas.winfo_height()

        
        self.img_canvas.bind('<Button-1>', self.left_mouse_down)  # 鼠标左键按下
        self.img_canvas.bind('<ButtonRelease-1>', self.left_mouse_up)  # 鼠标左键释放
        self.img_canvas.bind('<Button-3>', self.right_mouse_down)  # 鼠标右键按下
        self.img_canvas.bind('<ButtonRelease-3>', self.right_mouse_up)  # 鼠标右键释放
        self.img_canvas.bind('<B1-Motion>', self.moving_mouse)  # 鼠标左键按下并移动
        
        self.img_canvas.pack()
        canvas_frame.pack()
        self.set_image()

    def left_mouse_down(self, event):
        # print('鼠标左键按下')
        self.left_mouse_down_x = event.x
        self.left_mouse_down_y = event.y

    def left_mouse_up(self, event):
        # print('鼠标左键释放')
        self.left_mouse_up_x = event.x
        self.left_mouse_up_y = event.y
       # print("left_mouse_up_selfpath=",self.img_path)
        self.corp_img(self.img_path, self.left_mouse_down_x,
                      self.left_mouse_down_y,
                      self.left_mouse_up_x, self.left_mouse_up_y)

    def moving_mouse(self, event):
        # print('鼠标左键按下并移动')
        moving_mouse_x = event.x
        moving_mouse_y = event.y
        if self.sole_rectangle is not None:
            self.img_canvas.delete(self.sole_rectangle)  # 删除前一个矩形
        self.sole_rectangle = self.img_canvas.create_rectangle(self.left_mouse_down_x,
                                                               self.left_mouse_down_y,
                                                               moving_mouse_x,
                                                               moving_mouse_y, outline='red')

    def right_mouse_down(self, event):
        # print('鼠标右键按下')
        pass

    def right_mouse_up(self, event):
        # print('鼠标右键释放')
        pass

    def corp_img(self, source_file, x_begin, y_begin, x_end, y_end):
        print("corp_img_self.img_path=",self.img_path)
        print("corp_img_self.sourcefile=",source_file)
        if x_begin < x_end:
            min_x = x_begin
            max_x = x_end
        else:
            min_x = x_end
            max_x = x_begin
        if y_begin < y_end:
            min_y = y_begin
            max_y = y_end
        else:
            min_y = y_end
            max_y = y_begin
        
        suffix = os.path.splitext(source_file)[1]
        now = self.get_now()
        save_name = now + suffix
        save_path = os.path.join(self.save_folder, save_name)
        print("before sourcefile")
        print(os.path.isfile(source_file))
        if os.path.isfile(source_file):
            corp_image = Image.open(source_file)
            region = corp_image.crop((min_x, min_y, max_x, max_y))
            region.save(save_path)
            print("save_path",save_path)
            image=region
            img = ImageTk.PhotoImage(image)
            
            if self.sole_img is not None:
               print(self.sole_img)
               self.img_canvas.delete(self.sole_img)  # 删除前一张图片
               print("delete")
            
            self.sole_img=self.img_canvas.create_image(min_x,min_y, anchor='nw', image=img)
            print(type(self.sole_img)) 
            self.win.mainloop()  
            global imgCorp
            imgCorp=img
            global fin_path
            fin_path=os.path.join('image/',save_name)
        else:
            print("source file is wrong")
            
    
 ##           self.sole_img.winfo_height()
 ##       print(canvas_width1,canvas_height1)
 #       print(self.sole_img)


    def set_image(self,):
        
        global image
        global img

        
 ##       self.img_canvas.place(x=0, y=0) 
        print('选择图片路径')
        print(self.img_canvas)
        if self.sole_rectangle is not None:
            self.img_canvas.delete(self.sole_rectangle)  # 删除前一个矩形
        img_path=str(image['image'])
        self.img_path = os.path.abspath(img_path)
        print("123123123123",self.img_path)
        print('加载图片')
        
        print(self.img_canvas)
        canvas_width = self.win.winfo_screenwidth()*0.95
        canvas_height = self.win.winfo_screenheight()*0.95
        print(canvas_width,canvas_height)
        imageuse = Image.open(image['image'])
        
        now = self.get_now()
        str1=str(image['image'])
        
        suffix =str1.split('.')[1]
        save_name = now +"."+suffix
        save_path = os.path.join(self.provisional_folder, save_name)
        
        print(save_path)
        
        self.img_path=save_path
        
        img_width, img_height = imageuse.size
        a=round(img_width*2/3)
        b=round(img_height*2/3)
        if img_width > canvas_width or img_height > canvas_height:
            while a>canvas_width or b > canvas_height:
                a=round(a*2/3)
                b=round(b*2/3)
            re_img = imageuse.resize((a,b), Image.ANTIALIAS)
            re_img.save(save_path)
            imageuse=re_img
            image=re_img
            ret_path = save_path
            print('自动缩放图片完成,保存于:{}'.format(ret_path))
        
        
        else:
            print("not smaill")
            imageuse.save(save_path)
        
        img = ImageTk.PhotoImage(imageuse)
        if self.sole_img is not None:
            self.img_canvas.delete(self.sole_img)  # 删除前一张图片
            print('已清除前一张图片')
        else:
            print("sole_img=None")
        self.sole_img = self.img_canvas.create_image(0, 0, anchor='nw', image=img)
        print(self.sole_img)    

    def put(self,img1):
        global image 
        global img
        image=img1
    def get_corp(self,):
        global imgCorp
        print ("imgCorp",imgCorp )
        return imgCorp
    def get_corp_path(self,):
        global fin_path
        print ("imgCorp",fin_path )
        return fin_path




if __name__ == '__main__':
    corp = Crop()
    corp.create_window()
    corp.set_window_title('裁剪图片')
    corp.set_window_size('max')
    corp.choose_img()
    corp.show_window()