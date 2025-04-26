import zipfile
import binascii
import string
from tqdm import tqdm
 
fname_fcrc = {}
fcrc_fnames = {}
fcrc_value = {}
 
archive = zipfile.ZipFile("C:/Users/Lucian/Downloads/flag.zip")
print('正在提取crc：')
for fname in tqdm(archive.namelist()):
    name_info = archive.getinfo(fname)
    fcrc = name_info.CRC
    fname_fcrc[fname] = fcrc
    fcrc_fnames[fcrc] = []
 
for fname in fname_fcrc:
    fcrc = fname_fcrc[fname]
    fcrc_fnames[fcrc].append(fname)
 
print('正在破解3字节长crc')
for i in tqdm(range(0, 256)):
    tempi = hex(i)[2:]
    if len(tempi) == 1:
        tempi = '0' + tempi
    tempi = binascii.a2b_hex(tempi)
 
    for j in range(0, 256):
        tempj = hex(j)[2:]
        if len(tempj) == 1:
            tempj = '0' + tempj
        tempj = binascii.a2b_hex(tempj)
 
        for k in range(0, 256):
            tempk = hex(k)[2:]
            if len(tempk) == 1:
                tempk = '0' + tempk
            tempk = binascii.a2b_hex(tempk)
 
            fcrc = binascii.crc32(tempi + tempj + tempk)
            if fcrc in fcrc_fnames:
                fcrc_value[fcrc] = tempi + tempj + tempk
 
print(f'总crc个数：{len(fcrc_fnames)}，破解成功个数：{len(fcrc_value)}')
 
result = {}
print('正在将结果编码：')
for fcrc in tqdm(fcrc_value):
    for fname in fcrc_fnames[fcrc]:
        result[fname] = fcrc_value[fcrc].decode()
 
print('编码结果：')
for i in range(0, len(result)):
    print(result[f'{i}.txt'], end='')
