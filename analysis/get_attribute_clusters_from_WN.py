#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:32:51 2019

@author: amrita
"""

import json
import nltk
from nltk.corpus import wordnet as wn
from spacy.lemmatizer import Lemmatizer
import sys
glove_clustering_dir = '../../GloVe_Clustering'
visual_genome_dir = '..'
glove_clusters = json.load(open(glove_clustering_dir+'/data/cache/100D_6315-words_1000-clusters.json'))
glove_clusters_expanded = {}
for c in glove_clusters:
        for w in c:
                glove_clusters_expanded[w] = set(c) - set([w])

lemmatizer = Lemmatizer()
bad_words = set(['entity', 'physical_entity', 'object', 'whole', 'artifact', 'thing', 'part', 'relation', 'matter', 'substance'])
attributes = set([x for x in json.load(open(visual_genome_dir+'/data/raw/attribute_types.json'))])
attribute_names = set(['.'.join(x.split('.')[:-2]) for x in attributes])
attribute_names.update(['.'.join(x.split('.')[:-1]) for x in json.load(open(visual_genome_dir+'/data/preprocessed/attribute_types_expanded.json')).keys()])
attribute_clusters = {}

for attribute in attributes:
    attribute_name = '.'.join(attribute.split('.')[:-2])
    attribute_lemma = lemmatizer(attribute_name, 'NOUN')[0]
    ss = wn.synset(attribute)
    parents = set([])
    grandparents = set([])
    first_level_siblings = set([])
    second_level_siblings = set([])
    for path in ss.hypernym_paths():
        if len(path)<2:
            continue
        parent = path[-2]
        if len(path)<3:
            grandparent = None
        else:
            grandparent = path[-3]
        parent_name = parent.name()
        if grandparent is None:
            grandparent_name = None
        else:
            grandparent_name = grandparent.name()
        for x in parent.hyponyms():
            first_level_siblings.add(x.name())
            first_level_siblings.update([xi.name() for xi in wn.synsets(x.name())])
        first_level_siblings = first_level_siblings.intersection(attribute_names)
        if grandparent is not None:
            for parent1 in grandparent.hyponyms():
                second_level_siblings.update([x.name() for x in parent1.hyponyms()])
                for x in parent1.hyponyms():
                    second_level_siblings.add(x.name())
                    second_level_siblings.update([xi.name() for xi in wn.synsets(x.name())])
            second_level_siblings = second_level_siblings.intersection(attribute_names)    
       	 
        
        if len(first_level_siblings)==0 and len(second_level_siblings)==0:
            continue
        if attribute_name not in glove_clusters_expanded:
            glove_clusters_expanded[attribute_name] = set([])
        glove_clusters_expanded[attribute_name].update(first_level_siblings)
        glove_clusters_expanded[attribute_name].update(second_level_siblings)
        first_level_siblings.add(attribute_name)
        second_level_siblings.add(attribute_name)
        for s in first_level_siblings:
            if s not in glove_clusters_expanded:
                glove_clusters_expanded[s] = set([])
            glove_clusters_expanded[s].update(first_level_siblings - set([s]))
            glove_clusters_expanded[s].update(second_level_siblings - set([s]))
    if attribute_name not in glove_clusters_expanded:
        print ('no cluster for ', attribute_name)
    else:
        print ('found cluster for ', attribute_name, ':::', glove_clusters_expanded[attribute_name])    
        
for k in glove_clusters_expanded:        
       glove_clusters_expanded[k] = list(glove_clusters_expanded[k])     
      
json.dump(glove_clusters_expanded, open(visual_genome_dir+'/data/preprocessed/attribute_clusters.json','w'), indent=1)                
