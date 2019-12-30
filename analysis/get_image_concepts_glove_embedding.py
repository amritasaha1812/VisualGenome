#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:22:07 2019

@author: amrita
"""
import json
import pickle as pkl
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
 
visual_genome_dir = '..'
glove_clustering_dir = '../../GloVe_Clustering'
region_caption_data = json.load(open(visual_genome_dir+'/data/raw/region_graphs.json'))
glove_embedding = {x.strip().split(' ')[0]:[float(xi) for xi in x.strip().split(' ')[1:]] for x in open(glove_clustering_dir+'/data/glove/glove.6B.100d.txt').readlines()}
count = 0.0
image_phrase_dict = {}
for i in range(len(region_caption_data)):
    image_id = region_caption_data[i]['image_id']
    region_phrase_words = set([])
    for region in region_caption_data[i]['regions']:
        bbox = (region['x'], region['y'], region['height'], region['width'])
        region_str = str(image_id)+" "+str(bbox[0])+" "+str(bbox[1])+" "+str(bbox[2])+" "+str(bbox[3])
        region_phrase_words.update(set(region['phrase'].strip(' .?!').lower().split(' ')))
    region_wordembs = {w:glove_embedding[w] for w in region_phrase_words if w in glove_embedding}
    image_phrase_dict[image_id] = region_wordembs
pkl.dump(image_phrase_dict, open(visual_genome_dir+'/data/preprocessed/image_concepts_glove_embedding_filtered_datasize100.pkl','wb'))     
