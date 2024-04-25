# sys_analysis/puro.py

import numpy as np
from . import matrix


class ExpertMatrix(matrix.Matrix):

    def __init__(self, factors, row=None, col=None, *args):
        self._check_type(factors)
        self._factors = list(factors)

        factors_len = len(factors)
        if row and col:
            super().__init__(int(row), int(col))
        else:
            super().__init__(factors_len, factors_len)

        self._create_matrix(*args)

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, value):
        self._check_type(value)
        self._factors = value

    def rebuild(self):
        factors_len = len(self._factors)
        self._matrix = []
        self._row = factors_len
        self._col = factors_len

    def _are_args_equal(self, factors):
        return self._factors == factors

    def _validate(self, *args):
        pass

    def _create_matrix(self, *args):
        self._validate(*args)


class CanonicalMatrix(ExpertMatrix):
    def __init__(self, matrix=[], factors=[]):
        self._check_type(matrix)

        # expert's answer
        self.__value_matrix = list(matrix)

        super().__init__(factors)

    @property
    def value_matrix(self):
        return self.__value_matrix

    @value_matrix.setter
    def value_matrix(self, value):
        self._check_type(value)
        self.__value_matrix = list(value)

    def rebuild(self):
        super().rebuild()
        self.__create_matrix()

    def measure_of_closeness(self, matrix):
        if not isinstance(matrix, self.__class__):
            raise TypeError("Not {}!".format(str(self.__class__)))

        if not self._are_args_equal(matrix.factors):
            raise Exception("The factorsutes are not the same!")

        matrix = matrix.get_matrix()
        sum = 0
        for i in range(0, len(self._matrix)):
            sum_col = 0
            for j in range(0, len(self._matrix[i])):
                sum_col += abs(self._matrix[i][j] - matrix[i][j])
            sum += sum_col

        return sum / 2

    def __are_values_matrix_in_factors(self):
        if len(self.__value_matrix) != len(self._factors):
            return False

        result = True
        for item in self.__value_matrix:
            if item not in self._factors:
                result = False
        return result

    def _validate(self, *args):
        if not self.__are_values_matrix_in_factors():
            raise Exception("Not in factorsute set!")

    # Build matrix
    def _create_matrix(self, *args):
        super()._create_matrix(*args)

        value_matrix_len = len(self.__value_matrix)
        result = np.empty([value_matrix_len, value_matrix_len], dtype=int)
        index = 0
        for i in range(0, value_matrix_len):
            for j in range(index, value_matrix_len):
                if self.__value_matrix[i] == self.__value_matrix[j]:
                    result[i][j] = 0
                elif self.__value_matrix[i] < self.__value_matrix[j]:
                    result[i][j] = 1
                    result[j][i] = -1
                else:
                    result[i][j] = -1
                    result[j][i] = 1
            index += 1
        self.clone(result.tolist())


class IntermediateExpertMatrix(ExpertMatrix):

    def __init__(self, factors, *args):
        self._value_set = args
        args_len = len(args)
        super().__init__(factors, args_len, args_len, *args)


    @property
    def value_set(self):
        return self._value_set

    @value_set.setter
    def value_set(self, value_set):
        self._check_type(value_set)
        self._value_set = value_set

    def rebuild(self):
        super().rebuild()
        args = self._value_set
        args_len = len(args)
        self._row = args_len
        self._col = args_len
        self._create_matrix(*args)

    def find_coeff(self):
        if len(self._matrix) == 0:
            raise Exception('Matrix is not created!')

        matrix_values = []
        add_index = 0
        for row in self._matrix:
            for i in range(add_index, self._col):
                if row[i] not in matrix_values:
                    matrix_values.append(row[i])
            add_index += 1

        sum = 0
        for i in matrix_values:
            sum += i

        return round(sum / len(matrix_values), 1)


class DMatrix(IntermediateExpertMatrix):

    def __init__(self, factors, *args):
        self.__difference_matrix = []
        self.__count_of_difference = 0

        super().__init__(factors, *args)

    def get_difference_matrix(self):
        return self.__difference_matrix

    def get_count_of_difference(self):
        return self.__count_of_difference

    def rebuild(self):
        self.__difference_matrix = []
        self.__count_of_difference = 0
        super().rebuild()

    def __are_all_args_canonical_matrix(self, *args):
        for i in args:
            if not isinstance(i, CanonicalMatrix):
                return False
            if not self._are_args_equal(i.factors):
                return False
        return True

    def _validate(self, *args):
        if not self.__are_all_args_canonical_matrix(*args):
            raise TypeError("Not CanonicalMatrix or set factors is not the same!")

    # Build matrix
    def _create_matrix(self, *args):
        super()._create_matrix(*args)

        result = []
        for i in args:
            row = []
            # sum by one matrix
            diff_sum = 0
            for j in args:
                # difference between two matrix
                diff_count = i.measure_of_closeness(j)
                row.append(diff_count)
                diff_sum += diff_count
            result.append(row)
            self.__difference_matrix.append(diff_sum)
            self.__count_of_difference += diff_sum

        self.clone(result)

    def _to_string(self):
        matrix_string = ""
        index = 0
        for row in self._matrix:
            for i in row:
                matrix_string += "{}\t".format(i)
            matrix_string += "|{}|\n".format(self.__difference_matrix[index])
            index += 1
        matrix_string += str(self.__count_of_difference)
        return matrix_string


