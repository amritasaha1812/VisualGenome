## 1. Script to visualize the attribute and relation data from region annotations in the VisualGenome dataset. 
This script takes the attribute and relations json from the Visual Genome dataset and produces a json that summarizes the training data for each subject/verb/object. The data is of the form {'subject_i' : ['?-predictate-object']} for the subject json (and similarly for the object and verb json). It is supposed to give a quick visualizaiton of the different kind of tuples that appear with a given subject/verb or object.
* To run:  `python visualize_attribute_relation_catalog_data.py`

## 2. Script to extract the attribute and synset/object regions from the region annotations in VisualGenome dataset.
This script extracts all the regions corresponding to each attribute and object/synset in VisualGenome and dumps this in a json. The data for each attribute in the json looks like {'attribute_i': [{'image':..., 'bbox':(x,y,h,w)}]}. Similarly the data for each object/synset in the synset json looks like {'synset_i': [{'image':..., 'bbox':(x,y,h,w)}]}. This would be later used to create the training data for each attribute in the attribute catalog.
* To run (if parallerization is required): `./run_get_attribute_regions.sh`
* To run (if parallerization is not required): `python get_attribute_regions.py 0 1`

## 3. Script to merge the extracted region data for the attributes and synsets
Even if the above script is run in a non-parallelized mode, use this merging script to merge (and further cleanup if required) the jsons created from the extracted regions
* To run: 
   * Step 1) `python merge_region_data.py attribute` 
   * Step 2) `python merge_region_data.py synset`

## 4. Script to semantically cluster attributes.
This script semantically clusters attributes of similar types from the VisualGenome dataset based on Glove embedding and WordNet hypernym-hyponym hierarchy and Wordnet synonymy. It starts with the Glove based clustering and then further expands the clusters based on whether two words (i.e. attributes or their synonyms) are siblings of the first-order (sharing parents) or second order (sharing grandparents) of each other. 
* To run: `python get_attribute_clusters_from_WN.py`

## 5. Script to extract the negative regions corresponding to each attribute in the VisualGenome dataset. 
This script takes the original attribute regions extracted in Step 2 and the semantic clusters generated in Step 5 to do the following, to get the negative regions for each attribute in VisualGenome
* If an attribute belongs to a cluster, assume all its neighbors in the cluster as negative attributes. In that case add all the regions extracted in Step 2 as positive regions for each of the negative attributes as negative regions for the original attribute
* Additionally, for all the synsets (or objects) that the attribute appears with, all the region instances in the synset-region data (from step 3), where this attribute does not appear can be considered as weak signals for negative regions for the attribute
* To run (if parallerization is required): `./run_get_negative_attribute_regions.sh`
* To run (if parallerization is not required): `python get_negative_attribute_regions.py 0 1`

## 6. Script to merge the extracted negative region data for the attribute
Even if the above script is run in a non-parallelized mode, use this merging script to merge (and further cleanup if required) the jsons created from the extracted regions
* To run: `python merge_region_data.py attribute_negative`

## 7. Script to filter attributes based on various factors
 This script takes the original attribute list from VisualGenome data and filters it based on 
 i) `filter_attribute_based_on_VQA_histogram.py`: attribute should have occurred atleast a threshold number of times in the VQA dataset (where only surface level matching is done currently between the attribute in VisualGenome and its mention in the VQA dataset)
 ii) `filter_attribute_topk.py`: attribute is in the top-k most frequent attributes (as per occurrence in the VQA dataset)
 iii) `filter_attribute_by_training_data_size.py`: attribute has atleast N positive regions annotated with it in the VisualGenome dataset
 * To run i): `python filter_attribute_based_on_VQA_histogram.py`
 * To run ii): `python filter_attribute_topk.py`
 * To run iii): `python filter_attribute_by_training_data_size.py`

## 8. Script to get glove embedding of attributes
This script takes the pretrained glove embeddings available, and creates a numpy matrix containing the embeddings of the attribute words in VisualGenome. For phrases, it takes the average glove embedding of the individual words
* To run: `python get_attribute_glove_embedding.py`

## 9. Script to get a dictionary of all image regions required
This script takes the attribute region data (extracted in Steps 3 and 6) and compiles an entire list of all image regions for which region features need to be precomputed for training the catalog
* To run: `python get_region_dict.py`

## 10. Script to get region features of annotated regions
This script takes bounding box data from VisualGenome and extract the region as an image run pretrained resnet-34 on it to get 2048 dimension representations of that region and dump it in h5 format
* To run (if parallerization is required): `./run_get_region_features.sh`
* To run (if parallerization is not required): `python get_region_features.py 0 1`

## 11. Script to merge the precomputed region features 
Even if the above script is run run in a non-parallelized mode, use this merging script to merge (and further cleanup if required) the precomputed region features
* To run: `python merge_region_features.py`

<!--
python visualize_attribute_relation_catalog_data.py
./run_get_attribute_regions.sh
python merge_region_data.py attribute
python merge_region_data.py synset
python get_attribute_clusters_from_WN.py
./run_get_negative_attribute_regions.sh
python merge_region_data.py attribute_negative
python filter_attribute_based_on_VQA_histogram.py
python filter_attribute_topk.py
filter_attribute_by_training_data_size.py
python get_attribute_glove_embedding.py
python get_region_dict.py
./run_get_region_features.sh
python merge_region_features.py
-->
