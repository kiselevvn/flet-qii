# sys_analysis/matrix.py

class Matrix:

    def __init__(self, row, col):
        self._matrix = []
        self._row = int(row)
        self._col = int(col)

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        self._col = int(value)

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = int(value)

    def get_matrix(self):
        return self._matrix

    def add_row(self, row):
        self._check_type(row)
        if not self._is_row_in_limitation(row):
            raise Exception("Not in limitation!")
        self._matrix.append(list(row))

    def clone(self, matrix):
        self._check_type(matrix)
        for row in matrix:
            self.add_row(row)

    def get_transposition(self):
        result = []

        for j in range(0, self._col):
            row = []
            for i in range(0, self._row):
                row.append(self._matrix[i][j])
            result.append(row)

        return self._create_new_matrix(result, self._col, self._row)

    def print_matrix(self):
        print(self._to_string())

    def is_same_limitations(self, matrix):
        if self._col == matrix.col and self._row == matrix.row:
            return True
        return False

    def __len__(self):
        return len(self._matrix)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return "Matrix ({}, {})".format(self._row, self._col)

    def __add__(self, other):
        return self._adding(other)

    def __sub__(self, other):
        return self._adding(other, coefficient=-1)

    def __mul__(self, other):
        if self._col != other.row:
            raise Exception("The limitations of the matrices do not allow multiplication!")

        other = other.get_matrix()

        len_r = len(self._matrix)
        len_c = len(other[0])

        result = []
        for i in range(0, len_r):
            row = []
            for j in range(0, len_c):
                sum = 0
                for k in range(0, self._col):
                    sum += self._matrix[i][k] * other[k][j]
                row.append(sum)
            result.append(row)
        return self._create_new_matrix(result, len_r, len_c)

    def _create_new_matrix(self, new_list, row=None, col=None):
        if not row and not col:
            new_matrix = Matrix(self._row, self._col)
        else:
            new_matrix = Matrix(int(row), int(col))
        new_matrix.clone(new_list)
        return new_matrix

    def _adding(self, matrix, coefficient=1):
        if not self.is_same_limitations(matrix):
            raise Exception("Matrixes must have the same limitations!")

        matrix = matrix.get_matrix()
        result = []
        for i in range(0, len(self._matrix)):
            row = []
            for j in range(0, len(self._matrix[i])):
                row.append(
                    self._matrix[i][j] + matrix[i][j] * coefficient
                )
            result.append(row)
        # result matrix
        return self._create_new_matrix(result)

    def _check_type(self, arr):
        if not isinstance(arr, (list, set)):
            raise TypeError("Must be list or set!")

    def _is_row_in_limitation(self, row):
        return len(row) == self._col and len(self._matrix) < self._row

    def _to_string(self):
        matrix_string = ""
        for row in self._matrix:
            for i in row:
                matrix_string += "{}\t".format(i)
            matrix_string += "\n"
        return matrix_string[:-1]
