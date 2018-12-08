#! /usr/bin/env python3
# _*_ coding=utf-8 _*_
#===================================================================================
#         FILE: crypto.py
#
#  DESCRIPTION: 加密以及解密
#
#        USAGE: 双击py文件，选择1为加密，2为解密
#
#       AUTHOR: jr
#      VERSION: 1.0
#       CREATE: 2018-12-08
#===================================================================================


import os
import getpass
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex


AES_LENGTH = 16

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB
        self.cryptor = AES.new(self.pad_key(self.key).encode(), self.mode)

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def pad(self,text):
        while len(text) % AES_LENGTH != 0:
            text += ' '
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def pad_key(self,key):
        while len(key) % AES_LENGTH != 0:
            key += ' '
        return key

    def encrypt(self, text):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        # 加密的字符需要转换为bytes
        # print(self.pad(text))
        self.ciphertext = self.cryptor.encrypt(self.pad(text).encode())
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode()

    
    def decrypt(self, text):
        # 转为bytes
        text = bytes(text, encoding='utf-8')
        # 解密后，去掉补足的空格用strip() 去掉
        plain_text = self.cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip(' ')


if __name__ == '__main__':
    skey = getpass.getpass("skey:")  # 密钥
    pc = prpcrypt(skey)  # 初始化密钥
    
    mode = input("加密1/解密2：")
    if mode == '1':
        e_str = input("encode:")
        encode = pc.encrypt(e_str)
        print("str:", e_str)
        print("encode:", encode, sep='\n')
    elif mode == '2':
        d_str = input("decode:")
        decode = pc.decrypt(d_str)
        print("str:", d_str)
        print("decode:", decode, sep='\n')

os.system("pause")