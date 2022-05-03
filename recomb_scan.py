import json
from treelib import Node, Tree
import re
import random

import argparse
parser = argparse.ArgumentParser(description='Calculate Acc')
parser.add_argument('-train', default='datasets/scan/dsl/train_right_spans.json', help='Predited file')
parser.add_argument('-dev', default='datasets/scan/dsl/scan/dev_right_spans.json', help='Gold file')
parser.add_argument('-test', default='datasets/scan/dsl/scan/test_right_spans.json', help='test Gold file')
parser.add_argument('-comp', default='', help='test Gold file')
args = parser.parse_args()

all_sem=[]
semt=set()
orderD={'i_after':5, 'i_and':5, 'i_twice':4, 'i_thrice':4, 'i_jump':3, 'i_run':3, 'i_look':3, 'i_walk':3, 'i_turn':3, 'i_opposite':2, 'i_around':2,  'i_right':1, 'i_left':1 }

def correctFormat(string_instance):
    plist=string_instance.split()
    clist=[]
    for t in plist:
        if not t=='(' and  not t ==')' and not t==',':
            semt.add(t)
    i=0
    while i<len(plist):
        if (plist[i]=='i_left' or plist[i]=='i_right') and plist[i+1]==',':
            clist.append(plist[i+2])
            clist.append('(')
            clist.append(plist[i])
            clist.append(')')
            i+=3
        elif plist[i] in orderD and orderD[plist[i]]==3 and plist[i+2]==')':
            clist.append(plist[i])
            i+=3
        else:
            clist.append(plist[i])
            i+=1
    return ' '.join(clist)

with open(args.train) as reader:
    for line in reader:
        string_instance = json.loads(line.strip())
        
        string_instance['program'] = correctFormat(string_instance['program'])

        print(string_instance['question'])
        print(string_instance['program'])
        print(string_instance['gold_spans'])
        print()
        tree = Tree()
        assert(int(string_instance['gold_spans'][0]['span'][0])==0)
        
        while not int(string_instance['gold_spans'][0]['span'][1]) == len(string_instance['question'].split())-1:
            #print('^^^^^^^^^^^^^^^^')
            flag=int(string_instance['gold_spans'][0]['span'][1])
            va=0
            #print(flag, va)
            for sp in string_instance['gold_spans']:
                if sp['type'].startswith('i'):
                    if not sp['span'][0]==sp['span'][1]:
                        #print(sp)
                        if int(sp['span'][0]) <= flag:
                        #assert(int(sp['span'][1])-int(sp['span'][0])==int(string_instance['gold_spans'][0]['span'][1])-len(string_instance['question'].split())+1)
                            flag=int(sp['span'][0])
                            va=int(sp['span'][1])-int(sp['span'][0])
            #print(flag, va)
            #print('vvvvv',va)
            for sp in string_instance['gold_spans']:
                if int(sp['span'][0])>flag:
                    sp['span'][0]=int(sp['span'][0])-va
                if int(sp['span'][1])>flag:
                    sp['span'][1]=int(sp['span'][1])-va
            #print('&&&&&&', string_instance)
            
        assert(int(string_instance['gold_spans'][0]['span'][1]) == len(string_instance['question'].split())-1)


        for item in string_instance['gold_spans']:
            
            i_0 = int(item['span'][0])
            i_1 = int(item['span'][1])
            #print(i_0,i_1, len(string_instance['question'].split())-1)
            if i_0==0 and i_1==len(string_instance['question'].split())-1:
                tree.create_node(json.dumps(item), str(i_0)+' '+str(i_1))
            else:
                cur_node=tree.root
                #print(cur_node)
                while True:
                    if len(tree.children(cur_node)) == 0:
                        #print(i_0,i_1)
                        #tree.show()
                        tree.create_node(json.dumps(item), str(i_0)+' '+str(i_1), parent=cur_node)
                        break
                    flag=0
                    for n in tree.children(cur_node):
                        #print("!!!", int(n.identifier.split()[0]), i_0, int(n.identifier.split()[1]), i_1)
                        if int(n.identifier.split()[0])<=i_0 and int(n.identifier.split()[1])>=i_1:
                            cur_node = n.identifier
                            flag=1
                            break
                    if flag==1:
                        continue   
                    #print(i_0,i_1)
                    #tree.show()
                    #print("!!!", cur_node)
                    tree.create_node(json.dumps(item), str(i_0)+' '+str(i_1), parent=cur_node)
                    
                    move_list=[]
                    
                    for n in tree.children(cur_node):
                        if not n.identifier == str(i_0)+' '+str(i_1):
                            if int(n.identifier.split()[0])>=i_0 and int(n.identifier.split()[1])<=i_1:
                                move_list.append(n.identifier)
                    for m in move_list:
                        tree.move_node(m, str(i_0)+' '+str(i_1))
                    #tree.show()
                    
                    break
        '''for i, t in enumerate(string_instance['question'].split()):
            cur_node=tree.root
            while True:
                #print(i,t)
                
                if len(tree.children(cur_node)) == 0:
                    tree.create_node(t, str(i), parent=cur_node)
                    break
                flag=0
                for n in tree.children(cur_node):
                    if len(n.identifier.split())==2 and int(n.identifier.split()[0])<=i and int(n.identifier.split()[1])>=i:
                        cur_node = n.identifier
                        flag=1
                        break
                if flag==1:
                    #print(cur_node)
                    #print(flag)
                    continue 
                tree.create_node(t, str(i), parent=cur_node)
                #tree.show()
                break'''      
        all_sem.append((string_instance['question'], string_instance['program'], string_instance['gold_spans'], tree))  
        print('#######')   
        tree.show()

    print(semt,len(semt))

