import numpy

def max_1norm(matrix):
    norms = numpy.sum(numpy.abs(matrix), axis=0)
    max_norm = numpy.max(norms)
    return max_norm

def orthogonality_defect(matrix):
    numerator = 1
    for vector in matrix.T:
        numerator *= numpy.linalg.norm(vector, ord = 2)
    return numerator / abs(numpy.linalg.det(matrix))

class GGH:

    @staticmethod
    def orthogonal(matrix):
        x, y = matrix.shape
        if x != y: raise Exception('Matrix is not square')
        maximum = numpy.max(matrix)
        return (numpy.linalg.det(numpy.sqrt(matrix @ matrix.T)) ** (1 / x)) / maximum

    @staticmethod
    def encrypt(public_key, message, error_magnitude):
        vector = message.dot(public_key)
        return vector + (numpy.random.random(message.shape) - 0.5) * error_magnitude
    
    
# Basis of the lattice

R = [
    [10, 2],
    [ 1, 8],
]
R = numpy.array(R)

R_INV = numpy.linalg.inv(R)

DEF = orthogonality_defect(R)
RHO = max_1norm(R_INV)
SIGMA = 1 / (2 * RHO)


print('Private key:')
print(R)

print('Private key inverse:')
print(R_INV)
print()

print('Rho: ', RHO)
print('Sigma: ', SIGMA)
print('Defect: ', DEF)