import json
import numpy as np
import pickle as pkl
import sys
import os

visual_genome_dir = '..'
if not os.path.exists(visual_genome_dir+'/data/preprocessed/attribute_region_data/'):
   os.mkdir(visual_genome_dir+'/data/preprocessed/attribute_region_data/')
if not os.path.exists(visual_genome_dir+'/data/preprocessed/synset_region_data/'):
   os.mkdir(visual_genome_dir+'/data/preprocessed/synset_region_data/')
split_id = int(sys.argv[1])
num_splits = int(sys.argv[2])
attribute_region_data = {}
synset_region_data = {}
data_attr = {d['image_id']:d['attributes'] for d in json.load(open(visual_genome_dir+'/data/raw/attributes.json'))}
data_obj = {d['image_id']:d['objects'] for d in json.load(open(visual_genome_dir+'/data/raw/objects.json'))}
image_ids = sorted(list(data_obj.keys()))
split_len = int(len(image_ids)/float(num_splits))
start = split_len*split_id
print ('Split Length ', split_len)
n1=0
n2=0
for i,img_id in enumerate(image_ids[start:start+split_len]):
   if i%1000==0:
        print ('Finished ', float(i)/float(len(image_ids)), 'images')
   attributes = data_attr[img_id]
   objects = data_obj[img_id]
   bboxes_in_attributes = []    
   for attr in attributes:
        if 'attributes' not in attr or len(attr['attributes'])==0:
                continue
        bbox = (attr['x'], attr['y'], attr['h'], attr['w'])
        for syn in attr['synsets']:
                if syn not in synset_region_data:
                        synset_region_data[syn] = {}
                for at in attr['attributes']:
                        if at not in synset_region_data[syn]:
                               synset_region_data[syn][at] = []
                        synset_region_data[syn][at].append({'image_id':img_id, 'bbox':bbox})
                        n1+=1	
        for at in attr['attributes']:
                if at not in attribute_region_data:
                        attribute_region_data[at] = {}
                for syn in attr['synsets']:
                        if syn not in attribute_region_data[at]:
                               attribute_region_data[at][syn] = []
                        attribute_region_data[at][syn].append({'image_id':img_id, 'bbox':bbox})
                        n2+=1
        bboxes_in_attributes.append(bbox)
   for obj in objects:
        bbox = (obj['x'], obj['y'], obj['h'], obj['w'])
        if bbox not in bboxes_in_attributes:
             for syn in obj['synsets']:
                 if syn not in synset_region_data:
                        synset_region_data[syn] = {}
                 if 'no-attribute' not in synset_region_data[syn]:
                        synset_region_data[syn]['no-attribute'] = []
                 synset_region_data[syn]['no-attribute'].append({'image_id':img_id, 'bbox':bbox}) 
                 n1+=1
   if n1%1000==0:
        print ('added ',len(synset_region_data), ' synsets') 
        pkl.dump(synset_region_data, open(visual_genome_dir+'/data/preprocessed/synset_region_data/data_split_'+str(split_id)+'.pkl','wb'))
   if n2%1000==0:
        print ('added ', len(attribute_region_data), ' attributes')
        pkl.dump(attribute_region_data, open(visual_genome_dir+'/data/preprocessed/attribute_region_data/data_split_'+str(split_id)+'.pkl','wb'))
pkl.dump(synset_region_data, open(visual_genome_dir+'/data/preprocessed/synset_region_data/data_split_'+str(split_id)+'.pkl','wb'))
pkl.dump(attribute_region_data, open(visual_genome_dir+'/data/preprocessed/attribute_region_data/data_split_'+str(split_id)+'.pkl','wb'))			

