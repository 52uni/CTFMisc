# 打开文本文件
with open('赋值.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()  # 逐行读取文件内容

# 初始化结果列表
result = []

# 定义待匹配的字符串
target_string = "GET /index.php?id=1%27and%20(select%20ascii(substr((select%20skyflag_is_here2333%20from%20flag%20limit%200,1),{0},1)))"

# 统计不同x取值下特定信息出现的次数
for x in range(1, 34):
    count = 0
    for line in lines:
        if target_string.format(x) in line:
            count += 1
    result.append(count + 32)  # 将出现次数加上33

# 以空格隔开输出结果
output = ' '.join(str(count) for count in result)
print("每个x取值下特定信息出现的次数（加上32后）：", output)
