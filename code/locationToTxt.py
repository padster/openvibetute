import numpy as np
import scipy.io as sio
import csv

SUBJECT = 'aak'
IN_FILE = 'data/musicbci_VP%s.mat' % SUBJECT
OUT_FILE = 'dataCSV/%s_locations.txt' % SUBJECT

print "Loading matlab file %s..." % IN_FILE
data = sio.loadmat(IN_FILE)

channelNames = [str(c[0]) for c in data['data'][0]['clab'][0][0]]
positions = data['mnt'][0]['pos_3d'][0] # (3, 64)

channelList = " ".join('"' + name + '"' for name in channelNames)

"""
[
	[ "O1" "O2" "T5" "P7" "P3 ... "FC6" ]
	[ "x" "y" "z" ]
]
"""
header = '[\n\t[ %s ]\n\t[ "x" "y" "z" ]\n]\n' % channelList

print "Writing to %s..." % OUT_FILE
with open(OUT_FILE, 'w') as txtFile:
    txtFile.write(header)
    for i in range(len(channelNames)):
        if np.isnan(positions[:, i]).any():
            continue
        """
[
	[-0.309017 -0.951057 4.48966e-011 ]
]
        """
        row = "[\n\t[ %0.6f %0.6f %0.6f ]\n]\n" % tuple(positions[:, i])
        txtFile.write(row)

print "Done!"
