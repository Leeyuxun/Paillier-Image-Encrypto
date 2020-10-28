from gmpy2 import lcm, gcd, invert, powmod, mpz, bit_set, next_prime
import random
import pickle
# 公钥类
from mako.exceptions import RuntimeException


class PaillierPublicKey():
    def __init__(self, n, g, r):
        self.n = n
        self.g = g
        self.r = r
        self.nSquare = n ** 2


# 私钥类
class PaillierPrivateKey():
    def __init__(self, l, u, n):
        self.l = l
        self.u = u
        self.n = n
        self.nSquare = n ** 2


# 密钥类
class PaillierKeyPair():
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

# L函数
def L(x, n):
    return (x-1) // n


# 大素数生成
def generateLargePrime(nLength):
    rf = random.SystemRandom()
    r = mpz(rf.getrandbits(nLength))
    r = bit_set(r, nLength-1)
    return next_prime(r)

# 密钥生成
def generateKey():
    n = 0
    p = q = None
    nLength = 12
    while n.bit_length() != nLength and p == q:
        p = generateLargePrime(nLength // 2)
        q = generateLargePrime(nLength // 2)
        n = p * q

    l = lcm(p-1, q-1)
    if gcd(p*q, (p-1)*(q-1)) != 1:
        raise RuntimeException("错误：gcd（N，tot（N））！= 1")

    g = mpz()
    while gcd(g, n**2) != 1:
        g = random.SystemRandom().randrange(1, n)

    r = random.SystemRandom().randrange(1, n)
    u = invert(L(powmod(g, l, n**2), n), n)
    publicKey = PaillierPublicKey(n, g, r)
    privateKey = PaillierPrivateKey(l, u, n)
    return PaillierKeyPair(publicKey, privateKey)

# 加密
def encrypt(m, publicKey):
    a = powmod(publicKey.g, m, publicKey.nSquare)
    b = powmod(publicKey.r, publicKey.n, publicKey.nSquare)
    c = (a * b) % publicKey.nSquare
    return c

# 解密
def decrypt(c, privateKey):
    c = c % privateKey.n**2
    a = powmod(c, privateKey.l, privateKey.nSquare)
    return L(a, privateKey.n) * privateKey.u % privateKey.n

def main():
    keyPair = generateKey()
    print("公私密钥对生成中···")
    print("公钥：(n=", keyPair.publicKey.n, "g=", keyPair.publicKey.g, "r=", keyPair.publicKey.r, ")\n私钥：(n=",
          keyPair.privateKey.n, "l=", keyPair.privateKey.l, "u=", keyPair.privateKey.u, ")")
    m1 = mpz(input("请输入第一个加数："))
    c1 = encrypt(m1, keyPair.publicKey)
    print("加密后的内容为：", c1)
    m2 = mpz(input("请输入第二个加数："))
    c2 = encrypt(m2, keyPair.publicKey)
    print("加密后的内容为：", c2)
    c3 = c1 * c2
    print("密文相乘后的结果为: ", c3)
    print("解密结果为：", decrypt(c3, keyPair.privateKey))
    c4 = c1 * invert(c2, keyPair.publicKey.n ** 2)
    print("密文相除后的结果为：", c4)
    print("解密结果为：", decrypt(c4, keyPair.privateKey))
    # 存储公私钥
    with open(r'./client/keys/pub', 'w+', encoding='utf-8') as pub:
        pub.write(str(keyPair.publicKey.n) + '\n')
        pub.write(str(keyPair.publicKey.g) + '\n')
        pub.write(str(keyPair.publicKey.r) + '\n')
    with open(r'./client/keys/pri', 'w+', encoding='utf-8') as pri:
        pri.write(str(keyPair.privateKey.n) + '\n')
        pri.write(str(keyPair.privateKey.l) + '\n')
        pri.write(str(keyPair.privateKey.u) + '\n')