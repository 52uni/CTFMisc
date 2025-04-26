filename = '1.txt'

with open(filename, 'r') as file:
    data = file.read().replace('\n', '').replace(' ', '')

output = ''
for i in range(0, len(data), 16):
    output += data[i:i+16] + '\n'

with open('output.txt', 'w') as f:
    f.write(output)

with open('output.txt', 'r') as file:
    lines = file.readlines()

formatted_lines = []

for line in lines:
    line = line.strip()  # 去除行尾的换行符
    if len(line) >= 2:
        formatted_line = ''
        for i in range(0, len(line), 2):
            formatted_line += line[i:i+2] + ':'
        formatted_line = formatted_line[:-1]  # 去除最后一个多余的冒号
        formatted_lines.append(formatted_line)
    else:
        formatted_lines.append(line)

formatted_text = '\n'.join(formatted_lines)
print(formatted_text)
with open('usbdata.txt', 'w') as f:
    f.write(formatted_text)

mappings = { 0x04:"A",  0x05:"B",  0x06:"C", 0x07:"D", 0x08:"E", 0x09:"F", 0x0A:"G",  0x0B:"H", 0x0C:"I",  0x0D:"J", 0x0E:"K", 0x0F:"L", 0x10:"M", 0x11:"N",0x12:"O",  0x13:"P", 0x14:"Q", 0x15:"R", 0x16:"S", 0x17:"T", 0x18:"U",0x19:"V", 0x1A:"W", 0x1B:"X", 0x1C:"Y", 0x1D:"Z", 0x1E:"1", 0x1F:"2", 0x20:"3", 0x21:"4", 0x22:"5",  0x23:"6", 0x24:"7", 0x25:"8", 0x26:"9", 0x27:"0", 0x28:"n", 0x2a:"[DEL]",  0X2B:"    ", 0x2C:" ",  0x2D:"-", 0x2E:"=", 0x2F:"[",  0x30:"]",  0x31:"\\", 0x32:"~", 0x33:";",  0x34:"'", 0x36:",",  0x37:"." }
nums = []
keys = open('usbdata.txt')
for line in keys:
    # if line[0]!='0' or line[1]!='0' or line[3]!='0' or line[4]!='0' or line[9]!='0' or line[10]!='0' or line[12]!='0' or line[13]!='0' or line[15]!='0' or line[16]!='0' or line[18]!='0' or line[19]!='0' or line[21]!='0' or line[22]!='0':
        #  continue
    nums.append(int(line[6:8],16))
    # 00:00:xx:....
keys.close()
output = ""
for n in nums:
    if n == 0 :
        continue
    if n in mappings:
        output += mappings[n]
    else:
        # output += '[unknown]'
        pass
print('output :n' + output)