python recomb_org.py -comp geo_subs_iid_orig_ -train datasets/geo/funql/train_spans.json -dev datasets/geo/funql/dev_spans.json -test datasets/geo/funql/test_spans.json
python recomb_org.py -comp geo_subs_comp_orig_ -train datasets/geo/funql/train_template_spans.json -dev datasets/geo/funql/dev_template_spans.json -test datasets/geo/funql/test_template_spans.json
python recomb_org.py -comp geo_subs_len_orig_ -train datasets/geo/funql/train_len_spans.json -dev datasets/geo/funql/dev_len_spans.json -test datasets/geo/funql/test_len_spans.json

python recomb_induce_check.py -train induced/train_iid.json -all_train datasets/geo/funql/train.json
python recomb_induce_check.py -train induced/train_template.json -all_train datasets/geo/funql/train_template.json
python recomb_induce_check.py -train induced/train_len.json -all_train datasets/geo/funql/train_len.json
python recomb_induce.py -comp geo_subs_iid_ -train induced/train_iid.json -dev datasets/geo/funql/dev_spans.json -test datasets/geo/funql/test_spans.json
python recomb_induce.py -comp geo_subs_comp_ -train induced/train_template.json -dev datasets/geo/funql/dev_template_spans.json -test datasets/geo/funql/test_template_spans.json
python recomb_induce.py -comp geo_subs_len_ -train induced/train_len.json -dev datasets/geo/funql/dev_len_spans.json -test datasets/geo/funql/test_len_spans.json

#python filter_example.py -no_dup_train datasets/geo/funql/question-no-dup.train -train datasets/geo/funql/train_spans.json -out datasets/geo/funql/train_150_spans.json
python filter_example.py -no_dup_train datasets/geo/funql/query-no-dup.train -train datasets/geo/funql/train_template_spans.json -out datasets/geo/funql/train_template_200_spans.json -num 200
python filter_example.py -no_dup_train datasets/geo/funql/query-no-dup.train -train datasets/geo/funql/train_template_spans.json -out datasets/geo/funql/train_template_100_spans.json -num 100
python filter_example.py -no_dup_train datasets/geo/funql/query-no-dup.train -train datasets/geo/funql/train_template_spans.json -out datasets/geo/funql/train_template_50_spans.json -num 50
python recomb_org.py -comp geo_subs_comp_200_orig_ -train datasets/geo/funql/train_template_200_spans.json -dev datasets/geo/funql/dev_template_spans.json -test datasets/geo/funql/test_template_spans.json
python recomb_org.py -comp geo_subs_comp_100_orig_ -train datasets/geo/funql/train_template_100_spans.json -dev datasets/geo/funql/dev_template_spans.json -test datasets/geo/funql/test_template_spans.json
python recomb_org.py -comp geo_subs_comp_50_orig_ -train datasets/geo/funql/train_template_50_spans.json -dev datasets/geo/funql/dev_template_spans.json -test datasets/geo/funql/test_template_spans.json

