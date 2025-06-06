import sage.all as sage
from pypolydb.polydb import polyDB as basePolyDB


class polyDB(basePolyDB):

    def _flatten(self, list2d):
        return [x for row in list2d for x in row]

    def split_complex_types(self, s: str):
        paren_count = {}
        paren_stack = []

        for i, c in enumerate(s):
            if c == '<':
                paren_stack.append(i)
            elif c == '>':
                paren_count[paren_stack.pop()] = i
            if len(paren_stack) == 0:
                return s[0, paren_count[0]], s[paren_count[0] + 2:]

    def _split_type(self, t: str = None):
        try:
            p = t.index("<")
            c = t.index(",")
            if c < p:
                f, s = t.split(",", 1)
                return "polymake::common::" + f, "polymake::common::" + s
            f, s = self.split_complex_types(t)
            return "polymake::common::" + f, "polymake::common::" + s
        except ValueError:
            f, s = t.split(",")
            return "polymake::common::" + f, "polymake::common::" + s

    def convert_affine(self, a, typename: str):
        """
            Converts a polymake matrix type into a standard sage type
                while removing the first column
                (thus converting the homogeneous rep of polymake into an affine rep)

            The typename must be given and cannot be infered from the data
            It can be obtained with get_type(<property name>) from the json schema of the collection
        """
        M = self.convert(a, typename)
        return M[range(M.nrows()), range(1, M.ncols())]

    def convert(self, a, typename: str):
        """
            Converts a polymake type into a standard sage type

            The typename must be given and cannot be infered from the data
            It can be obtained with get_type(<property name>) from the json schema of the collection
        """
        if typename.startswith('polymake::common::Matrix'):
            ring = typename.removeprefix('polymake::common::Matrix<').split(',')[0]
            if ring == 'Rational':
                return sage.matrix(sage.QQ, len(a), len(a[0]), self._flatten(a))
            if ring == 'Integer' or ring == 'Int':
                return sage.matrix(sage.ZZ, len(a), len(a[0]), self._flatten(a))
            print("unknown field in matrix: ", typename)
            return None

        if typename.startswith('polymake::common::Vector'):
            ring = typename.removeprefix('polymake::common::Vector<')[:-1]
            if ring == 'Rational':
                return sage.vector(sage.QQ, a)
            if ring == 'Integer' or ring == 'Int':
                return sage.vector(sage.ZZ, a)
            print("unknown field in vector: ", type)
            return None

        if typename.startswith('polymake::common::Integer'):
            return sage.ZZ(a)
        if typename.startswith('polymake::common::Rational'):
            return sage.QQ(a)
        if typename.startswith('polymake::common::Int'):
            return int(a)
        if typename.startswith('polymake::common::Bool'):
            return bool(a)
        if typename.startswith('polymake::common::String'):
            return str(a)
        if typename.startswith('polymake::common::IncidenceMatrix'):
            return sage.IncidenceStructure(a[-1]['cols'], a[:len(a) - 1])
        if typename.startswith('polymake::common::Array'):
            elementtype = "polymake::common::" + typename.removeprefix('polymake::common::Array<')[:-1]
            return [self.collections_listconvert(e, elementtype)
                    for e in a]
        if typename.startswith('polymake::common::Set'):
            elementtype = "polymake::common::" + typename.removeprefix('polymake::common::Set<')[:-1]
            l = set()
            for e in a:
                ec = self.convert(e, elementtype)
                print(type(ec))
                if isinstance(ec, list):
                    l.add(tuple(ec))
                else:
                    l.add(ec)
            return l
        if typename.startswith('polymake::common::Map'):
            elementtype_a, elementtype_b = self._split_type(typename.removeprefix('polymake::common::Map<')[:-1])
            return {self.convert(i, elementtype_a):
                    self.convert(j, elementtype_b)
                    for i, j in a}
        if typename.startswith('polymake::common::Pair'):
            elementtype_a, elementtype_b = self._split_type(typename.removeprefix('polymake::common::Pair<')[:-1])
            return [self.convert(a[0], elementtype_a),
                    self.convert(a[1], elementtype_b)]

        print("unknown type: ", typename)
        return None
