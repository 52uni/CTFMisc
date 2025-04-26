from PIL import Image, ImageDraw

# 设置图像大小
width = 150
height = 900

# 创建一幅模式为RGB，尺寸为247*247并且背景为白色的图片
image = Image.new('RGB', (width, height), (255, 255, 255))

# 创建Draw对象:
draw = ImageDraw.Draw(image)

# 打开文件
misc100 = open('basic.txt')

# 循环填充每个像素:
for x in range(width):
    for y in range(height):
        # 读取每行rgb值并分割处理成int列表
        rgb_str = misc100.readline().strip()[1:-1]  # 去掉括号
        rgb = list(map(int, rgb_str.split(',')))
        # 为每个像素设置rgb值
        draw.point((x, y), (rgb[0], rgb[1], rgb[2]))

# 显示图片
image.show()
