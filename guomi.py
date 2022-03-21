import binascii

from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


class Sm4:
    """
    国密sm4加解密
    """

    def __init__(self):
        self.crypt_sm4 = CryptSM4()

    def str_to_hexstr(self, hex_str):
        """
        字符串转hex
        :param hex_str: 字符串
        :return: hex
        """
        hex_data = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hex_data)
        return str_bin.decode('utf-8')

    def encrypt(self, value, encrypt_key="3l5butlj26hvv313"):
        """
        国密sm4加密
        :param encrypt_key: sm4加密key
        :param value: 待加密的字符串
        :return: sm4加密后的hex值
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(encrypt_key.encode(), SM4_ENCRYPT)
        encrypt_value = crypt_sm4.crypt_ecb(value.encode())  # bytes类型
        return encrypt_value.hex()

    def decrypt(self, encrypt_value, decrypt_key="3l5butlj26hvv313"):
        """
        国密sm4解密
        :param decrypt_key:sm4加密key
        :param encrypt_value: 待解密的hex值
        :return: 原字符串
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(decrypt_key.encode(), SM4_DECRYPT)
        decrypt_value = crypt_sm4.crypt_ecb(
            bytes.fromhex(encrypt_value))  # bytes类型
        return self.str_to_hexstr(decrypt_value.hex())


if __name__ == '__main__':
    str_data = "测试SM4"
    key = "3l5butlj26hvv313"
    Sm4 = Sm4()
    print("待加密内容：", str_data)
    encoding = Sm4.encrypt(str_data, key)
    print("国密sm4加密后的结果：", encoding)
    print("国密sm4解密后的结果：", Sm4.decrypt(encoding, key))
    encoding = Sm4.encrypt(str_data)
    print("国密sm4加密后的结果：", encoding)
    print("国密sm4解密后的结果：", Sm4.decrypt(encoding))
