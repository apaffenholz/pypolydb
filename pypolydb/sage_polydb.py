import sage.all as sage

def flatten(list2d):
    return [x for row in list2d for x in row]

def split_complex_types(s : str):
    paren_count = {}
    paren_stack = []

    for i, c in enumerate(s):
        if c == '<':
            paren_stack.append(i)
        elif c == '>':
            paren_count[paren_stack.pop()] = i
        if len(paren_stack) == 0:
            return s[0,paren_count[0]], s[paren_count[0]+2:]

def split_type(t:str = None):
    try:
        p = t.index("<")
        c = t.index(",")
        if c < p :
            f,s = t.split(",",1)
            return "polymake::common::" + f, "polymake::common::" + s
        else:
            f,s = split_complex_types(t)
            return "polymake::common::" + f, "polymake::common::" + s
    except ValueError:
        f,s = t.split(",")
        return "polymake::common::" + f, "polymake::common::" + s

def convert(a, typename : str):
    if typename.startswith('polymake::common::Matrix'):
        ring = typename.removeprefix('polymake::common::Matrix<').split(',')[0]
        if ring == 'Rational':
            return sage.matrix(sage.QQ, len(a) , len(a[0]), flatten(a))
        elif ring == 'Integer' or ring == 'Int':
            return sage.matrix(sage.ZZ, len(a) , len(a[0]), flatten(a))
        else:
            print("unknown field in matrix: ", typename)
            return None
    elif typename.startswith('polymake::common::Vector'):
        ring = typename.removeprefix('polymake::common::Vector<')[:-1]
        if ring == 'Rational':
            return sage.vector(sage.QQ,a)
        elif ring == 'Integer' or ring == 'Int':
            return sage.vector(sage.ZZ, a)
        else:
            print("unknown field in vector: ", type)
            return None
    elif typename.startswith('polymake::common::Integer'):
        return sage.ZZ(a)
    elif typename.startswith('polymake::common::Rational'):
        return sage.QQ(a)
    elif typename.startswith('polymake::common::Int'):
        return int(a)
    elif typename.startswith('polymake::common::Bool'):
        return bool(a)
    elif typename.startswith('polymake::common::String'):
        return str(a)
    elif typename.startswith('polymake::common::IncidenceMatrix'):
        i = sage.IncidenceStructure(a[-1]['cols'], a[:len(a)-1])
        return i
    elif typename.startswith('polymake::common::Array'):
        elementtype = "polymake::common::" + typename.removeprefix('polymake::common::Array<')[:-1]
        l = list()
        for e in a:
            l.append(convert(e,elementtype))
    elif typename.startswith('polymake::common::Set'):
        elementtype = "polymake::common::" + typename.removeprefix('polymake::common::Set<')[:-1]
        l = set()
        for e in a:
            ec = convert(e,elementtype)
            print(type(ec))
            if type(ec) == list:
                l.add(tuple(ec))
            else:
                l.add(ec)
        return l
    elif typename.startswith('polymake::common::Map'):
        elementtype_a, elementtype_b = split_type(typename.removeprefix('polymake::common::Map<')[:-1])
        l = dict()
        for i,j in a:
            l[convert(i,elementtype_a)] = convert(j,elementtype_b)
        return l
    elif typename.startswith('polymake::common::Pair'):
        elementtype_a, elementtype_b = split_type(typename.removeprefix('polymake::common::Pair<')[:-1])
        l = list()
        l.append(convert(a[0],elementtype_a))
        l.append(convert(a[1],elementtype_b))
        return l
    else:
        print("unknown type: ", typename)
        return None