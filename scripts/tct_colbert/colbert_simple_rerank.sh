RUNFILE=./runs/head.tsv
MODEL=../encoders/distilbert-base-uncased_colbert_rep-mask_qry-aug_cls_m-0.35_main_a49ea44_t-1
TOKENIZER=../encoders/tokenizer-distilbert-base-uncased
CMD='python scripts/tct_colbert/colbert_utils.py test_scoring'

while read line; do
    qid=`echo $line | awk '{print $1}'`
    pid=`echo $line | awk '{print $2}'`
    true_score=`echo $line | awk '{print $4}'`
    echo $qid $pid $true_score
    msmarco_utils.sh query $qid | cut -f2- > query.txt
    msmarco_utils.sh doc $pid | cut -f2- > doc.txt
    set -x
    $CMD $MODEL $TOKENIZER --visualize=False --query_augment=True \
        --query_file ./query.txt --doc_file ./doc.txt
    set +x
    break
done < $RUNFILE
