import bitarray

import random
from sympy import nextprime


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def gen_right_prime_number(start, end):
    x = nextprime(random.randint(0xfffffff, 0xffffffffffffff))
    while x % 4 != 3:
        x = nextprime(random.randint(0xfffffff, 0xffffffffffffff))
    return x


def create_rand_key(m):
    # 1 step
    q = gen_right_prime_number(0xfffffff, 0xffffffffffffff)
    p = gen_right_prime_number(0xffffffff, 0xffffffffffffff)
    N = p * q
    # 2 step
    s = N
    while gcd(N, s) > 1:
        s = random.randint(1, N)
    u = [(s * s) % N]
    #step 3
    x = []
    for i in range(0, m):
        u.append(u[i]**2 % N)
        x.append(u[i+1] & 0b1)
    #step 4
    while len(x) % 8 > 0:
        x = [0].append(x)
    # result = []
    # for i in range(0, len(x), 8):
    #     k = 0
    #     for j in range(0, 8):
    #         k += x[i+j] * (7 - j)**2
    #     result.append(k)
    return x


def str2bits(message):
    bit_str = message.encode('utf-8')
    print('encode: ', bit_str)
    result = bitarray.bitarray()
    temp = []
    for i in bit_str:
        order = 0x80
        for j in range(0, 8):
            temp.append(i & order > 0)
            order = order >> 1
    result += [i for i in temp]
    print('bit string: ', result)
    return result


def bits2str(bit_str):
    resString = b''
    for i in range(0, len(bit_str), 8):
        symbol = 0
        for j in range(0, 8):
            symbol += bit_str[i + j] * 2 ** (7 - j)
        resString += symbol.to_bytes(1, byteorder='little', signed=False)
    return resString


def xor_bits_str(Fstr, Sstr):
    result = bitarray.bitarray()
    temp = []
    for i in range(0, len(Fstr)):
        temp.append((int(Fstr[i]) + int(Sstr[i])) % 2)
    result += [i for i in temp]
    return result


def xor_bit_str(str):
    result = False
    for i in range(0, len(str)):
        result = (result or str[i]) and not (result and str[i])
    return int(result)


def add_bits_str(Fstr, Sstr):
    result = bitarray.bitarray()
    temp = []
    for i in range(0, len(Fstr)):
        temp.append(int(Fstr[i]) == 1 and int(Sstr[i]) == 1)
    result += [i for i in temp]
    # print('+++++++++++++++++++++++++++++++++++++++')
    # print(Fstr)
    # print(Sstr)
    # print(result)
    # print('+++++++++++++++++++++++++++++++++++++++')
    return result


def gamming_message(message):
    m = len(message)
    key = bitarray.bitarray()
    rand_key = create_rand_key(m * 8)
    key += [i for i in rand_key]
    print(message)
    bit_message = str2bits(message)
    chiper_message = xor_bits_str(bit_message, key)
    print(bit_message)
    print(key)
    print(chiper_message)
    return chiper_message, rand_key


def hi_kvadrat_test(Str):
    Zeros = Str.count(0)
    Units = Str.count(1)
    N = len(Str)
    S = N * ((Zeros / N - 0.5) * (Zeros / N - 0.5) / 0.5
             + (Units / N - 0.5) * (Units / N - 0.5) / 0.5)
    if S > 5.991:
        print('Гипотеза о равномерности последовательности отвергается')
    else:
        print('Гипотеза о равномерности последовательности не отвергается')
    print(S)
    return S > 5.991


def scrambler(polinom, startstr, message):
    result_key = bitarray.bitarray()
    scramStr = []
    for i in range(0, len(startstr) - 1):
        scramStr.append(int(startstr[i]))
    print(scramStr)
    temp = []

    for i in range(0, 8 * len(message)):
        nextbit = xor_bit_str(add_bits_str(scramStr, polinom))
        temp.append(scramStr[7])
        # print(scramStr)
        for j in range(7, 0, -1):
            scramStr[j] = scramStr[j-1]
        scramStr[0] = nextbit
        # print(scramStr)
    # print('temp = ', temp)
    # print(temp.count(0), temp.count(1))
    hi_kvadrat_test(temp)
    result_key += [i for i in temp]
    bit_message = str2bits(message)
    print('bit message: ', bit_message)
    chiper_message = xor_bits_str(bit_message, result_key)
    return chiper_message, result_key


