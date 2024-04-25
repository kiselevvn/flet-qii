# sys_analysis/functional_completeness.py

import numpy as np

from . import matrix

"""
    Matrixes P01, P10, P11
"""
class PowerSet(matrix.Matrix):

    def __init__(self, source_matrix):
        self._check_type(source_matrix)

        source_matrix_len = len(source_matrix)
        self._source_matrix = source_matrix

        super().__init__(source_matrix_len, source_matrix_len)

        self._build()

    def _is_condition(self, source_matrix, i_index, j_index, k_index):
        return False

    def _build(self):
        result_matrix = np.empty([self._row, self._col], dtype=int)

        for i in range(0, self._row):
            for j in range(0, self._col):
                if i == j:
                    result_matrix[i][j] = 0
                    continue
                sum = 0
                for k in range(0, len(self._source_matrix[0])):
                    if self._is_condition(self._source_matrix, i, j, k):
                        sum += 1
                result_matrix[i][j] = sum
        self.clone(result_matrix.tolist())


class P11(PowerSet):

    def _is_condition(self, source_matrix, i_index, j_index, k_index):
        return source_matrix[i_index][k_index] == source_matrix[j_index][k_index] and source_matrix[i_index][k_index] == 1


class P10(PowerSet):

    def _is_condition(self, source_matrix, i_index, j_index, k_index):
        return source_matrix[i_index][k_index] == 1 and source_matrix[j_index][k_index] == 0


class P01(PowerSet):

    def _is_condition(self, source_matrix, i_index, j_index, k_index):
        return source_matrix[i_index][k_index] == 0 and source_matrix[j_index][k_index] == 1


"""
    Matrixes S, H, G
"""
class MeasureMatrix(matrix.Matrix):

    def __init__(self, P10_matrix, P11_matrix, P01_matrix=None):
        if not isinstance(P10_matrix, matrix.Matrix):
            raise TypeError("Not Matrix")

        if not isinstance(P11_matrix, matrix.Matrix):
            raise TypeError("Not Matrix")

        if P01_matrix and not isinstance(P01_matrix, matrix.Matrix):
            raise TypeError("Not Matrix")

        matrix_len = len(P10_matrix)
        self._p10 = P10_matrix
        self._p11 = P11_matrix
        self._p01 = P01_matrix

        super().__init__(matrix_len, matrix_len)

        self._build()

    def _get_formula_parts(self):
        return 0, 1

    def _build(self, exception=1):
        dividend, division = self._get_formula_parts()
        dividend = dividend.get_matrix()
        division = division.get_matrix()

        result = []
        for i in range(0, self._row):
            row = []
            for j in range(0, self._col):
                if division[i][j] == 0:
                    row.append(exception)
                    continue
                row.append(round(dividend[i][j] / division[i][j], 3))
            result.append(row)
        self.clone(result)


class SMatrix(MeasureMatrix):

    def __init__(self, P10_matrix, P11_matrix, P01_matrix):
        super().__init__(P10_matrix, P11_matrix, P01_matrix)

    def _get_formula_parts(self):
        return self._p01, self._p11 + self._p10

    def _build(self, exception=0):
        super()._build(exception)


class HMatrix(MeasureMatrix):

    def _get_formula_parts(self):
        return self._p11, self._p11 + self._p10


class GMatrix(MeasureMatrix):

    def _get_formula_parts(self):
        return self._p11, (self._p11 + self._p10) + self._p01


"""
    Matrixes P0, S0, H0, G0
"""
class RelationshipMatrix(matrix.Matrix):

    def __init__(self, measure_matrix, threshold_value):
        self._check_measure_matrix(measure_matrix)

        measure_matrix_len = len(measure_matrix)
        self._measure_matrix = measure_matrix.get_matrix()
        self._threshold_matrix = float(threshold_value)

        super().__init__(measure_matrix_len, measure_matrix_len)

        self._build()

    def _build(self):
        result_matrix = np.empty([self._row, self._col], dtype=int)

        for i in range(0, self._row):
            for j in range(0, self._col):
                result_matrix[i][j] = int(self._is_condition(self._measure_matrix, i, j))

        self.clone(result_matrix.tolist())

    def _check_measure_matrix(self, measure_matrix):
        pass


class P0Matrix(RelationshipMatrix):

    def _check_measure_matrix(self, measure_matrix):
        if not isinstance(measure_matrix, P01):
            raise TypeError("Not P01")

    def _is_condition(self, measure_matrix, i_index, j_index):
        return measure_matrix[i_index][j_index] <= self._threshold_matrix and i_index != j_index


class S0Matrix(P0Matrix):

    def _check_measure_matrix(self, measure_matrix):
        if not isinstance(measure_matrix, SMatrix):
            raise TypeError("Not SMatrix")


class H0Matrix(RelationshipMatrix):

    def _check_measure_matrix(self, measure_matrix):
        if not isinstance(measure_matrix, HMatrix):
            raise TypeError("Not HMatrix")

    def _is_condition(self, measure_matrix, i_index, j_index):
        return measure_matrix[i_index][j_index] >= self._threshold_matrix or i_index == j_index


class G0Matrix(H0Matrix):

    def _check_measure_matrix(self, measure_matrix):
        if not isinstance(measure_matrix, GMatrix):
            raise TypeError("Not GMatrix")


"""
    Class which build all matrixes by the method
"""
class FunctionalCompleteness:

    def __init__(self, source_matrix):
        if not isinstance(source_matrix, (list, set)):
            raise TypeError("Must be list or set!")

        self._source_matrix = source_matrix

    def calculate(self, e_p, e_s, e_h, e_g):
        result = {}

        # PowerSet matrixes
        result['P01'] = P01(self._source_matrix)
        result['P10'] = result['P01'].get_transposition() # or P10(self._source_matrix)
        result['P11'] = P11(self._source_matrix)

        # MeasureMatrix matrixes
        result['SMatrix'] = SMatrix(result['P10'], result['P11'], result['P01'])
        result['HMatrix'] = HMatrix(result['P10'], result['P11'])
        result['GMatrix'] = GMatrix(result['P10'], result['P11'], result['P01'])

        # RelationshipMatrix matrixes
        result['P0Matrix'] = P0Matrix(result['P01'], e_p)
        result['S0Matrix'] = S0Matrix(result['SMatrix'], e_s)
        result['H0Matrix'] = H0Matrix(result['HMatrix'], e_h)
        result['G0Matrix'] = G0Matrix(result['GMatrix'], e_g)

        # P0Matrix + P0Matrix^2
        p0_m = P0Matrix(result['P01'], 0)
        full_absorption_matrix = p0_m + (p0_m * p0_m)
        result['full_absorption_matrix'] = self.__full_absorption_matrix_with_row_sum(full_absorption_matrix)

        return result

    def __row_sum(self, row):
        sum = 0
        for i in row:
            sum += i
        return sum

    def __full_absorption_matrix_with_row_sum(self, full_absorption_matrix):
        row = full_absorption_matrix.row
        col = full_absorption_matrix.col

        old_matrix = full_absorption_matrix.get_matrix()

        for i in old_matrix:
            i.append(self.__row_sum(i))

        new_matrix = matrix.Matrix(row, col+1)
        new_matrix.clone(old_matrix)

        return new_matrix
