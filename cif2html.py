#!/bin/python
from sys import argv as argument
import re

def collapse_whitespace(text): return re.sub(r'\s+', ' ', text).strip()

text = []

file = open(argument[1], 'r')
for line in file: text.append(collapse_whitespace(line.rstrip()))
file.close()

# make a list of indices where loops begin
indices = [i + 1 for i, x in enumerate(text) if x == 'loop_'] + [len(text) + 1]
dictionary = {}

for i in range(len(indices) - 1):
    dictionary[text[indices[i]]] = []
    for j in range(indices[i] + 1, indices[i + 1] - 1):
        dictionary[text[indices[i]]].append(text[j])

for entry in dictionary:
    if entry in ['_publ_author_name', '_symmetry_equiv_pos_as_xyz']:
        for item in dictionary[entry]:
            if item.split('_')[0] == '':
                index = dictionary[entry].index(item)
                dictionary[entry] = dictionary[entry][:index]
                break
    elif entry in ['_atom_site_aniso_label', '_atom_site_label', '_atom_type_symbol']:
        dictionary[entry] = [entry] + dictionary[entry]
        rewrite = []
        counter = 0
        for item in dictionary[entry]:
            if '' in item.split('_'): counter += 1
        rewrite += [dictionary[entry][:counter]]
        for item in dictionary[entry][counter:]: rewrite += [item.split(' ')]
        dictionary[entry] = rewrite

for line in text:
    if line.split(' ')[0] == '_space_group_IT_number': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_angle_alpha': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_angle_beta': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_angle_gamma': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_formula_units_Z': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_length_a': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_length_b': dictionary[line.split(' ')[0]] = line.split(' ')[1]
    if line.split(' ')[0] == '_cell_length_c': dictionary[line.split(' ')[0]] = line.split(' ')[1]

print("var uca = " + dictionary["_cell_length_a"].split('(')[0] + ";")
print("var ucb = " + dictionary["_cell_length_b"].split('(')[0] + ";")
print("var ucc = " + dictionary["_cell_length_c"].split('(')[0] + ";")
print()

data = []

#for entry in dictionary:
#    print(entry)
#    print(dictionary[entry])
#    print()

indx = dictionary['_atom_site_label'][0].index('_atom_site_fract_x')
indy = dictionary['_atom_site_label'][0].index('_atom_site_fract_x') + 1
indz = dictionary['_atom_site_label'][0].index('_atom_site_fract_x') + 2

radNClr = {  "H":[0.37,"0xFFFFFF"],
            "He":[0.32,"0xD9FFFF"],
            "Li":[1.34,"0xCD7EFF"],
            "Be":[0.90,"0xC5FF00"],
             "B":[0.82,"0xFFB7B7"],
             "C":[0.77,"0x393939"],
             "N":[0.75,"0x2F2FD7"],
             "O":[0.73,"0xF00000"],
             "F":[0.71,"0xD4F03F"],
            "Ne":[0.69,"0xAFE3F4"],
            "Na":[1.54,"0xAA5EF2"],
            "Mg":[1.30,"0x89FF00"],
            "Al":[1.18,"0xD2A5A5"],
            "Si":[1.11,"0x819A9A"],
             "P":[1.06,"0xFF8000"],
             "S":[1.02,"0xFFFF00"],
            "Cl":[0.99,"0x20F020"],
            "Ar":[0.97,"0x81D1E4"],
             "K":[1.96,"0x8F41D3"],
            "Ca":[1.74,"0x3DFF00"],
            "Sc":[1.44,"0xE6E6E4"],
            "Ti":[1.36,"0xC0C3C6"],
             "V":[1.25,"0xA7A5AC"],
            "Cr":[1.27,"0x8B99C6"],
            "Mn":[1.39,"0x9C7BC6"],
            "Fe":[1.25,"0x817BC6"],
            "Co":[1.26,"0x707BC3"],
            "Ni":[1.21,"0x5D7BC3"],
            "Cu":[1.38,"0xFF7B62"],
            "Zn":[1.31,"0x7C81AF"],
            "Ga":[1.26,"0xC39291"],
            "Ge":[1.22,"0x669292"],
            "As":[1.19,"0xBE81E3"],
            "Se":[1.16,"0xFFA200"],
            "Br":[1.14,"0xA52A2A"],
            "Kr":[1.10,"0x5DBAD1"],
            "Rb":[2.11,"0x712EB2"],
            "Sr":[1.92,"0x00FF00"],
             "Y":[1.62,"0x96FDFF"],
            "Zr":[1.48,"0x96E1E1"],
            "Nb":[1.37,"0x74C3CB"],
            "Mo":[1.45,"0x55B5B7"],
            "Tc":[1.56,"0x3C9FA8"],
            "Ru":[1.26,"0x238E97"],
            "Rh":[1.35,"0x0B7C8C"],
            "Pd":[1.31,"0x006986"],
            "Ag":[1.53,"0x99C6FF"],
            "Cd":[1.48,"0xFFD891"],
            "In":[1.44,"0xA77673"],
            "Sn":[1.41,"0x668181"],
            "Sb":[1.38,"0x9F65B5"],
            "Te":[1.35,"0xD57B00"],
             "I":[1.33,"0x930093"],
            "Xe":[1.30,"0x429FB0"],
            "Cs":[2.25,"0x57198F"],
            "Ba":[1.98,"0x00CB00"],
            "La":[1.85,"0x70DEFF"],
            "Ce":[1.85,"0xFFFFC8"],
            "Pr":[1.85,"0xD9FFC8"],
            "Nd":[1.85,"0xC6FFC8"],
            "Pm":[1.85,"0xA4FFC8"],
            "Sm":[1.85,"0x92FFC8"],
            "Eu":[1.85,"0x63FFC8"],
            "Gd":[1.80,"0x47FFC8"],
            "Tb":[1.75,"0x32FFC8"],
            "Dy":[1.75,"0x1FFFB7"],
            "Ho":[1.75,"0x00FF9D"],
            "Er":[1.75,"0x00E776"],
            "Tm":[1.75,"0x00D353"],
            "Yb":[1.75,"0x00C039"],
            "Lu":[1.75,"0x00AD23"],
            "Hf":[1.50,"0x4DC2FF"],
            "Ta":[1.38,"0x4DA7FF"],
             "W":[1.46,"0x2794D6"],
            "Re":[1.59,"0x277EAC"],
            "Os":[1.28,"0x276897"],
            "Ir":[1.37,"0x185587"],
            "Pt":[1.28,"0x185B91"],
            "Au":[1.44,"0x185B91"],
            "Hg":[1.49,"0xB5B5C3"],
            "Tl":[1.48,"0xA7554D"],
            "Pb":[1.47,"0x575A60"],
            "Bi":[1.46,"0x9F4FB5"],
            "Po":[1.75,"0xAC5D00"],
            "At":[1.50,"0x764F45"],
            "Rn":[1.45,"0x428497"],
            "Fr":[2.30,"0x420066"],
            "Ra":[2.15,"0x007C00"],
            "Ac":[1.95,"0x71AAFC"],
            "Th":[1.80,"0x00BBFF"],
            "Pa":[1.80,"0x00A1FF"],
             "U":[1.75,"0x0092FF"],
            "Np":[1.75,"0x0081F2"],
            "Pu":[1.75,"0x006BF2"],
            "Am":[1.75,"0x555BF2"],
            "Cm":[1.75,"0x785BE3"],
            "Bk":[1.70,"0x894FE3"],
            "Cf":[1.70,"0xA137D5"],
            "Es":[1.70,"0xB31FD5"],
            "Fm":[1.70,"0xB31FBA"],
            "Md":[1.70,"0xB30DA7"],
            "No":[1.70,"0xBD0D87"],
            "Lr":[1.70,"0xC90066"]}