class PMatrix(IntermediateExpertMatrix):

    def _validate(self, *args):
        factors_len = len(self._factors)
        for matrix in args:
            self._check_type(matrix)
            if len(matrix) != factors_len:
                raise Exception("Matrixes must have same length!")
            for value in matrix:
                if value not in self._factors:
                    raise Exception("Not in factorsute set!")

    def _create_matrix(self, *args):
        super()._create_matrix(*args)

        args = list(args)
        args_len = len(args)
        factors_len = len(self._factors)
        denominator = factors_len ** 3 - factors_len

        result = np.empty([args_len, args_len], dtype=float)
        index = 0
        for i in range(0, args_len):
            for j in range(index, args_len):
                if i == j:
                    result[i][j] = 1
                    continue
                sum = 0
                for k in range(0, factors_len):
                    sum += (args[i][k] - args[j][k]) ** 2
                result[i][j] = result[j][i] = round(1 - (6 * sum) / denominator, 2)
            index += 1

        self.clone(result.tolist())


class ResultExpertMatrix(matrix.Matrix):

    def __init__(self, matrix, coeff=0):

        self._intermediate_matrix = matrix
        self._coeff = coeff

        super().__init__(matrix.row, matrix.col)

        self._create_matrix()

    @property
    def intermediate_matrix(self):
        return self._intermediate_matrix

    @property
    def coeff(self):
        return self._coeff

    def rebuild(self):
        self._matrix = []
        self._row = self._intermediate_matrix.row
        self._col = self._intermediate_matrix.col
        self._create_matrix()

    def _validate(self):
        pass

    def _create_matrix(self):
        self._validate()


class DZMatrix(ResultExpertMatrix):

    def _validate(self):
        if not isinstance(self._intermediate_matrix, DMatrix):
            raise TypeError("Not DMatrix")

    def _create_matrix(self):
        super()._create_matrix()

        result = []
        for matrix_row in self._intermediate_matrix.get_matrix():
            row = []
            for i in matrix_row:
                if i <= self._coeff:
                    row.append(1)
                else:
                    row.append(0)
            result.append(row)

        self.clone(result)


class PZMatrix(ResultExpertMatrix):

    def _validate(self):
        if not isinstance(self._intermediate_matrix, PMatrix):
            raise TypeError("Not PMatrix")

    def _create_matrix(self):
        super()._create_matrix()

        result = []
        for matrix_row in self._intermediate_matrix.get_matrix():
            row = []
            for i in matrix_row:
                if i >= self._coeff:
                    row.append(1)
                else:
                    row.append(0)
            result.append(row)

        self.clone(result)


"""
    Class which build the matrix for two methods: Matching method and Disagreement method
"""
class PUROMethod:

    def __init__(self, factors, *args):
        try:
            self.__factors = np.array(factors, dtype=int)
            self.__answers = np.array(list(args), dtype=int)
        except:
            factors, answers = self.__transform(factors, *args)
            self.__factors = np.array(factors, dtype=int)
            self.__answers = np.array(answers, dtype=int)

        self.__factors = self.__factors.tolist()
        self.__answers = self.__answers.tolist()

    def matching_method(self, coeff=None):
        result = {}

        p_matrix = PMatrix(self.__factors, *self.__answers)
        result['p_matrix'] = p_matrix

        if not coeff:
            coeff = p_matrix.find_coeff()
        pz_matrix = PZMatrix(p_matrix, coeff)
        result['pz_matrix'] = pz_matrix

        return result

    def disagreement_method(self, coeff=None):
        result = {}

        canonical_matrixes = [CanonicalMatrix(matrix=i, factors=self.__factors) for i in self.__answers]
        result['canonical_matrixes'] = canonical_matrixes

        d_matrix = DMatrix(self.__factors, *canonical_matrixes)
        result['d_matrix'] = d_matrix
        result['full_d_matrix'] = self.__full_d_matrix(d_matrix)

        if not coeff:
            coeff = d_matrix.find_coeff()
        dz_matrix = DZMatrix(d_matrix, coeff)
        result['dz_matrix'] = dz_matrix

        return result


    def __full_d_matrix(self, d_matrix):
        import copy

        new_d_matrix = matrix.Matrix(d_matrix.row, d_matrix.col + 1)
        old_matrix = copy.deepcopy(d_matrix.get_matrix())
        diff_matrix = d_matrix.get_difference_matrix()

        for i in range(0, d_matrix.col):
            old_matrix[i].append(diff_matrix[i])

        new_d_matrix.clone(old_matrix)

        return new_d_matrix


    def __transform(self, factors, *args):
        answers = []

        factors = list(factors)

        for row in args:
            answer = []
            for i in row:
                answer.append(factors.index(i))
            answers.append(answer)

        for i in range(0, len(factors)):
            factors[i] = i

        return factors, answers
