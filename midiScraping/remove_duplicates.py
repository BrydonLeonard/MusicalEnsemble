import argparse

parser = argparse.ArgumentParser(description='Deduplicate a file of midi download urls. The final item on each line should be the url')
parser.add_argument('urlFile', help='The file to deduplicate')
parser.add_argument('urlOutputFile', help='The file to write to')

args = parser.parse_args()

f = open(args.urlFile)
lines = f.read().split('\n')
f.close()

del lines[0]

url_dict = dict()

for line in lines:
    spl = line.split(',')
    url_dict[spl[-1]] = ','.join(spl[:-1])


no_duplicates_file = open(args.urlOutputFile, 'w')
for url in url_dict:
    no_duplicates_file.write(','.join([url_dict[url], url]) + '\n')

no_duplicates_file.close()
