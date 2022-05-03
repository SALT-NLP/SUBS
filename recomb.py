import json
from treelib import Node, Tree
import re
import random

import argparse
parser = argparse.ArgumentParser(description='Calculate Acc')
parser.add_argument('-train', default='geo/train_spans.json', help='Predited file')
parser.add_argument('-dev', default='geo/dev_spans.json', help='Gold file')
parser.add_argument('-test', default='geo/test_spans.json', help='test Gold file')
parser.add_argument('-comp', default='', help='test Gold file')
args = parser.parse_args()

all_sem=[]
with open(args.train) as reader:
    for line in reader:
        string_instance = json.loads(line.strip())
        print(string_instance['question'])
        print(string_instance['program'])
        print(string_instance['gold_spans'])
        print()
        tree = Tree()
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
        tree.show()

def twoArgs(a, b):
    t1=a['sem']
    t2=b['sem']
    if '(' in t1 and '(' in t2:
        assert('exclude' in t1 or 'exclude' in t2)
        if 'exclude' in t1:
            assert(t1[-1]==')')
            return t1[:-1] + ', ' + t2 + ' )'
        else:
            assert(t2[-1]==')')
            return t2[:-1] + ', ' + t1 + ' )'
    elif '(' in t1:
        return t2+' ( '+t1+' )'
    elif '(' in t2:
        return t1+' ( '+t2+' )'
    elif '#' in t1:
        return t2+' ( '+' ( '.join(t1.split('#'))+(', _ ) )' if t1.split('#')[0]=='cityid' else ' ) )')
    elif '#' in t2:
        return t1+' ( '+' ( '.join(t2.split('#'))+(', _ ) )' if t2.split('#')[0]=='cityid' else ' ) )')
    else:
        t1, t2 = sorted([a, b], key=lambda x:int(x['span'][0]))
        entity_list=['state', 'city', 'river', 'capital', 'mountain', 'place']
        assert(t1['sem'] in entity_list or t2['sem'] in entity_list)
        if t1['sem'] in entity_list:
            return t2['sem']+' ( '+t1['sem']+' ( all ) )'
        else:
            return t1['sem']+' ( '+t2['sem']+' ( all ) )'

def tranverseTree(tree, cur_node):
    tag_list=[]
    for c in tree.children(cur_node):
        tranverseTree(tree, c.identifier)
        tag_list.append(json.loads(c.tag))
    d=json.loads(tree.get_node(cur_node).tag)
    if len(tag_list)==0:
        d['sem'] = d['type']
    elif len(tag_list)==1:
        d['sem'] = tag_list[0]['sem']
    elif len(tag_list)==2:
        d['sem']=twoArgs(tag_list[0], tag_list[1])
        '''t1=tag_list[0]['sem']
        t2=tag_list[1]['sem']
        if '(' in t1 and '(' in t2:
            assert(t1[-1]==')')
            d['sem']=t1[:-1] + ', ' + t2 + ' )'
        elif '(' in t1:
            d['sem']=t2+' ( '+t1+' )'
        elif '(' in t2:
            d['sem']=t1+' ( '+t2+' )'
        elif '#' in t1:
            d['sem']=t2+' ( '+' ( '.join(t1.split('#'))+(', _ ) )' if t1.split('#')[0]=='cityid' else ' ) )')
        elif '#' in t2:
            d['sem']=t1+' ( '+' ( '.join(t2.split('#'))+(', _ ) )' if t2.split('#')[0]=='cityid' else ' ) )')
        else:
            t1, t2 = sorted([tag_list[0], tag_list[1]], key=lambda x:int(x['span'][0]))
            entity_list=['state']
            if t1['sem'] in entity_list:
                d['sem']=t2['sem']+' ( '+t1['sem']+' ( all ) )'
            else:
                d['sem']=t1['sem']+' ( '+t2['sem']+' ( all ) )'''
    else:
        assert(len(tag_list)==3)
        t1, t2, t3 = sorted([tag_list[0], tag_list[1], tag_list[2]], key=lambda x:int(x['span'][0]))
        #' ( '.join(t1.split('#'))
        d['sem']=t2['sem']+' ( ' + twoArgs(t1, t3)+ ' )' 

    tree.get_node(cur_node).tag=json.dumps(d)


