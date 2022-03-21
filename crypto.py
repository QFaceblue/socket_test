# -*- coding：utf-8 -*-
import base64
import hashlib
import hmac
import time

from Crypto.Cipher import AES
from Crypto.Cipher import DES3, DES


class Use_aes:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    def to_16(self, key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)  # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def decodebytes(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(
            text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密


class Use_des:
    """
    new(key, mode, *args, **kwargs)
    key:必须8bytes倍数介于16-24
    mode：
    iv:初始化向量适用于MODE_CBC、MODE_CFB、MODE_OFB、MODE_OPENPGP，4种模式
        ``MODE_CBC``, ``MODE_CFB``, and ``MODE_OFB``长度为8bytes
        ```MODE_OPENPGP```加密时8bytes解密时10bytes
        未提供默认随机生成
    nonce：仅在 ``MODE_EAX`` and ``MODE_CTR``模式中使用
            ``MODE_EAX``建议16bytes
            ``MODE_CTR``建议[0, 7]长度
            未提供则随机生成
    segment_size：分段大小，仅在 ``MODE_CFB``模式中使用，长度为8倍数，未指定则默认为8
    mac_len： 适用``MODE_EAX``模式，身份验证标记的长度（字节），它不能超过8（默认值）
    initial_value：适用```MODE_CTR```，计数器的初始值计数器块。默认为**0**。
    """

    def __init__(self, key):
        self.key = key
        self.mode = DES.MODE_ECB

    def encrypt(self, text):
        """
        传入明文
        :param text:bytes类型，长度是KEY的倍数
        :return:
        """
        if not isinstance(text, bytes):
            text = bytes(text, 'utf-8')
        # x = len(text) % 8
        # text = text + b'\0' * (8-x)
        while len(text) % 8 != 0:
            text += b'\0'
        cryptor = DES.new(self.key, self.mode)
        ciphertext = cryptor.encrypt(text)
        return ciphertext

    def decrypt(self, text):
        cryptor = DES.new(self.key, self.mode)
        plain_text = cryptor.decrypt(text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        return st


class Use_des3:
    """
    new(key, mode, *args, **kwargs)
    key:必须8bytes倍数介于16-24
    mode：
    iv:初始化向量适用于MODE_CBC、MODE_CFB、MODE_OFB、MODE_OPENPGP，4种模式
        ``MODE_CBC``, ``MODE_CFB``, and ``MODE_OFB``长度为8bytes
        ```MODE_OPENPGP```加密时8bytes解密时10bytes
        未提供默认随机生成
    nonce：仅在 ``MODE_EAX`` and ``MODE_CTR``模式中使用
            ``MODE_EAX``建议16bytes
            ``MODE_CTR``建议[0, 7]长度
            未提供则随机生成
    segment_size：分段大小，仅在 ``MODE_CFB``模式中使用，长度为8倍数，未指定则默认为8
    mac_len： 适用``MODE_EAX``模式，身份验证标记的长度（字节），它不能超过8（默认值）
    initial_value：适用```MODE_CTR```，计数器的初始值计数器块。默认为**0**。
    """

    def __init__(self, key):
        self.key = key
        self.mode = DES3.MODE_ECB

    def encrypt(self, text):
        """
        传入明文
        :param text:bytes类型，长度是KEY的倍数
        :return:
        """
        if not isinstance(text, bytes):
            text = bytes(text, 'utf-8')
        # x = len(text) % 8
        # text = text + b'\0' * (8-x)
        while len(text) % 16 != 0:
            text += b'\0'
        cryptor = DES3.new(self.key, self.mode)
        ciphertext = cryptor.encrypt(text)
        return ciphertext

    def decrypt(self, text):
        cryptor = DES3.new(self.key, self.mode)
        plain_text = cryptor.decrypt(text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        return st


def use_md5(test):
    if not isinstance(test, bytes):
        test = bytes(test, 'utf-8')
    m = hashlib.md5()
    m.update(test)
    return m.hexdigest()


def use_hmac(key, text):
    if not isinstance(key, bytes):
        key = bytes(key, 'utf-8')
    if not isinstance(text, bytes):
        text = bytes(text, 'utf-8')
    h = hmac.new(key, text, digestmod='MD5')
    return h.hexdigest()


def use_sha(text):
    if not isinstance(text, bytes):
        text = bytes(text, 'utf-8')
    sha = hashlib.sha1(text)
    encrypts = sha.hexdigest()
    return encrypts


if __name__ == '__main__':
    aes_test = Use_aes("assssssssdfasasasasa")
    start = time.time()
    for i in range(1000):
        a = aes_test.encrypt("测试!1")
        b = aes_test.decodebytes(a)
    print(a, b)
    print(time.time() - start)
    # rsa_test = USE_RSA()
    # a = rsa_test.rsaEncrypt("测试加密")
    # b = rsa_test.rsaDecrypt(a)

    des_test = Use_des(b"12345678")
    start = time.time()
    for i in range(1000):
        a = des_test.encrypt("测试加密1")
        b = des_test.decrypt(a)
    print(a, b)
    print(time.time() - start)

    des3_test = Use_des3(b"123456789qazxswe")
    start = time.time()
    for i in range(1000):
        a = des3_test.encrypt("测试加密1")
        b = des3_test.decrypt(a)
    print(a, b)
    print(time.time() - start)

    md5_test = use_md5("测试签名")
    print(md5_test)
    hmac_test = use_hmac("123456", "测试")
    print(hmac)
    sha_test = use_sha("测试加密")
    print(sha_test)
