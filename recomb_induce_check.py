import json
from treelib import Node, Tree
import re
import random

import argparse
parser = argparse.ArgumentParser(description='Calculate Acc')
parser.add_argument('-train', default='datasets/geo/funql/train_template.json', help='Predited file')
parser.add_argument('-all_train', default='induced/template.json', help='Predited file')

args = parser.parse_args()
all_sem=[]   


f_list=[]
with open(args.all_train) as reader:
    for line in reader:
        string_instance = json.loads(line.strip())
        f_list.append(string_instance['question'])

with open(args.train) as reader:
    for line in reader:
        string_instance = json.loads(line.strip())
        if not string_instance['question'] in f_list:
            print(string_instance['question'])
        #assert(string_instance['question'] in f_list)