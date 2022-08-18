import numpy as np

q = 2 ** 1000
t = 2 ** 100

A = np.array([[4, 1, 11, 10], [5, 5, 9, 5], [3, 9, 0, 10], [1, 3, 3, 2], [12, 7, 3, 4], [6, 5, 11, 4], [3, 3, 5, 0]])

# let sA be the secret key , eA be the error 

sA = np.array([[6, 2, 5, 8], [9, 1, 7, 8], [11, 10, 2, 4], [11, 12, 8, 9]])
eA = np.array([[0, 1, -1, 1], [-1, 1, 1, 0], [1, 0, 0, -1], [1, 0, 0, 0], [1, 1, 1, 1], [0, 0, -1, 1], [-1, -1, -1, 1]])
bA = np.matmul(A, sA) % q
bA = np.add(bA, eA) % q
print("Output\n bA ->", bA, "\n A ->", A)

pk = (bA, A)

eA1 = np.array(
    [[1, 0, -1, 1], [-1, 0, 1, 0], [0, 0, 0, -1], [1, -1, 0, 0], [1, 1, 1, 1], [0, -1, -1, 1], [-1, 1, 0, 1]]) % t
eA2 = np.array(
    [[0, 1, 0, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 1], [0, 0, 1, 1], [0, 0, -1, -1], [1, 1, -1, 1]]) % t

uA = np.array([[1, 2, 2, 9], [9, 6, 4, 5], [10, 1, 7, 3], [1, 2, 3, 9]])


# encrypt
def encrypt(number, q, t, pk):
    m = np.array(
        [[number, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) % t
    delta = q // t
    scaled_delta = delta * m

    temp0 = np.matmul(pk[0], uA) % q
    temp0 = (temp0 + eA1) % q
    temp0 = (temp0 + scaled_delta) % q

    temp1 = np.matmul(pk[1], uA) % q
    temp1 = (temp1 + eA2) % q

    return (temp0, temp1)


# decrypyt
def decrypt(ct, q, t, sA):
    delta = q // t
    num = (ct[0] + (np.matmul(ct[1], sA) % q)) % q
    num = (num // delta) % t
    return num[0][0]


# add ciphertext and plaintext
def addition(ct, pt, q, t):
    m = np.array(
        [[pt, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) % t
    delta = q // t
    scaled_delta = (delta * m) % q

    new_ct = (ct[0] + scaled_delta) % q

    return (new_ct, ct[1])


# add two ciphertext
def addcipher(ct1, ct2, q):
    new_ct0 = (ct1[0] + ct2[0]) % q
    new_ct1 = (ct1[1] + ct2[1]) % q

    return (new_ct0, new_ct1)


# multiply plaintext and ciphertext
def multiply(ct, pt, q, t, pk):
    m = np.array([[pt, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) % t
    new_c0 = np.matmul(ct[0], m) % q
    new_c1 = np.matmul(ct[1], m) % q
    return decrypt((new_c0, new_c1), q, t, sA)


# To return encrypted product of plaintext and ciphertext
def mul_plain(ct, pt, q, t, pk):
    return encrypt(multiply(ct, pt, q, t, pk), q, t, pk)


# 1000000001 be the integer to be encrypted
ct = encrypt(1000000001, q, t, pk)
print("Encrypted number->", decrypt(ct, q, t, sA))

# We add 999999999 to the ciphertext (1000000001)
sum1 = addition(ct, 999999999, q, t)
print("add 999999999 to ciphertext->", decrypt(sum1, q, t, sA))

# We add two ciphertext
ct_new = encrypt(123456789, q, t, pk)
sum2 = addcipher(ct, ct_new, q)
print("addition of 2 ciphertext 1000000001 + 123456789->", decrypt(sum2, q, t, sA))

# We multiply 1000000001 to ciphertext (999999999)
product = mul_plain(ct, 99999999, q, t, pk)
print("muliplication 1000000001*999999999->", decrypt(product, q, t, sA))