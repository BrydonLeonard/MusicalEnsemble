import pycurl
import argparse
import os

parser = argparse.ArgumentParser(description='Download all midis from the urls in a given file')
parser.add_argument('urlFile', help='The file to read')

args = parser.parse_args()

lines = []

with open(args.urlFile, 'r') as f:
    lines = f.read().split('\n')

del lines[0]

urls = dict()

for line in lines:
    if line:
        this_midi = line.split(',')
        if this_midi[1] in urls:
            urls[this_midi[1]].append(this_midi[2])
        else:
            urls[this_midi[1]] = [this_midi[2]]

for genre in urls:
    print('Starting genre: ' + genre)
    for i in range(0, len(urls[genre])):
        print(str(i) + '/' + str(len(urls[genre])))
        if not os.path.exists('../midi/genres/' + genre + '/'):
            os.makedirs('../midi/genres/' + genre)
        with open('../midi/genres/' + genre + '/' + genre + '-' + str(i) + '.mid', 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, urls[genre][i])
            c.setopt(c.WRITEDATA, f)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            c.perform()
            c.close()

    print(str(len(urls[genre])) + '/' + str(len(urls[genre])) + ' - ' + genre + ' complete.')