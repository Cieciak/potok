import numpy, random

def max_1norm(matrix):
    '''Maximum Taxicab distance of a basis vector'''
    norms = numpy.sum(numpy.abs(matrix), axis=0)
    return numpy.max(norms)

def unimodular(dimension: int):
    base = numpy.random.randint(-10, 10, size=(dimension, dimension))
    determinant = numpy.linalg.det(base)
    inverse = numpy.linalg.inv(base)
    sign = numpy.sign(determinant)
    
    return sign * numpy.round(determinant) * inverse


class GGH:

    @staticmethod
    def orthogonality_defect(basis: numpy.ndarray):
        numerator = 1
        for vector in basis.T:
            numerator *= numpy.linalg.norm(vector, ord = 2)

        return numerator / abs(numpy.linalg.det(basis))

    @staticmethod
    def get_sigma(private: numpy.ndarray):
        inverse = numpy.linalg.inv(private)
        return 0.5 / max_1norm(inverse)

    @staticmethod
    def get_private_basis(dimension: int, bound: int, k: int):
        basis = numpy.random.randint(
            low   = -bound,
            high  =  bound,
            size  =  (dimension, dimension),
            dtype =  numpy.int64,
        )

        return basis + numpy.identity(
            n     = dimension,
            dtype = numpy.int64,
        ) * k
    
    @staticmethod
    def get_unimodular_private(dimension: int, bound: int, k: int):
        basis = unimodular(dimension)
        return basis
    
    @staticmethod
    def get_unimodular_public(private: numpy.ndarray, steps: int):
        public = unimodular(private.shape[0])
        return public
    
    @staticmethod
    def get_public_basis(private: numpy.ndarray, steps: int):
        '''Mix private basis usng itself'''
        basis = private.copy()
        for _ in range(steps):
            GGH.mix(basis, private) # It used to reduce to zero matrix often

        return basis

    @staticmethod
    def get_error(dimension: int, sigma: float):
        return (2 * numpy.random.randint(
            low  = 0,
            high = 2,
            size = (dimension, )
        ) - 1) * random.random() * sigma * 0.1

    @staticmethod
    def get_transformation(private: numpy.ndarray, public: numpy.ndarray):
        return numpy.linalg.inv(public) @ private

    @staticmethod
    def check_error(vector: numpy.ndarray, private: numpy.ndarray):
        inverse = numpy.linalg.inv(private)
        return vector.dot(inverse)

    @staticmethod
    def mix(matrix: numpy.ndarray, mixer: numpy.ndarray):
        '''For each basis vector add random linear combination of other'''
        row, column = matrix.shape
        for i in range(column):
            matrix[:, i] += GGH.linear(mixer)

    @staticmethod
    def linear(matrix: numpy.ndarray):
        '''Return linear combination of vectors in the matrix'''
        row, column = matrix.shape
        vector = numpy.zeros((column, ), dtype = numpy.int64)
        for i in range(column):
            vector += matrix[:, i] * random.choices(
                population = [-1, 0, 1], # Proposed in doc
                weights    = [ 1, 5, 1], # 
                k          = 1
            )[0]

        return vector

    @staticmethod
    def encrypt(public: numpy.ndarray, vector: numpy.ndarray, error: numpy.ndarray):
        return vector.dot(public) + error

    @staticmethod
    def decrypt(private: numpy.ndarray, transform: numpy.ndarray, cipher: numpy.ndarray):
        inverse = numpy.linalg.inv(private)
        return numpy.round(cipher.dot(inverse)).dot(transform)

DIM = 4
RAN = 4
ORT = 1

PRIVATE_BASIS = GGH.get_unimodular_private(DIM, RAN, ORT)
print('Private basis:')
print(PRIVATE_BASIS)
print(f'Orthogonality defect: {GGH.orthogonality_defect(PRIVATE_BASIS)}')
print()


PUBLIC_BASIS = GGH.get_unimodular_public(PRIVATE_BASIS, 2 * DIM)
print('Public:')
print(PUBLIC_BASIS)
print(f'Orthogonality defect: {GGH.orthogonality_defect(PUBLIC_BASIS)}')
print()

print(f'Orthogonality defect ratio: {GGH.orthogonality_defect(PUBLIC_BASIS) / GGH.orthogonality_defect(PRIVATE_BASIS)}\n')

MESSAGE = numpy.random.randint(0, 2 ** 10, (DIM, ), dtype=numpy.int64)
print('Message:')
print(MESSAGE)
print()

ERROR = GGH.get_error(DIM, GGH.get_sigma(PRIVATE_BASIS))
print('Error:')
print(ERROR)
print()

CIPHER = GGH.encrypt(PUBLIC_BASIS, MESSAGE, ERROR)
print('Cipher:')
print(CIPHER)
print()

DECRYPTED = GGH.decrypt(PRIVATE_BASIS, GGH.get_transformation(PRIVATE_BASIS, PUBLIC_BASIS), CIPHER)
print('Decrypted:')
print(DECRYPTED)
print()

CHECK = GGH.check_error(ERROR, PRIVATE_BASIS)
print('Check:')
print(numpy.round(CHECK))
print()

TRANSFORM = GGH.get_transformation(PRIVATE_BASIS, PUBLIC_BASIS)
print('Transform:')
print(TRANSFORM)
print()


print('Diff:')
print(numpy.round(DECRYPTED - MESSAGE, 2))
print()