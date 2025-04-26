from binascii import crc32
import string
import zipfile
dic=string.printable
def CrackCrc(crc):
    for i in dic :
        # print (i)
        for j in dic:
            for p in dic:
                for q in dic:
                    s=i+j+p+q
                    # print (crc32(bytes(s,'ascii')) & 0xffffffff)
                    if crc == (crc32(bytes(s,'ascii')) & 0xffffffff):
                        print (s)
                        return
 
def getcrc32(fname):
    l=[]
    file = fname
    f = zipfile.ZipFile(file, 'r')
    global fileList
    fileList =f.namelist ()
    print (fileList)
    # print (type(fileList))
    for filename in fileList:
        Fileinfo = f.getinfo(filename)
        # print(Fileinfo)
        crc = Fileinfo.CRC
        # print ('crc',crc)
        l.append(crc)
    return l
 
def main (filename=None):
    l = getcrc32(filename)
    # print(l)
    for i in range(len(l)):
        print(fileList[i], end='的内容是:')
        CrackCrc(l[i])
 
if __name__  == "__main__":
    main ('password.zip')
# 4字节