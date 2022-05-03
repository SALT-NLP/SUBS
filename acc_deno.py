import argparse
from geo_eval import executor_geo
from acc import readPredGold

parser = argparse.ArgumentParser(description='Calculate Acc')
parser.add_argument('-pred', default='', help='Predited file')
parser.add_argument('-gold', default='', help='Gold file')
parser.add_argument('-v', action='store_true', help='Gold file')
args = parser.parse_args()

def compute_acc(pred_sents, gold_sents):

    executor = executor_geo.ProgramExecutorGeo()

    total_num = 0
    correct_num = 0
    for pred, gold in zip(pred_sents,gold_sents):
        if len(gold)>0:
            total_num+=1

            pred_answer = 'init'
            gold_answer = 'init'

            pred_answer = executor.execute(' '.join(pred))
            gold_answer = executor.execute(' '.join(gold))

            assert not (gold_answer == 'init')
        
            if pred_answer==gold_answer:
                correct_num+=1
            else:
                if args.v:
                    print(gold)
                    print(pred)
                    print(gold_answer)
                    print(pred_answer)
                    print('---------------------------')
                pass

    print('Correct: %d, Total: %d, Acc: %f'% (correct_num, total_num, correct_num/total_num))


if __name__ == "__main__":
    pred_sents, gold_sents = readPredGold(args.pred, args.gold)
    compute_acc(pred_sents, gold_sents)

