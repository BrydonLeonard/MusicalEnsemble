import argparse

parser = argparse.ArgumentParser(description='Deduplicate a file of midi download urls. The final item on each line should be the url')
parser.add_argument('urlFile', help='The file to deduplicate')
parser.add_argument('urlOutputFile', help='The file to write to')
parser.add_argument('-g', '--genreOutputFile', type=str, help='File to write genres to.', default='../genres.csv')

args = parser.parse_args()

f = open(args.urlFile)
lines = f.read().split('\n')
f.close()

url_dict = dict()
genres = set()

for line in lines:
	if line:
		spl = line.split(',')
		url_dict[spl[-1]] = ','.join(spl[:-1])
		track_genres = spl[1].split('-')
		for g in track_genres:
			genres.add(g)


with open(args.urlOutputFile, 'w') as no_duplicates_file:
	for url in url_dict:
		no_duplicates_file.write(','.join([url_dict[url], url]) + '\n')
		
with open(args.genreOutputFile, 'w') as genre_file:
	genre_file.write('\n'.join(genres))
