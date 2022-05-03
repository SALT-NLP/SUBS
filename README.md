# SUBS

This repo contains codes for the following paper: 

*Jingfeng Yang, Le Zhang, Diyi Yang* SUBS: Subtree Substitution for Compositional Semantic Parsing. (NAACL' 2022)

If you would like to refer to it, please cite the paper mentioned above. 


## Getting Started
These instructions will get you running the codes.

### Requirements
* treelib
* Pytorch 
* OpenNMT 1.2
* fairseq

### Run on GeoQuery

Run for SUBS data augmentation:
```
bash run_suns.sh 
```
Run BART or LSTM parser:
```
bash new_aug_query_gold_span_logic_bart_large.sh ||
bash new_aug_query_induce_logic_copy.sh
```
Refer to other bash files for other settings.

### Run on SCAN
Run for SUBS data augmentation:
```
python recomb_scan.py
```
Run parser:
```
bash scan_right_aug.sh
```
Refer to other bash files for other settings.

## Aknowledgement

Parsers are adapted from [OpenNMT](https://github.com/OpenNMT/OpenNMT-py) and [fairseq](https://github.com/pytorch/fairseq).