onmt_preprocess -train_src data/src.train -train_tgt data/tgt.train -valid_src data/src.val  -valid_tgt data/tgt.val -save_data data/train_val_copy -dynamic_dict
CUDA_VISIBLE_DEVICES=3 onmt_train -data data/train_val_copy -save_model model/new_question_logic_copy/model_sgd -gpu_ranks 0 -valid_steps 600 -train_steps 18000 -save_checkpoint_steps 600 -copy_attn -global_attention mlp -word_vec_size 64 -layers 1 -encoder_type brnn -reuse_copy_attn -keep_checkpoint 50 -learning_rate=0.001 -optim adam -dropout 0.5 -batch_size 1
for f in model/new_question_logic_copy/model_sgd* 
do 
    echo '------------------------------------------------------------'
    echo $f
    CUDA_VISIBLE_DEVICES=4 onmt_translate -gpu 0 -model $f -src data/src.test -tgt data/tgt.test -replace_unk -output data/pred_copy.test
    python acc.py -pred data/pred_copy.test -gold data/tgt.test
done