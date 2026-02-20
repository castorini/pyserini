rm -r similarities
mkdir similarities
for setmode in q2c
do
for metric in weight_jaccard kl_divergence tf_filter df_filter js_divergence
do
python compare_domains.py \
    --index_path indexes \
    --output_path similarities/${setmode}-${metric}.tsv \
    --compare_sets ${setmode} \
    --compare_metric ${metric}
done
done
