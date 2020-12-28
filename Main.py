from functools import reduce


def gcd(a1, b1):
    a1 = abs(a1)
    b1 = abs(b1)
    while a1:
        a1, b1 = b1 % a1, a1
    return b1
# gcd() returns the gcd of the 2 inputs


def gcd_list(l1):
    return reduce(gcd, l1)
# gcd_list() returns the gcd of the given list of numbers


def print_matrix(matrix, dimension, mode):
    global STEP
    print("Step", STEP)
    if mode == 'coefficient matrix':
        print('The Coefficient Matrix: ')
        for i in range(dimension):
            for j in range(dimension):
                if matrix[i][j] == 0:
                    print(0, end='')
                else:
                    print("%.2f" % matrix[i][j], end='')
                print("  ", end='')
            print()
    else:
        print('The Augmented Coefficient Matrix: ')
        for i in range(dimension):
            for j in range(dimension + 1):
                if matrix[i][j] == 0:
                    print(0, end='')
                else:
                    print("%.2f" % matrix[i][j], end='')
                print("  ", end='')
            print()
    print()
    STEP += 1
    print('=================================')
# print_matrix() prints the matrix in a good form base on which mode you use
# (mode : 'coefficient matrix' -> prints the nonAugmented matrix, mode: anything else -> prints the augmented matrix)
# we print each element by 2 decimal like 'anything.xx' except zero


def print_vector(vector, dimension):
    for i in range(dimension):
        if vector[i] == 0:
            print(0)
        else:
            print(vector[i])
# print_vector() prints the answer vector in a good form


def interchange(matrix, dimension, row1, row2):
    r1 = matrix[row1]
    r2 = matrix[row2]
    matrix[row1] = r2
    matrix[row2] = r1
    print('Interchange Executed!')
    print_matrix(matrix, dimension, '')
# interchange() changes 2 given row of the matrix


def scale(matrix, dimension, row_index, constant):
    print('constant', constant)
    r = matrix[row_index]
    for i in range(dimension + 1):
        r[i] = r[i] * constant
    matrix[row_index] = r
    print('Scale Executed')
    print_matrix(matrix, dimension, '')
# scale() get a row of a matrix and multiply it with the constant it gets from input


def initialize(matrix, dimension, current_row, current_column):
    if matrix[current_row][current_column] == 0:
        for i in range(dimension):
            if matrix[i][0] != 0:
                interchange(matrix, dimension, i, 0)
                return
# initialize() we use it once at the beginning for placing a row on top which the first element of that row is nonzero


def replacement(matrix, dimension, current_row, current_column):
    for i in range(current_row + 1, dimension, 1):
        if matrix[i][current_column] != 0:
            should_get_zero = matrix[i][current_column]
            temp = matrix[current_row].copy()
            if matrix[current_row][current_column] != 0:
                for k in range(dimension + 1):
                    if matrix[current_row][current_column] != 0:
                        temp[k] *= (-1 * should_get_zero) / matrix[current_row][current_column]
                for j in range(dimension + 1):
                    matrix[i][j] += temp[j]
    print("Replacement Executed!")
    print_matrix(matrix, dimension, '')
# replacement() finding, multiplying, adding and setting a row by the other one


def fix(matrix, dimension):
    new_matrix = matrix
    k = 0
    for i in range(dimension):
        flag = True
        for j in range(dimension + 1):
            if matrix[i][j] != 0:
                flag = False
                new_matrix[k] = matrix[i]
                k += 1
                break
        if flag:
            ttmp = [0 for q in range(dimension + 1)]
            new_matrix[k] = ttmp
            k += 1
    # augmentedA = new_matrix
    return new_matrix
# fix() it puts from top to bottom the row which has the leftMost pivot


def optimize(matrix, dimension):
    for i in range(dimension):
        if gcd_list(matrix[i]) != 1:
            if gcd_list(matrix[i]) != 0:
                scale(matrix, dimension, i, 1 / gcd_list(matrix[i]))
