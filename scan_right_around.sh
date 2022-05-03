onmt_preprocess -train_src scan_right_around/src.train -train_tgt scan_right_around/tgt.train -valid_src scan_right_around/src.val  -valid_tgt scan_right_around/tgt.val -save_data scan_right_around/train_val_copy -dynamic_dict
CUDA_VISIBLE_DEVICES=3 onmt_train -data scan_right_around/train_val_copy -save_model model/scan_right_around_copy/model_sgd -gpu_ranks 0 -valid_steps 200 -train_steps 6000 -save_checkpoint_steps 200 -copy_attn -global_attention mlp -word_vec_size 64 -layers 1 -encoder_type brnn -reuse_copy_attn -keep_checkpoint 50 -learning_rate=0.001 -optim adam -dropout 0.5 -batch_size 64 
for f in model/scan_right_around_copy/model_sgd* 
do 
    echo '------------------------------------------------------------'
    echo $f
    CUDA_VISIBLE_DEVICES=4 onmt_translate -gpu 0 -model $f -src scan_right_around/src.test -tgt scan_right_around/tgt.test -replace_unk -output scan_right_around/pred_copy.test
    python acc.py -pred scan_right_around/pred_copy.test -gold scan_right_around/tgt.test
done