for l in all_sem:
    print(l[0])
    print(l[1])
    tranverseTree(l[3], l[3].root)
    l[3].show()
    pred=json.loads(l[3].get_node(l[3].root).tag)['sem']
    if not '(' in pred:
        pred=pred + ' ( all )'
    print('g', l[1])
    print('p', 'answer ( ' +pred+ ' )')
    assert(l[1]=='answer ( ' +pred+ ' )')
    print()
        
sem_dict={}
for l in all_sem:
    for item in re.sub(r"\'.*\'", '', l[1]).split():
        if item not in ['(', ')', '_'] and not item[0]=="'" and not item[-1]=="'" and not item =='answer' and not item == 'all':
            sem_dict[item]=[]

print(sem_dict)
print(len(sem_dict))

for l in all_sem:
    sem = l[1].split()
    sent = l[0].split()
    print(sent)
    print(sem)
    l[3].show()
    for i in range(len(sem)):
        if sem[i] in sem_dict:
            print('!!!',sem[i])
            id = ''
            for n in l[3].leaves():
                if json.loads(n.tag)['type']== sem[i]:
                    id = n.identifier
                    break
            if id == '':
                continue ########more cases
            while l[3].parent(id) is not None and json.loads(l[3].parent(id).tag)['sem']==json.loads(l[3].get_node(id).tag)['sem']:
                id = l[3].parent(id).identifier
                #print('sem', json.loads(l[3].parent(id).tag))
            if l[3].parent(id) is None:
                print('*********************')
                continue
            assert(len(l[3].children(l[3].parent(id).identifier))==2 or len(l[3].children(l[3].parent(id).identifier))==3)
            if len(l[3].children(l[3].parent(id).identifier))==2 and json.loads(l[3].parent(id).tag)['sem'].startswith(sem[i]):
                p_span=json.loads(l[3].parent(id).tag)['span']
                c_span=json.loads(l[3].get_node(id).tag)['span']
                l_start=int(p_span[0])
                l_end=int(c_span[0])
                r_start=int(c_span[1])+1
                r_end=int(p_span[1])+1
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!", sem[i])
                continue
            f_seg=[]
            f_seg.append(sent[l_start: l_end])
            f_seg.append(sent[r_start: r_end])
            assert(sem[i+1]=='(')
            num=1
            j=i+1
            while num>0:
                j+=1
                if sem[j]=='(':
                    num+=1
                if sem[j]==')':
                    num-=1
            f_sem=sem[i+2:j]
            print('@@',sem[i],(f_sem, f_seg))
            sem_dict[sem[i]].append((f_sem, f_seg))
#print(sem_dict)

augmented_pairs = {}

seg_lens=[]
seg_olens=[]