def twoArgs(a, b):
    t1=a['sem'] if orderD[a['sem'].split()[0]] > orderD[b['sem'].split()[0]] else b['sem']
    t2=b['sem'] if orderD[a['sem'].split()[0]] > orderD[b['sem'].split()[0]] else a['sem']
    '''if not t1.split()[0] in ['i_after', 'i_and']:
        print(t1, t2)
        assert(not '(' in t1)'''
    if not '(' in t1:
        return t1+' ( '+t2+' )'
    else:
        assert t1.split()[0] in ['i_after', 'i_and'] or t2 in ['i_left', 'i_right']
        if t1.split()[0] in ['i_after', 'i_and']:
            return ' '.join(t1.split()[:-1] + [','] + t2.split() +[')'])
        else:
            return ' '.join(t1.split()[:-1] + ['('] + t2.split() +[')', ')'])

def tranverseTree(tree, cur_node):
    tag_list=[]
    for c in tree.children(cur_node):
        tranverseTree(tree, c.identifier)
        tag_list.append(json.loads(c.tag))
    d=json.loads(tree.get_node(cur_node).tag)
    if len(tag_list)==0:
        d['sem'] = d['type']
    else:
        assert(len(tag_list)==2)
        d['sem']=twoArgs(tag_list[0], tag_list[1])

    tree.get_node(cur_node).tag=json.dumps(d)


for l in all_sem:
    print(l[0])
    print(l[1])
    tranverseTree(l[3], l[3].root)
    l[3].show()
    pred=json.loads(l[3].get_node(l[3].root).tag)['sem']
    print('g', l[1])
    print('p', pred)
    assert(l[1]==pred)
    print()
        
sem_dict={}
for l in all_sem:
    for item in l[1].split():
        if item in ['i_left', 'i_right']:
            sem_dict[item]=[]

print(sem_dict)
print(len(sem_dict))

augmented_pairs = {}
for l in all_sem:
    sem = l[1].split()
    sent = l[0].split()
    print(l[0])
    print(l[1])
    augmented_pairs[l[0]]=l[1]
    #l[3].show()
    for n in l[3].leaves():
        i_tag=json.loads(n.tag)
        if i_tag['type'] in sem_dict:
            id = n.identifier
            c_span=json.loads(l[3].get_node(id).tag)['span']
            start=int(c_span[1])
            end=int(c_span[1])+1

            if i_tag['type'] == 'i_left':

                aug_sent = sent[:start] + ['right'] + sent[end:]
                i_tag['type'] = 'i_right'
                n.tag=json.dumps(i_tag)
                tranverseTree(l[3], l[3].root)
                aug_sem=json.loads(l[3].get_node(l[3].root).tag)['sem']

                i_tag['type'] = 'i_left'
                n.tag=json.dumps(i_tag)

                print(' '.join(aug_sent))
                print(aug_sem)
                augmented_pairs[' '.join(aug_sent)]=aug_sem

            if i_tag['type'] == 'i_right':

                aug_sent = sent[:start] + ['left'] + sent[end:]
                i_tag['type'] = 'i_left'
                n.tag=json.dumps(i_tag)
                tranverseTree(l[3], l[3].root)
                aug_sem=json.loads(l[3].get_node(l[3].root).tag)['sem']

                i_tag['type'] = 'i_right'
                n.tag=json.dumps(i_tag)
                print(' '.join(aug_sent))
                print(aug_sem)
                augmented_pairs[' '.join(aug_sent)]=aug_sem


f_list=list(augmented_pairs.items())
#print(f_list)
random.shuffle(f_list)
with open(args.comp+"scan_right/src_aug.train", 'w', encoding='utf-8') as writer1, open(args.comp+"scan_right/tgt_aug.train", 'w', encoding='utf-8') as writer2:
    for key, value in f_list:
        writer1.write(key+'\n')
        writer2.write(value+'\n')

all_set=set()
with open(args.train) as reader, open(args.comp+"scan_right/src.train", 'w', encoding='utf-8') as writer1, open(args.comp+"scan_right/tgt.train", 'w', encoding='utf-8') as writer2:
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        all_set.add(string_instance['question'])
        writer2.write(correctFormat(string_instance['program'])+'\n')


with open(args.dev) as reader, open(args.comp+"scan_right/src.val", 'w', encoding='utf-8') as writer1, open(args.comp+"scan_right/tgt.val", 'w', encoding='utf-8') as writer2:
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        writer2.write(correctFormat(string_instance['program'])+'\n')

with open(args.test) as reader, open(args.comp+"scan_right/src.test", 'w', encoding='utf-8') as writer1, open(args.comp+"scan_right/tgt.test", 'w', encoding='utf-8') as writer2:
    total=0
    intotal=0
    ointotal=0
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        writer2.write(correctFormat(string_instance['program'])+'\n')
        total+=1
        if string_instance['question'] in augmented_pairs:
            intotal+=1
        if string_instance['question'] in all_set:
            ointotal+=1
    print(total, intotal, intotal/float(total))
    print(total, ointotal, ointotal/float(total))
    
print(len(augmented_pairs))
