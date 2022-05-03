onmt_preprocess -train_src scan_right/src_aug.train -train_tgt scan_right/tgt_aug.train -valid_src scan_right/src.val  -valid_tgt scan_right/tgt.val -save_data scan_right/train_val_aug_copy -dynamic_dict
CUDA_VISIBLE_DEVICES=3 onmt_train -data scan_right/train_val_aug_copy -save_model model/scan_right_copy_aug/model_sgd -gpu_ranks 0 -valid_steps 300 -train_steps 9000 -save_checkpoint_steps 300 -copy_attn -global_attention mlp -word_vec_size 64 -layers 1 -encoder_type brnn -reuse_copy_attn -keep_checkpoint 50 -learning_rate=0.001 -optim adam -dropout 0.5 -batch_size 64 
for f in model/scan_right_copy_aug/model_sgd* 
do 
    echo '------------------------------------------------------------'
    echo $f
    CUDA_VISIBLE_DEVICES=4 onmt_translate -gpu 0 -model $f -src scan_right/src.test -tgt scan_right/tgt.test -replace_unk -output scan_right/pred_copy_aug.test
    python acc.py -pred scan_right/pred_copy_aug.test -gold scan_right/tgt.test
done