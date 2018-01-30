from entites import Box,Vec3,TupleAnglesRotation,BoxDimensions
from math import radians

pave1 = Box(Vec3(56.0,5.0,5.0), TupleAnglesRotation(0,47,0),BoxDimensions(10,10,10))

pave2 = Box(Vec3(55.0,5.0,5.0),TupleAnglesRotation(90.0,90.0,90.0),BoxDimensions(5,5,5))

if(pave1.intersectsPave(pave2)):
    print("deu ruim, achou intersecao")
else:
    print("deu bom, nao achou intersecao")
