# -*- coding: cp936 -*-
import lib601.le as le
import lib601.circ as circ

ce = le.EquationSet()
ce.addEquation(le.Equation([10.0,-12.0,1.0,1.0],['e0','e1','e2','e3'],0.0))
ce.addEquation(le.Equation([0,1.0,-3.0,1.0],['e0','e1','e2','e3'],0.0))
ce.addEquation(le.Equation([1.0],['e3'],10.0))
ce.addEquation(le.Equation([1.0],['e0'],0.0))

ce.addEquation(le.Equation([-1.0,1.0,1.0],['i1','i2','i4'],0.0))
ce.addEquation(le.Equation([-1.0,1.0,-1.0],['i2','i3','i6'],0.0))
ce.addEquation(le.Equation([-1.0,1.0,1.0],['i4','i5','i6'],0.0))
ce.addEquation(le.Equation([10.0,-1.0],['i4','e1'],0.0))
ce.addEquation(le.Equation([100,-1.0],['i5','e2'],0.0))
ce.addEquation(le.Equation([1.0,-1.0,-100.0],['e3','e2','i3'],0.0))

print (ce.solve())

ce1 = circ.Circuit([
    circ.VSrc(10, 'e3', 'e0'),
    circ.Resistor(100, 'e3', 'e1'),
    circ.Resistor(10, 'e1', 'e0'),
    circ.Resistor(100, 'e3', 'e2'),
    circ.Resistor(100, 'e1', 'e2'),
    circ.Resistor(100, 'e2', 'e0'),
    ])
print ce1.solve('e0')