def decipher(cipher_bit_text, key):
    dechiper_message = xor_bits_str(cipher_bit_text, key)
    print('dec message: ', dechiper_message)
    resString = bits2str(dechiper_message)
    print(resString.decode('utf-8'))
    return resString.decode('utf-8')


def find_period():
    input = open('polinom.txt', 'r')
    polinom = input.read()
    input.close()
    input = open('startVector.txt', 'r')
    startVector = input.read()
    input.close()

    scramStr = []
    for i in range(0, len(startVector) - 1):
        scramStr.append(int(startVector[i]))
    temp = []
    i = 0

    while True:
        if scramStr in temp:
            print('Find period of scrambler = ', len(temp) - temp.index(scramStr))
            break
        iterStr = []
        for item in scramStr:
            iterStr.append(item)
        temp.append(iterStr)
        nextbit = xor_bit_str(add_bits_str(scramStr, polinom))
        lastNum = scramStr[7]
        for j in range(7, 0, -1):
            scramStr[j] = scramStr[j - 1]
        scramStr[0] = nextbit
        i += 1


def move_bit_left(bitStr):
    return bitStr[1:] + bitStr[:1]


def correlation():
    input = open('keyScram.txt', 'r')
    key = input.read()
    input.close()

    newKey = move_bit_left(key)
    newKey = xor_bits_str(key, newKey)
    e = 0
    n = 0
    for i in range(0, len(key)):
        if int(key[i]) == int(newKey[i]):
            e += 1
        else:
            n += 1
    print('e =', e, 'n =', n, 'size = ', len(key))
    print('result = ', abs((e - n) / len(key)))
    if abs((e - n) / len(key)) < 0.05 :
        print("Гипотеза о корреляции не отвергается")
    else:
        print("Гипотеза о корреляции отвергается")


def balance():
    input = open('keyScram.txt', 'r')
    key = input.read()
    input.close()
    e = 0
    n = 0

    for i in range(0, len(key)):
        if int(key[i]) == 1:
            e += 1
        else:
            n += 1

    print('e =', e, 'n =', n, 'size = ', len(key))
    print('result = ', abs(e - n))
    if (abs(e - n) <= 1):
        print("Последовательность сбалансирована")
    else:
        print("Последовательность не сбалансирована")


def cyclicity():
    input = open('keyScram.txt', 'r')
    key = input.read()
    input.close()

    tmp = []
    cycle = []
    tmp.append(key[0])
    for i in range(1, len(key)):
        if key[i - 1] != key[i]:
            cycle.append(tmp)
            tmp = [key[i]]
        else:
            tmp.append(key[i])
    lens = []
    for i in range(0, len(cycle)):
        lens.append(len(cycle[i]))
    lens.sort()
    count = {}
    for i in range(0, len(lens)):
        count[i + 1] = lens.count(lens[i])
    for i in count.keys():
        # ???????
        if abs(count[i] / len(cycle)) > pow(1/2, i):
            print("Последовательность не циклична")
            return
    print("Последовательность циклична")


def f(x):
    return x[1:] + x[:1]


def brent():
    input = open('keyScram.txt', 'r')
    x0 = input.read()
    input.close()

    # инициализация переменных
    tortoise = x0
    hare = f(x0)
    power = lam = 1

    # поиск цикла
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1

    # определение длины цикла
    mu = 0
    tortoise = hare = x0
    for i in range(lam):
        hare = f(hare)
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1

    if mu == 0:
        print('Строка не является циклической.')
    else:
        print(f'Строка является циклической. Длина цикла: {lam}, сдвиг: {mu}.')

    # возврат результата
    return lam, mu
