TASK=geo_subs_comp_data
onmt_preprocess -train_src $TASK/src_aug.train -train_tgt $TASK/tgt_aug.train -valid_src $TASK/src.val  -valid_tgt $TASK/tgt.val -save_data $TASK/train_val_aug_copy -dynamic_dict
CUDA_VISIBLE_DEVICES=3 onmt_train -data $TASK/train_val_aug_copy -save_model $TASK/new_query_logic_copy_aug_induce2/model_sgd -gpu_ranks 0 -valid_steps 500 -train_steps 15000 -save_checkpoint_steps 500 -copy_attn -global_attention mlp -word_vec_size 64 -layers 1 -encoder_type brnn -reuse_copy_attn -keep_checkpoint 50 -learning_rate=0.001 -optim adam -dropout 0.5 -batch_size 64
for f in $TASK/new_query_logic_copy_aug_induce2/model_sgd* 
do 
    echo '------------------------------------------------------------'
    echo $f
    CUDA_VISIBLE_DEVICES=4 onmt_translate -gpu 0 -model $f -src $TASK/src.test -tgt $TASK/tgt.test -replace_unk -output $TASK/pred_copy_aug_induce.test
    python acc.py -pred $TASK/pred_copy_aug_induce.test -gold $TASK/tgt.test
done