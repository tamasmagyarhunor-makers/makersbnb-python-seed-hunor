from lib.space import *

def test_space_constructs():
    space = Space(1,'The Manor','A Manor house',100,1)

    assert space.id == 1
    assert space.name == 'The Manor'
    assert space.description == 'A Manor house'
    assert space.price == 100
    assert space.host_id == 1

def test_space_formatting():
    space = Space(1,'The Manor','A Manor house',100,1)

    assert str(space) == 'Space(1, The Manor, A Manor house, £100/night, 1)'

def test_spaces_are_equal():
    space1 = Space(1,'The Manor','A Manor house',100,1)
    space2 = Space(1,'The Manor','A Manor house',100,1)
    space3 = Space(2,'The Manor','Manor house',120,1)

    assert space1 == space2
    assert space1 != space3