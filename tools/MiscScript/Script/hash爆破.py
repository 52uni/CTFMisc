hash='dxdydxdudxdtdxeadxekdxea'
def textToarray(hash):
    array =[]
    for c in hash:
        code = ord(c)
        array.append(code-97)
    return array


def arrayTostring(array):
    string=''
    for i in range(0,len(array),2) :
        string+= chr(array[i]*26+array[i+1])
    return string

if __name__ == '__main__':
    print (arrayTostring((textToarray((arrayTostring((textToarray(hash))))))))