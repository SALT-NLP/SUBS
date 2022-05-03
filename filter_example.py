import json
from treelib import Node, Tree
import re
import random

import argparse
parser = argparse.ArgumentParser(description='Calculate Acc')
parser.add_argument('-train', default='datasets/geo/funql/train_template.json', help='Predited file')
parser.add_argument('-no_dup_train', default='induced/template.json', help='Predited file')
parser.add_argument('-out', default='induced/template.json', help='Predited file')
parser.add_argument('-num', type=int, default=200, help='Number of examples')

args = parser.parse_args()
all_sem=[]   

f_list=[]
with open(args.no_dup_train) as reader:
    for line in reader:
        f_list.append(line.split('|||')[0].strip())

num = 0
write_list=[]
with open(args.out, 'w') as writer:
    with open(args.train) as reader:
        for line in reader:
            string_instance = json.loads(line.strip())
            sent = ' '.join(string_instance['question'].strip().split()[:-1])

            if sent in f_list:
                write_list.append(line.strip())
                writer.write(line.strip()+'\n')
                num +=1
                if num >= args.num:
                    break
    
    if len(write_list) < args.num:
        with open(args.train) as reader:
            for line in reader:
                if line.strip() not in write_list:
                    writer.write(line.strip()+'\n')
                    num +=1
                    if num >= args.num:
                        break




