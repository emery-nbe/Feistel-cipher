#par NTUMBA BUKASA Emery L2 Génie

def generateKeys(K):
    H = [6,5,2,7,4,1,3,0]
    K = [int (i) for i in '{0:08b}'.format(K)]
    K = [K[i] for i in H]
    k1_prime = K[:4]
    k2_prime = K[4:]
    k1 = [k1_prime[i] ^ k2_prime[i] for i in range(4)]
    k2 = [k2_prime[i] & k1_prime[i] for i in range(4)]
    k1 = [k1[(i-2) % 4] for i in range(4)]
    k2 = [k2[(i+1) % 4] for i in range(4)]

    return k1, k2


def encrypt(text, k1, k2):
    
    def permutation(x):
        return ((x & 1) << 6) | ((x & 2) << 3) | ((x & 4) >> 3) | ((x & 8) >> 6)
    

    def inverse_permutation(x):
        return ((x & 1) << 6) | ((x & 2) << 3) | ((x & 4) >> 3) | ((x & 8) >> 6)
    
    n = permutation(text)

    g0 = n >> 4
    d0 = n & 0xF

    d1 = permutation(g0) ^ k1
    g1 = d0 ^ (g0 | k1)

    d2 = permutation(g1) ^ k2
    g2 = d1 ^ (g1 | k2)
    c = (g2 << 4) | d2

    return inverse_permutation(c)


#decryptage

def decrypt(c, k1, k2):
    c = int(c, 2)
    p = [4,6,0,2,7,3,1,5]
    c = int(''.join([str((c >> 1) & 1) for i in p]), 2)

    d2 = c & 0b1111
    g2 = c >> 4
    
    g1 = permutation_inverse(d2 ^ k2)
    d1 = g2 ^ (g1 | k2)

    g0 = permutation_inverse(d1 ^ k1)
    d0 = g1 ^ (g0 | k1)

    n = (g0 << 4) + d0

    pi_inverse = [7,5,1,3,6,0,2,4]
    n =int(''.join([str((n >> i) & 1) for i in pi_inverse]), 2)

    return n

def permutation_inverse(x):
    return ((x & 1) << 2) + (x >> 2)
