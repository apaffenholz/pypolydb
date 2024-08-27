import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypolydb import polydb


def connect():
    pdb = polydb.polyDB()
    collection = pdb.get_collection("Polytopes.Lattice.SmoothReflexive")
    poly = collection.find_one()
    assert poly['SMOOTH']


def test_get_collection():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    poly = coll.find_one()
    assert poly['SMOOTH']


def test_answer():
    connect()
    test_get_collection()
