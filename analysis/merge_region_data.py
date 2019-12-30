import pickle as pkl
import os
import sys
type_of_data = sys.argv[1]
if type_of_data not in ['attribute', 'attribute_negative','synset']:
    raise Exception('Wrong Argument... should be one of (\'attribute\', \'attribute_negative\', \'synset\'')
visual_genome_dir ='..'
data = {}
dir = visual_genome_dir+'/data/preprocessed/'+type_of_data+'_region_data/'
for file in os.listdir(dir):
	file = dir+'/'+file
	d = pkl.load(open(file,'rb'),encoding='latin1')
	print ('file ', file, 'len ', len(d), 'len ', len(data))
	for k1 in d:
		k1_word = k1.strip().lower().replace(' ','_')
		if type_of_data=='synset' and len(k1_word.split('.'))==3:
			k1_word = '.'.join(k1_word.split('.')[:-2])
		if k1_word not in data:
			data[k1_word] = d[k1]
		else:
			for k2 in d[k1]:
				if k2 not in data[k1_word]:
					data[k1_word][k2] = d[k1][k2]
				else:
					data[k1_word][k2].extend(d[k1][k2])
pkl.dump(data, open('../data/preprocessed/'+type_of_data+'_regions.pkl','wb'))
