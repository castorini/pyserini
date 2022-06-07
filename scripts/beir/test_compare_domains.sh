for metric in weight_jaccard kl_divergence tf_filter df_filter
do
python compare_domains.py \
    --index_path indexes \
    --output_path indexes_${metric}.tsv \
    --compare_metric ${metric}
done
