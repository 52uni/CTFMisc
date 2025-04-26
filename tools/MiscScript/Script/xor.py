#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# --author：valecalida--
# 异或运算仅允许数字之间的运算，不允许其他类型之间的运算
 
from base64 import b64decode as b64d
message = input("请输入您想要进行操作的字符串 >>>")
if message[0:2] == "b\'":
    message = message[2:-1]
#print(message)
flags = input("请输入解码的样式(例：flag、ctfhub) >>>")
 
 
def b64_detect(msg):
    try:
        cipher_text = b64d(msg)
    except BaseException as e:
        print("您输入的值好像不能使用Base64解密,请再尝试别的方法")
    else:
        res = []
        for i in range(len(flags)):
            res.append(cipher_text[i] ^ ord(flags[i]))
    finally:
        return res, cipher_text
 
 
def decode_xor():
    result = ''
    res, cipher_text =b64_detect(message)
    if res[0] - res[1] == 0:
        print("这是一个值不变的Xor运算")
        for i in range(len(cipher_text)):
            result += chr(res[0] ^ cipher_text[i])
        return result
    elif res[0] - res[1] == 1:
        print("这是一个值递减的Xor运算")
        for i in range(len(cipher_text)):
            result += chr((res[0] - i) ^ cipher_text[i])
        return result
    elif res[0] - res[1] == -1:
        print("这是一个值递增的Xor运算")
        for i in range(len(cipher_text)):
            result += chr((res[0] + i) ^ cipher_text[i])
        return result
    else:
        print("这好像不是Xor运算，再试试别的吧")
        return result
 
 
print("\t程序返回的结果是 >>", decode_xor())
 
 