spaceGroups = { "225":  [["x", "y", "z"], ["-x", "-y", "z"], ["-x", "y", "-z"], ["z", "x", "y"],   ["y", "x", "-z"], ["-x", "-y", "-z"], ["x", "y + 0.5", "z + 0.5"], ["x + 0.5", "y", "z + 0.5"], ["x + 1.0", "y", "z"], ["x", "y + 1.0", "z"], ["x", "y", "z + 1.0"]],

                "123": [["x", "y", "z"], ["-x", "-y", "z"], ["-y", "x",  "z"], ["-x", "y", "-z"], ["-x", "-y", "-z"], ["x + 1.0", "y", "z"], ["x", "y + 1.0", "z"], ["x", "y", "z + 1.0"]],
                
                "221":  [["x", "y", "z"], ["-x", "-y", "z"], ["-x", "y", "-z"], ["z",  "x",  "y"], [ "y",  "x", "-z"], ["-x", "-y", "-z"], ["x + 1.0", "y", "z"], ["x", "y + 1.0", "z"], ["x", "y", "z + 1.0"]],

                "222": [["x", "y", "z"], ["-x+.5","-y+.5","z"], ["-x+.5","y","-z+.5"], ["z",  "x",  "y"], ["y", "x", "-z+.5"], ["-x", "-y", "-z"], ["x + 1.0", "y", "z"], ["x", "y + 1.0", "z"], ["x", "y", "z + 1.0"]]

                }

def adjust(x):
    while x < 0.0: x += 1
    while x > 1.0: x -= 1
    x = round(1000000.0 * x) / 1000000.0
    return x

def translate(x, y, z, x_, y_, z_): return eval("adjust(" + x_ + ")"), eval("adjust(" + y_ + ")"), eval("adjust(" + z_ + ")")

def generate(q, g):

    q1, q2, q3 = [], q, []

    while q1 != q2:
        for i in q2:
            if i not in q1:
                x, y, z = i[0], i[1], i[2]
                for j in g:
                    q = list(translate(x, y, z, j[0], j[1], j[2]))
                    if q not in q2 and q not in q3: q3.append(q)

        q1 = q2[:]
        q2 += q3
        q3 = []

        q1.sort(key=lambda t: t[0])
        q2.sort(key=lambda t: t[0])

    q1[-1] = list(q1[-1])
    return q1
    
spaceGroupNumber = dictionary['_space_group_IT_number']

for atom in dictionary['_atom_site_label']:
    if atom[0] == '_atom_site_label': continue
    else:
        atomName = atom[0]
        element = ''.join([i for i in atomName if not i.isdigit()]).capitalize()
        genPos = [[float(atom[indx].split('(')[0]), float(atom[indy].split('(')[0]), float(atom[indz].split('(')[0])]]
        
        radius = radNClr[element]
        color = radius[1]
        radius = radius[0]
        specialPos = [generate(genPos, spaceGroups[spaceGroupNumber])]
        
        data += [[atomName, radius, color] + [q for q in specialPos]]

print('var data = ' + str(data) + ';')