for l in all_sem:
    sem = l[1].split()
    sent = l[0].split()
    '''print(sent)
    print(sem)
    l[3].show()'''
    for i in range(len(sem)):
        if sem[i] in sem_dict:
            #print('!!!',sem[i])
            id = ''
            for n in l[3].leaves():
                if json.loads(n.tag)['type']== sem[i]:
                    id = n.identifier
                    break
            if id == '':
                continue ########more cases
            while l[3].parent(id) is not None and json.loads(l[3].parent(id).tag)['sem']==json.loads(l[3].get_node(id).tag)['sem']:
                id = l[3].parent(id).identifier
                #print('sem', json.loads(l[3].parent(id).tag))
            if l[3].parent(id) is None:
                print('*********************')
                continue
            assert(len(l[3].children(l[3].parent(id).identifier))==2 or len(l[3].children(l[3].parent(id).identifier))==3)
            if len(l[3].children(l[3].parent(id).identifier))==2 and json.loads(l[3].parent(id).tag)['sem'].startswith(sem[i]):
                p_span=json.loads(l[3].parent(id).tag)['span']
                c_span=json.loads(l[3].get_node(id).tag)['span']
                l_start=int(p_span[0])
                l_end=int(c_span[0])
                r_start=int(c_span[1])+1
                r_end=int(p_span[1])+1
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!", sem[i])
                continue
            f_seg=[]
            f_seg.append(sent[l_start: l_end])
            f_seg.append(sent[r_start: r_end])
            assert(sem[i+1]=='(')
            num=1
            j=i+1
            while num>0:
                j+=1
                if sem[j]=='(':
                    num+=1
                if sem[j]==')':
                    num-=1
            f_sem=sem[i+2:j]
            #print('@@',sem[i],(f_sem, f_seg))
            for t in sem_dict[sem[i]]:
                if len(f_seg[0])==0 and not len(t[1][0])==0:
                    continue
                if len(f_seg[1])==0 and not len(t[1][1])==0:
                    continue
                #print(sent[:l_start] , t[1][0] , sent[l_end: r_start] , t[1][1] , sent[r_end:])
                c_sent= sent[:l_start] + t[1][0] + sent[l_end: r_start] + t[1][1] + sent[r_end:]
                #print(sem[:i+2] , t[0] , sem[j:])
                c_sem= sem[:i+2] + t[0] + sem[j:]
                
                #print('pair 1: ', ' '.join(c_sent))
                #print('pair 2: ', ' '.join(c_sem))
                if ' '.join(c_sent) not in augmented_pairs:
                    seg_lens.append(len(t[1][0]+t[1][1]))
                    seg_olens.append(len(t[0]))
                    augmented_pairs[' '.join(c_sent)]=' '.join(c_sem)
                if len(t[1][0]+t[1][1])>8 and len(c_sent)>15:
                    print(sent)
                    print(sem)
                    print(sent[:l_start] , t[1][0] , sent[l_end: r_start] , t[1][1] , sent[r_end:])
                    print(sem[:i+2] , t[0] , sem[j:])
                    print('pair 1: ', ' '.join(c_sent))
                    print('pair 2: ', ' '.join(c_sem))
                    l[3].show()

print('!!!!!')
print(sum(seg_lens) / len(seg_lens))
print(max(seg_lens))

print('!!!!!')
print(sum(seg_olens) / len(seg_olens))
print(max(seg_olens))
print(len(seg_lens))

print('!!!!!')
print(sum(seg_lens+seg_olens) / len(seg_lens+seg_olens))
print(max(seg_lens+seg_olens))

lens=[]
olens=[]

for key, value in augmented_pairs.items():
    #print(key)
    lens.append(len(key.split()))
    #print(value)
    olens.append(len(value.split()))
    #print()
    
print('!!!!!')
print(sum(lens) / len(lens))
print(max(lens))

print('!!!!!')
print(sum(olens) / len(olens))
print(max(olens))


f_list=list(augmented_pairs.items())
with open(args.train) as reader:
    for line in reader:
        string_instance = json.loads(line.strip())
        f_list.append((string_instance['question'],string_instance['program']))
#print(f_list)
random.shuffle(f_list)
with open(args.comp+"data/src_aug.train", 'w', encoding='utf-8') as writer1, open(args.comp+"data/tgt_aug.train", 'w', encoding='utf-8') as writer2:
    for key, value in f_list:
        writer1.write(key+'\n')
        writer2.write(value.replace("'", '')+'\n')

with open(args.train) as reader, open(args.comp+"data/src.train", 'w', encoding='utf-8') as writer1, open(args.comp+"data/tgt.train", 'w', encoding='utf-8') as writer2:
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        writer2.write(string_instance['program'].replace("'", '')+'\n')

with open(args.dev) as reader, open(args.comp+"data/src.val", 'w', encoding='utf-8') as writer1, open(args.comp+"data/tgt.val", 'w', encoding='utf-8') as writer2:
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        writer2.write(string_instance['program'].replace("'", '')+'\n')

with open(args.test) as reader, open(args.comp+"data/src.test", 'w', encoding='utf-8') as writer1, open(args.comp+"data/tgt.test", 'w', encoding='utf-8') as writer2:
    for line in reader:
        string_instance = json.loads(line.strip())
        writer1.write(string_instance['question']+'\n')
        writer2.write(string_instance['program'].replace("'", '')+'\n')
    
print(len(augmented_pairs))                