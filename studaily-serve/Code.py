from PIL import Image,ImageDraw,ImageFont
import random
import io
# im=Image.new("RGB",(100,100),color=(255,0,0))
# draw=ImageDraw.Draw(im)
# for i in range(1,100):
#     draw.point((random.randint(1,100),random.randint(1,100)),fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))


class code:
    def __init__(self):
        self.width=120
        self.height=40
        self.im=None
        self.lineNum=0
        self.pointNum=0
        self.textNum=4
        self.textes="abcdefgABCDEFG1234567890"
        self.str=""
        self.bg=None
    def create(self):
        self.bg=self.bgColor()
        self.im=Image.new("RGBA",(self.width,self.height),color=(self.bg))
    def bgColor(self):
        self.bg=(random.randint(0,120),random.randint(0,120),random.randint(0,120),255)
        return self.bg
    def fgColor(self):
        return (random.randint(120, 255), random.randint(120, 255),random.randint(120,255),255)
    def point(self):
        draw = ImageDraw.Draw(self.im)
        pnum=self.pointNum or random.randint(30,60)
        for i in range(pnum):
            draw.point((random.randint(0,self.width),random.randint(0,self.width)),fill=(self.fgColor()))
    def line(self):
        draw = ImageDraw.Draw(self.im)
        lnum = self.lineNum or random.randint(3, 6)
        for i in range(lnum):
            place = (random.randint(0, self.width), random.randint(0, self.height), random.randint(0, self.width),random.randint(0, self.height))
            draw.line(place, fill=(self.fgColor()),width=random.randint(1,3))
    def rotate(self):
        self.im=self.im.rotate(random.randint(-10,10))
        im1=Image.new("RGBA",(self.width,self.height),color=(self.bg))
        self.im=Image.composite(self.im,im1,self.im)
    def texts(self):
        draw = ImageDraw.Draw(self.im)
        for i in range(self.textNum):
            t=self.textes[random.randint(0,len(self.textes)-1)]
            x=i*self.width/self.textNum+random.randint(-7,7)
            y=random.randint(-5,5)
            draw.text((x,y),t,font=ImageFont.truetype("C:/WINDOWS/Fonts/MSYH.TTC",random.randint(22,28)),fill=(self.fgColor()))
            self.str += t
        self.rotate()



    def output(self):
        self.create()
        self.point()
        self.line()
        self.texts()
        # self.im.show()
        # 把文件保存在内存里面
        bt=io.BytesIO()
        self.im.save(bt,"png")
        return bt.getvalue()    #返回值  图片的数据

# codeobj=code()
# codeobj.output()
# z在路哟中output()输出  为一堆字符串    设置头信息  返回给浏览器
