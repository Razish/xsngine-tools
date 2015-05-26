#!/usr/bin/python

import re
import sys

s = ''

scale = float( sys.argv[2] )

with open( sys.argv[1] + '.xmf', 'r') as f:
	for line in f:
		line = line.strip()
		if line and line.startswith( 'v '):
			matched = re.findall( r"[-+]?\d*\.\d+|\d+", line )
			s += 'v ' + str( float( matched[0] ) * scale ) + ' ' + str( float( matched[1] ) * scale ) + ' ' + str( float( matched[2] ) * scale ) + '\n'
		else:
			s += line + '\n'

f = open( sys.argv[1] + '.xmf', 'w+' )
f.write( s )
f.close()