# optimize() simplifies the rows and divide them by they gcd if possible


def reduced_echelon_form_replacement(matrix, dimension, current_row, current_column):
    for i in range(current_row - 1, -1, -1):
        if matrix[i][current_column] != 0:
            should_get_zero = matrix[i][current_column]
            temp = matrix[current_row].copy()
            if matrix[current_row][current_column] != 0:
                for k in range(dimension + 1):
                    temp[k] *= (-1 * should_get_zero) / matrix[current_row][current_column]
            for j in range(dimension + 1):
                matrix[i][j] += temp[j]
    print("Reduced Echelon Form Replacement Executed!")
    print_matrix(matrix, dimension, '')
# reduced_echelon_form_replacement() finding, multiplying and adding a row by the other one to make it reduced form


def check_if_has_answer(matrix, dimension):
    confirm = True
    for i in range(dimension):
        flag = False
        for j in range(dimension):
            if matrix[i][j] != 0:
                flag = True
        if not flag and matrix[i][dimension] != 0:
            confirm = False
            return confirm
    return confirm
# check_if_has_answer returns if the system has a solution or not by checking [0 0 ... 0 | b] and b == 0


def find_pivot_positions(matrix, dimension):
    ans = []
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j] != 0:
                ans.append(j)
                break
    return ans
# find_pivot_positions() finds and returns pivot columns index


def find_zeroes(matrix, dimension):
    ans = []
    for i in range(dimension):
        counter = 0
        for j in range(dimension):
            if matrix[i][j] == 0:
                counter += 1
        ans.append(counter)
    return ans
# find_zeroes() returns how many 0 we got in each row


def main():
    n = int(input())
    A = [[0 for i in range(n)] for j in range(n)]
    b = []
    for i in range(n):
        tmp = input().split(' ')
        tmp = [float(a) for a in tmp]
        A[i] = tmp
    # finish building matrix A

    b = input().split()
    b = [float(a) for a in b]
    # finish building vector b

    augmentedA = [[0 for i in range(n + 1)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            augmentedA[i][j] = A[i][j]
    for i in range(n):
        augmentedA[i][n] = b[i]
    # finish building augmented matrix A

    column = 0
    for i in range(n):
        row = i
        initialize(augmentedA, n, row, column)
        replacement(augmentedA, n, row, column)
        column += 1
    for i in range(n):  # round the numbers
        for j in range(n + 1):
            augmentedA[i][j] = round(augmentedA[i][j], 2)

    augmentedA = fix(augmentedA, n)
    # finish building echelon form

    for i in range(n - 1, -1, -1):
        row = i
        for j in range(n + 1):
            if augmentedA[row][j] != 0:
                column = j
                break
        reduced_echelon_form_replacement(augmentedA, n, row, column)
    for i in range(0, n, 1):
        for j in range(0, n + 1, 1):
            if augmentedA[i][j] != 0:
                scale(augmentedA, n, i, (1 / augmentedA[i][j]))
                break
    for i in range(n):  # round the numbers
        for j in range(n + 1):
            augmentedA[i][j] = round(augmentedA[i][j], 2)
    augmentedA = fix(augmentedA, n)
    # finish building reduced echelon form

    pivots = find_pivot_positions(augmentedA, n)
    x = []  # the answer vector
    if check_if_has_answer(augmentedA, n):
        if len(pivots) == n:  # each row has a pivot position
            for i in range(n):
                for j in range(n + 1):
                    if augmentedA[i][j] != 0:
                        x.append(augmentedA[i][n])
                        break
            print("\nThe answer vector:")
            print_vector(x, n)
        else:
            print("\nThis Linear Equation has infinitely many solutions.")
    else:
        print("\nThis Linear Equation has no solutions")
    # finish printing the answer!
# connect all the functions and gets inputs and prints the outputs


STEP = 1
# a global variable that indicates the step we are in
main()
# call for the function main to solve the equations
