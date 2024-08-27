import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypolydb import polydb


def test_find_one():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    filter = {'N_VERTICES': 10}
    p = coll.find_one(skip=3, filter=filter)
    assert p['_id'] == 'F.3D.0008'


def test_find():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    filter = {'N_VERTICES': 10}
    c = coll.find(skip=3, limit=1, filter=filter)
    p = c.next()
    assert p['_id'] == 'F.3D.0008'


def test_count():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    filter = {'N_VERTICES': 10}
    c = coll.count(filter=filter)
    assert c == 11


def test_distinct():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    filter = {'N_VERTICES': 10, 'DIM': 5}
    d = coll.distinct("N_LATTICE_POINTS", filter=filter)
    assert d == [378, 406, 491, 636, 846]


def test_answer():
    test_find()
    test_find_one()
    test_count()
    test_distinct()
