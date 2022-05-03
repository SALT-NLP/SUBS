TASK=geo_subs_comp_data
PARAM='-aug-large-share-ebd2'


for SPLIT in train val test
do
  for LANG in src_aug tgt_aug
  do
    python -m examples.roberta.multiprocessing_bpe_encoder \
    --encoder-json /home/ec2-user/quic-efs/user/jingfe/util_files/bart.base/encoder.json \
    --vocab-bpe /home/ec2-user/quic-efs/user/jingfe/util_files/bart.base/vocab.bpe \
    --inputs "$TASK/$LANG.$SPLIT" \
    --outputs "$TASK/$SPLIT.bpe.$LANG" \
    --workers 60;
  done
done

fairseq-preprocess \
  --source-lang "src_aug" \
  --target-lang "tgt_aug" \
  --trainpref "${TASK}/train.bpe" \
  --validpref "${TASK}/val.bpe" \
  --destdir "${TASK}/bin-aug-large/" \
  --workers 60 \
  --srcdict /home/ec2-user/quic-efs/user/jingfe/util_files/bart.large/dict.txt \
  --tgtdict /home/ec2-user/quic-efs/user/jingfe/util_files/bart.large/dict.txt; 



#TOTAL_NUM_UPDATES=3000
TOTAL_NUM_EPOCHS=100
#20000  
WARMUP_UPDATES=500
#500     
LR=1e-5
#3e-05
MAX_TOKENS=1024
#2048
UPDATE_FREQ=1
#32
BART_PATH=/home/ec2-user/quic-efs/user/jingfe/util_files/bart.large/model.pt

CUDA_VISIBLE_DEVICES=$1 fairseq-train "${TASK}/bin-aug-large" \
    --restore-file $BART_PATH \
    --max-tokens $MAX_TOKENS \
    --task translation \
    --source-lang src_aug --target-lang tgt_aug \
    --truncate-source \
    --layernorm-embedding \
    --share-all-embeddings \
    --share-decoder-input-output-embed \
    --reset-optimizer --reset-dataloader --reset-meters \
    --required-batch-size-multiple 1 \
    --arch bart_large \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --dropout 0.1 --attention-dropout 0.1 \
    --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.999)" --adam-eps 1e-08 \
    --clip-norm 0.1 \
    --lr $LR --max-epoch $TOTAL_NUM_EPOCHS \
    --fp16 --update-freq $UPDATE_FREQ \
    --skip-invalid-size-inputs-valid-test \
    --find-unused-parameters \
    --save-dir "$TASK/bart-checkpoints$PARAM"; 


for f in $TASK/bart-checkpoints$PARAM/checkpoint*
do 
    echo '------------------------------------------------------------'
    echo $f
    CUDA_VISIBLE_DEVICES=$1 python /home/ec2-user/quic-efs/user/jingfe/sem_parses/my_code/semantic_parsing.py --model-dir $(dirname $f) --model-file $(basename $f) --src $TASK/src_aug.test --out $TASK/pred$PARAM.test --data-dir "${TASK}/bin-aug-large/" 
    python acc_deno.py -pred $TASK/pred$PARAM.test -gold $TASK/tgt_aug.test
done
