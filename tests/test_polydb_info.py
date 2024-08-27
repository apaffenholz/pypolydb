import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pypolydb import polydb


def test_section_info():
    pdb = polydb.polyDB()
    info = pdb.section_info('Polytopes.Lattice')
    assert info['maintainer']['name'] == "Andreas Paffenholz"


def test_collection_info():
    pdb = polydb.polyDB()
    coll = pdb.get_collection('Polytopes.Lattice.SmoothReflexive')
    info = coll.info()
    assert info['maintainer'][0]['name'] == "Andreas Paffenholz"


def test_answer():
    test_section_info()
    test_collection_info()
