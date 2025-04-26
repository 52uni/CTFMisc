from PIL import Image
a=[]
im = Image.open('E:/AInternetsecurity/1python/flag.bmp')
pix = im.load()
width = im.size[0]
height = im.size[1]
demo=open('rgb.txt','w')
for y in range(width):
    for x in range(height):
        r, g, b = pix[y, x]
        rgb=r,g,b	
        demo.write(str(rgb)+"\n")