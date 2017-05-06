import scipy.io as sio
import csv

SUBJECT = 'aak'
IN_FILE = 'data/musicbci_VP%s.mat' % SUBJECT
OUT_FILE = 'dataCSV/%s_signal.csv' % SUBJECT

print "Loading matlab file %s..." % IN_FILE
data = sio.loadmat(IN_FILE)
readings = data['data'][0]['X'][0]

# First line: Row count, then channel names, then sample rate
channelNames = [str(c[0]) for c in data['data'][0]['clab'][0][0]]
sampleRate = data['data'][0]['fs'][0][0][0]

print "# Readings: %d" % readings.shape[0]
print "# Channels: %d" % len(channelNames)
print "Sample rate: %d hz" % sampleRate

# sampleRate samples/sec = 1000 / sampleRate ms/sample
secPerSample = 1.0 / sampleRate

print "Writing to %s..." % OUT_FILE
with open(OUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time (s)'] + channelNames + ['Sampling Rate'])
    # First row has extra rate:
    writer.writerow([0.0] + readings[0].tolist() + [sampleRate])
    for r in range(1, readings.shape[0]):
        writer.writerow([r * secPerSample] + readings[r].tolist())

print "Done!"
