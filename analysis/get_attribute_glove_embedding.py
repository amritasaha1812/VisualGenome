import pickle as pkl
import numpy as np
visual_genome_dir = '..'
glove_clustering_dir = '../../GloVe_Clustering'
#attributes = pkl.load(open(visual_genome_dir+'/data/preprocessed/attribute_regions_filtered_freq10_top100.pkl','rb'), encoding='latin1').keys()
attributes = pkl.load(open(visual_genome_dir+'/data/preprocessed/synset_regions_filtered_datasize100.pkl','rb'), encoding='latin1').keys()
attributes_vocab = {}
i = 0
for att in attributes:
	attributes_vocab[att] = i
	i += 1
attribute_glove_emb = {x.strip().split(' ')[0]:[float(xi) for xi in x.strip().split(' ')[1:]] for x in open(glove_clustering_dir+'/data/glove/glove.6B.100d.txt').readlines()}
new_attributes_glove_emb = {}
for attr in attributes_vocab:
	words = attr.replace('-','_').replace("'s","").replace("?","").replace(",","_").strip().split('_')
	words = ['.'.join(x.split('.')[:-2]) for x in words]
	embs = []
	for word in words:
		if word in attribute_glove_emb:	
			embs.append(attribute_glove_emb[word])
	if len(embs)>0:
		embs = np.asarray(embs)
		emb = np.mean(embs, axis=0)
	else:
		print ('Found no embedding ', attr)
		emb = np.asarray([0.]*100)
	new_attributes_glove_emb[attr] = emb
#new_attributes_glove_emb = np.asarray(new_attributes_glove_emb)
#np.save(visual_genome_dir+'/data/preprocessed/attribute_glove_emb_filtered_datasize100.npy', new_attributes_glove_emb)
#np.save(visual_genome_dir+'/data/preprocessed/attribute_glove_emb_filtered_freq10_top100.npy', new_attributes_glove_emb)
pkl.dump(new_attributes_glove_emb, open(visual_genome_dir+'/data/preprocessed/synset_glove_emb_filtered_datasize100.pkl','wb'))
