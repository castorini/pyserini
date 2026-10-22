import argparse
import numpy as np

from pyserini.index.lucene import IndexReader


def index2stats(index_path):
    index_reader = IndexReader(index_path)

    terms = index_reader.terms()

    cf_dict = {}
    df_dict = {}
    for t in terms:
        txt = t.term
        df = t.df
        cf = t.cf
        cf_dict[txt] = int(cf)
        df_dict[txt] = int(df)

    return cf_dict, df_dict, index_reader.stats() 

def count_total(d):
    s = 0
    for t in d:
        s += d[t]
    return s

def kl_divergence(d1, d2):
    value = float(0)
    for w in d1:
        if w in d2: # through out zero tokens for both sets
            value += d1[w] * np.log(d1[w] / d2[w])
    return value

def js_divergence(d1, d2):
    mean = {}
    for w in d1:
        mean[w] = d1[w] * 0.5
    for w in d2:
        if w in mean:
            mean[w] += d2[w] * 0.5
        else:
            mean[w] = d2[w] * 0.5

    jsd = 0.5 *  (kl_divergence(d1, mean) + kl_divergence(d2, mean))
    return jsd

def jaccard(d1, d2):
    ret = (float(len(set(d1).intersection(set(d2)))) / 
           float(len(set(d1).union(set(d2)))))
    return ret

def weighted_jaccard(d1, d2):
    term_union = set(d1).union(set(d2))
    min_sum = max_sum = 0
    for t in term_union:
        if t not in d1:
            max_sum += d2[t]
        elif t not in d2:
            max_sum += d1[t]
        else:
            min_sum += min(d1[t], d2[t])
            max_sum += max(d1[t], d2[t])
    ret = float(min_sum) / float(max_sum)
    return ret

def cf2freq(d):
    total = count_total(d)
    new_d = {}
    for t in d:
        new_d[t] = float(d[t]) / float(total)
    return new_d

def df2idf(d, n):
    total = n
    new_d = {}
    for t in d:
        new_d[t] = float(n) / float(d[t])
    return new_d

def filter_freq_dict(freq_d, threshold=0.0001):
    new_d = {}
    for t in freq_d:
        if freq_d[t] > threshold:
            new_d[t] = freq_d[t]
    return new_d

def print_results(datasets, results, save_file):
    f = open(save_file, 'w')

    f.write("\t{}\n".format("\t".join(datasets)))
    for d1 in datasets:
        f.write(d1)
        for d2 in datasets:
            f.write("\t{:.4f}".format(results[d1][d2]))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_path', type=str, help='path to indexes of all the beir dataset', required=True)
    parser.add_argument('--compare_metric', type=str, help='the metric for comparing two vocab, choose from: jaccard, weight_jaccard, df_filter, tf_filter, kl_divergence, js_divergence', default="weight_jaccard")
    parser.add_argument('--compare_threshold', type=float, help='when choosing df_filter, or tf_filter, you can choolse the threshold', default=0.0001)
    parser.add_argument('--output_path', type=str, help='path to save the stat results', required=True)
    parser.add_argument('--compare_sets', type=str, default="c2c", help="choose from c2c, q2q, q2c")
    args = parser.parse_args()

    corpus_format = "/corpus/lucene-index-beir-{}"
    queries_format = "/queries/lucene-index-beir-queires-{}"

    beir_datasets = ['trec-covid', 'bioasq', 'nfcorpus', 'nq', 'hotpotqa', 'climate-fever', 'fever', 'dbpedia-entity', 'fiqa', 'signal1m', 'trec-news',  'robust04', 'arguana', 'webis-touche2020', 'quora', 'cqadupstack', 'scidocs', 'scifact', 'msmarco']
    #beir_datasets = ['trec-covid', 'bioasq', 'nfcorpus', 'nq'] # Testing
    cfs = {}
    dfs = {}
    summary = {}
    cfs2 = {}
    dfs2 = {}
    summary2 = {}
    if args.compare_sets == "c2c":
        for d in beir_datasets:
            cf, df, stat = index2stats(args.index_path + corpus_format.format(d))
            cfs[d] = cf # count frequency -- int
            dfs[d] = df # document frequency -- int
            summary[d] = stat
#            stats[d] = stat
        cfs2 = cfs
        dfs2 = dfs
        summary2 = summary
    elif args.compare_sets == "q2q":
        for d in beir_datasets:
            cf, df, stat = index2stats(args.index_path + queries_format.format(d))
            cfs[d] = cf
            dfs[d] = df
            summary[d] = stat
        cfs2 = cfs
        dfs2 = dfs
        dfs2 = dfs
        summary2 = summary
    elif args.compare_sets == "q2c":
        for d in beir_datasets:
            cf, df, stat = index2stats(args.index_path + queries_format.format(d))
            cfs[d] = cf
            dfs[d] = df
            summary[d] = stat
        for d in beir_datasets:
            cf, df, stat = index2stats(args.index_path + corpus_format.format(d))
            cfs2[d] = cf
            dfs2[d] = df
            summary2[d] = stat
    else:
        NotImplementedError("--compare_sets {}".format(args.compare_sets))


    results = {}
    for d1 in beir_datasets:
        metric_d1 = {}
        for d2 in beir_datasets:
            if args.compare_metric == "jaccard":
                metric_d1[d2] = jaccard(cfs[d1], cfs2[d2])
            elif args.compare_metric == "weight_jaccard":
                new_d1 = cf2freq(cfs[d1])
                new_d2 = cf2freq(cfs2[d2])
                metric_d1[d2] = weighted_jaccard(new_d1, new_d2)
            elif args.compare_metric == "df_filter":
                new_d1 = filter_freq_dict(cf2freq(cfs[d1]))
                new_d2 = filter_freq_dict(cf2freq(cfs2[d2]))
                metric_d1[d2] = jaccard(new_d1, new_d2)
            elif args.compare_metric == "tf_filter":
                new_d1 = filter_freq_dict(df2idf(dfs[d1], summary[d1]["documents"]))
                new_d2 = filter_freq_dict(df2idf(dfs2[d2], summary2[d2]["documents"]))
                metric_d1[d2] = jaccard(new_d1, new_d2)
            elif args.compare_metric == "kl_divergence":
                new_d1 = filter_freq_dict(cf2freq(cfs[d1]))
                new_d2 = filter_freq_dict(cf2freq(cfs2[d2]))
                metric_d1[d2] = kl_divergence(new_d1, new_d2)
            elif args.compare_metric == "js_divergence":
                new_d1 = filter_freq_dict(cf2freq(cfs[d1]))
                new_d2 = filter_freq_dict(cf2freq(cfs2[d2]))
                metric_d1[d2] = js_divergence(new_d1, new_d2)
            else:
                raise NotImplementedError
        results[d1] = metric_d1

    print_results(beir_datasets, results, args.output_path)








