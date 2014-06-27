__author__ = 'wallsr'

import datetime
import sys

time_file = sys.argv[1]
start_block = sys.argv[2]
end_block = sys.argv[3]

with open(time_file, 'r') as infile:
    lines = infile.readlines()

lines_parsed = []

for line in lines:
    block, lowertime, uppertime = line.split('\t')

    if block in [start_block, end_block]:
        lowertime = datetime.datetime.strptime(lowertime, '%a %b %d %H:%M:%S %Y')
        lines_parsed.append((block, lowertime))

if len(lines_parsed) != 2:
    print 'Failed to grab two lines'

blockdiff = int(lines_parsed[1][0]) - int(lines_parsed[0][0])
timediff = (lines_parsed[1][1] - lines_parsed[0][1]).total_seconds()

print '%d blocks in %d seconds: %f b/s' % (blockdiff, timediff, float(blockdiff)/timediff)
