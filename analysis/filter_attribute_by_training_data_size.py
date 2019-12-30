#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:51:46 2019

@author: amrita
"""
import pickle as pkl
import operator 

visual_genome_dir = '..'
synsets_pos_data = pkl.load(open(visual_genome_dir+'/data/preprocessed/synset_regions.pkl','rb'), encoding='latin1')
synsets_pos_data_size = {}
for k,v in synsets_pos_data.items():
    if k not in synsets_pos_data_size:
        synsets_pos_data_size[k] = 0
    for syn,syn_data in v.items():
        synsets_pos_data_size[k] += len(syn_data)
for k in list(synsets_pos_data.keys()):
    data_size = synsets_pos_data_size[k]
    if data_size > 100:
        continue
    if k in synsets_pos_data:
        del synsets_pos_data[k]
synsets_pos_data = pkl.dump(synsets_pos_data, open(visual_genome_dir+'/data/preprocessed/synset_regions_filtered_datasize100.pkl','wb'))

attributes_pos_data = pkl.load(open(visual_genome_dir+'/data/preprocessed/attribute_regions.pkl','rb'), encoding='latin1')
attributes_pos_data_size = {}
for k,v in attributes_pos_data.items():
    if k not in attributes_pos_data_size:
        attributes_pos_data_size[k] = 0
    for syn,syn_data in v.items():
        attributes_pos_data_size[k] += len(syn_data)
for k in list(attributes_pos_data.keys()):
    data_size = attributes_pos_data_size[k]
    if data_size > 100:
        continue
    if k in attributes_pos_data:
        del attributes_pos_data[k]
attributes_pos_data = pkl.dump(attributes_pos_data, open(visual_genome_dir+'/data/preprocessed/attribute_regions_filtered_datasize100.pkl','wb'))
