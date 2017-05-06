import scipy.io as sio
import csv

SUBJECT = 'aak'
IN_FILE = 'data/musicbci_VP%s.mat' % SUBJECT
OUT_FILE = 'dataCSV/%s_events.csv' % SUBJECT

print "Loading matlab file %s..." % IN_FILE
data = sio.loadmat(IN_FILE)

trials = data['data'][0]['trial'][0]
values = data['data'][0]['y'][0]
assert trials.shape == values.shape

eventCount = trials.shape[1]
sampleRate = int(round(data['data'][0]['fs'][0][0][0]))
print "# Events: %d" % eventCount


print "Writing to %s..." % OUT_FILE
with open(OUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time (s)', 'Identifier', 'Duration'])
    # First row has extra rate:
    for i in range(eventCount):
        msOffset = int(round(trials[0, i])) * 1000 / sampleRate
        # eID = values[0, i]
        eID = 33024 + values[0, i] # HACK: http://openvibe.inria.fr/stimulation-codes/
        writer.writerow([msOffset / 1000.0, eID, 1])

print "Done!"
