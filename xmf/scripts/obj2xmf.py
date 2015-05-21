#!/usr/bin/python

import re
import sys

if len( sys.argv ) < 2 or len( sys.argv ) > 3:
	print( '''usage: obj2xmf.py <obj_input_file> [xmf_output_file]
	note: do not specify extensions
	note: xmf_output_file is optional and will default to the same name as the input file''' )
	exit()

vertices = []
uvs = []
faces = []

inputFile = sys.argv[1] + '.obj'
outputFile = (sys.argv[1] + '.xmf') if (len( sys.argv ) != 3) else (sys.argv[2] + '.xmf')

print( 'reading ' + inputFile )
with open( inputFile, 'r') as f:
	for line in f:
		line = line.strip()
		if line:
			if line.startswith( 'v '):
				matched = re.findall( r"[-+]?\d*\.\d+|\d+", line )
				vertices.append( [ matched[0], matched[1], matched[2] ] )
			elif line.startswith( 'vt' ):
				matched = re.findall( r"[-+]?\d*\.\d+|\d+", line )
				uvs.append( [ matched[0], matched[1] ] )
			elif line.startswith( 'f' ):
				group = line.split( ' ' )
				group.pop( 0 )
				face = []
				for g in group:
					indices = g.split( '/' )
					face.append( int( indices[0] ) )
					#FIXME: consider UVs per face
					# ignore normals, we calculate them ourselves
				faces.append( face )
		else:
			s += line + '\n'

#HACK: fuck up the UVs until we properly read them
if len( uvs ) == 0:
	for v in vertices:
		uvs.append( [ '0.0', '1.0' ] )

# show diagnostics
print( str( len( vertices ) ) + ' vertices, ' + str( len( faces ) ) + ' faces, ' + str( len( uvs ) ) + ' UVs' )

# calculate vertex normals
#print( 'calculating normals using Newell\'s method' )
#meshVertices = []
#for v in vertices:
#	meshVertices.append( [float( p ) for p in v] )
#meshIndices = []
#for f in faces:
#	for i in f:
#		meshIndices.append( i )
#i = 0
#while i < len( meshIndices ):
#	print( str( i ) + '\n' )
#	p1 = meshVertices[meshIndices[i + 0]]
#	p2 = meshVertices[meshIndices[i + 1]]
#	p3 = meshVertices[meshIndices[i + 2]]
#	i = i + 3

# write out the file
s = '''version 3
o "textures/models/box.png"
'''

for v in vertices:
	s += 'v ' + ' '.join( v ) + '\n'
for uv in uvs:
	s += 'uv ' + ' '.join( uv ) + '\n'
for f in faces:
	s += 'f ' + str( f[0] - 1 ) + '/' + str( f[1] - 1 ) + '/' + str( f[2] - 1 ) + '\n'

# write the XMF file
print( 'writing ' + outputFile + ' (' + '{0:.1f}'.format( len( s ) / 1024.0 ) + 'kB) - version 3' )
f = open( outputFile, 'w' )
f.write( s )
f.close()
