#!/bin/python

from sys import argv as argument

# wraps all coordinates back into the unit cell and truncates coordinates to the millionth's place.
def adjust(x):
    if x in [-0.0, -1.0, 2.0, -2.0]: x = 0.0
    if x < 0.0: x = 1 + x
    if x > 1.0: x = x - 1
    x = round(1000000.0 * x) / 1000000.0
    return x

def translate(x, y, z, x_, y_, z_): return eval("adjust(" + x_ + ")"), \
        eval("adjust(" + y_ + ")"), eval("adjust(" + z_ + ")")

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

def find_min(L):
    mn = L[0]
    for i in L:
        if i < mn: mn = i
    return mn

def find_max(L):
    mn = L[0]
    for i in L:
        if i > mn: mn = i
    return mn

def fix_hex(h):
    hl = h.split('x')
    bh = hl[1]
    if len(bh) == 1: bh = '0' + bh
    bh = '0x' + bh + bh + bh
    return bh

# main
f = open(argument[1], 'r')
name = argument[1].split('.')[0]
atomFlag = False
atoms = {}
for line in f:
    l = line.split()
    if len(l) > 0:
        if l[0] == 'TITL': group = l[-1]
        if l[0] == 'CELL': a, b, c = l[2], l[3], l[4]
        if l[0] == 'SFAC': sfac = l
        if l[0] == 'MOLE': atomFlag = not atomFlag
        if atomFlag:
            try:
                try: dummy = float(l[0])
                except ValueError:
                    if atomFlag:
                        atoms[l[0]] = [l[1], l[2], l[3], l[4], l[6]]
            except IndexError: continue
f.close()

space_groups = {"Fm-3m": [["x", "y", "z"], ["-x", "-y", "z"], ["-x", "y", "-z"], ["z", "x", "y"], ["y", "x", "-z"], ["-x", "-y", "-z"], ["x", "y + 0.5", "z + 0.5"], ["x + 0.5", "y", "z + 0.5"]]}
r = {'C': '0.77', 'SI': '1.17', 'FE': '1.24', 'PR': '1.86'}
clr = {'C': '0xffffff', 'SI': '0x3333ff', 'FE': '0xff0000', 'PR': '0xffff00'}

print('<html>\n\
<head>\n\
    <title>' + name + '</title>\n\
    <style>\n\
        body {margin: 0;}\n\
        canvas {width: 100%; height: 100%}</style></head>\n\
<body>\n\
    <script src="js/three.min.js"></script>\n\
    <script>\n\
        var scene, camera, renderer;\n\
        var geometry, material, mesh;')

atomList, U = [], []
for atom in atoms:
    atomList += [atom]
    U += [float(atoms[atom][4])]

mn = find_min(U)
mx = find_max(U)

U = [fix_hex(hex(int(255 * (i - mn) / (mx - mn)))) for i in U]

for atom in atoms:
    # get position of current atom in list 'a'
    n = atomList.index(atom)
    atoms[atom][-1] = U[n]

for atom in atoms:
    atm = sfac[int(atoms[atom][0])]
    q = [(float(atoms[atom][1]), float(atoms[atom][2]), float(atoms[atom][3]))]
    print('        var ' + atom + ' = [\'' + atom + '\', \'' + atm + '\', ' + r[atm] + ', ' + clr[atm] + ', ' + atoms[atom][-1] + ', ' + str(generate(q, space_groups[group])) + '];')

print('        \n\
        init();\n\
        animate();\n\
        \n\
        function init() {\n\
            scene = new THREE.Scene();\n\
            camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 10000 );\n\
            camera.position.z = 25;\n\
            \n\
            var a = ' + str(a) + ';\n\
            var b = ' + str(b) + ';\n\
            var c = ' + str(c) + ';\n\
            unitCellFrm = new THREE.BoxGeometry( a, b, c );\n\
            unitCellStf = new THREE.MeshBasicMaterial( { color: 0xff0000, wireframe: true } );\n\
            unitCell = new THREE.Mesh( unitCellFrm, unitCellStf );\n\
            scene.add(unitCell);\n\
            \n\
            var atomScale = 0.5;\n\
            \n\
')
for atom in atoms:
    print('            var name = ' + atom + '[0];')
    print('            var element = ' + atom + '[1];')
    print('            var radius = ' + atom + '[2];')
    print('            var colorCode = ' + atom + '[3];')
    print('            var thermalCode = ' + atom + '[4];')
    print('            var positions = ' + atom + '[5];\n\
            \n\
            var geometry = new THREE.SphereGeometry( radius * atomScale, 8, 8 );\n\
            var group = new THREE.Group();\n\
            group.name = name;\n\
            group.element = element;\n\
            \n\
            for ( var i = 0; i < positions.length; i ++ ) {\n\
            	var object = new THREE.Mesh( geometry, new THREE.MeshBasicMaterial( { color: colorCode, wireframe: true } ) );\n\
            	object.position.x = a * positions[i][0] - 0.5 * a;\n\
            	object.position.y = b * positions[i][1] - 0.5 * b;\n\
            	object.position.z = c * positions[i][2] - 0.5 * c;\n\
            	group.add( object );\n\
            }\n\
            \n\
            scene.add ( group );\n\
')

print('                \n\
                renderer = new THREE.WebGLRenderer();\n\
                renderer.setSize( window.innerWidth, window.innerHeight );\n\
                document.body.appendChild( renderer.domElement );\n\
            }\n\
            \n\
            function animate() {\n\
                requestAnimationFrame( animate );\n\
                for ( var i = 0, l = scene.children.length; i < l; i ++ ) {\n\
                    var object = scene.children[ i ];\n\
                    object.rotation.x += 0.001;\n\
                    object.rotation.y += 0.002;\n\
            }\n\
            \n\
            renderer.render( scene, camera );\n\
            \n\
        }</script></body></html>')
