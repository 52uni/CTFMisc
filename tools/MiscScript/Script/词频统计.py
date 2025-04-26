alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-={}[]"
# filename = input('请输入目标文本:')
data = input()
result = {d:0 for d in alphabet}#生成字典


def sort_by_value(d):
    items = d.items()
    backitems = [[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    print(backitems,'\n\n') #按出现次数从大到小输出对应次数和字符
    return [ backitems[i][1] for i in range(0,len(backitems))]#按出现次数从大到小返回字符

for d in data:
    for alpha in alphabet:
        if d == alpha:
            result[alpha] = result[alpha] + 1 #字符出现一次加一

print(''.join(sort_by_value(result))) #连接成字符串

