# Does Cohere Deliver a 3X Better MIRACL?

_Monday, January 16, 2023_

tl;dr &mdash; doesn't appear so... but Cohere's multilingual embeddings nevertheless yield impressive quality improvements.

On December 12, 2022, Cohere made a [splashy product announcement](https://twitter.com/CohereAI/status/1602343694010646529) about multilingual text understanding model support for 100+ languages, which claims to deliver "3X better performance than existing open-source models".
We read this with excitement, "Wow 3X!"

Wait, but 3X better what?
Does performance refer to quality? Latency? Throughput? Memory usage?
When [questioned about this](https://twitter.com/awadallah/status/1602537786111758336), it didn't seem like one of the co-founders [even understood the question](https://twitter.com/nickfrosst/status/1602538610728763392), at least initially.
Regardless, as Carl Sagan famously noted, "extraordinary claims require extraordinary evidence".
This led us to dig a bit deeper...

Based on Cohere's [blog post](https://txt.cohere.ai/multilingual/), they claimed to have "extensively benchmarked [their] new model... across a wide range of applications, domains and languages".
Among other datasets:

> We benchmarked on two datasets from BEIR, 10 datasets from Mr. Tydi, and 14 datasets from MIRACL. The benchmark consists of 16 languages from various language families and alphabets: Arabic, Bengali, Finnish, French, German, Hindi, Indonesian, Japanese, Korean, Persian, Russian, Spanish, Swahili, Telugu, Thai, and Vietnamese. All of these benchmarks have been created by native speakers on original text.

Hey, that's awesome!
We're the team behind the MIRACL dataset, which is a collaboration between the University of Waterloo and Huawei Noah's Ark Lab, so it's great that others are using our resources.

[MIRACL](http://miracl.ai) 🌍🙌🌏 (Multilingual Information Retrieval Across a Continuum of Languages) is an [WSDM 2023 Cup challenge](https://www.wsdm-conference.org/2023/program/wsdm-cup) that focuses on search across 18 different languages, which collectively encompass over three billion native speakers around the world.
The dataset is part of a competition with a [leaderboard](https://eval.ai/web/challenges/challenge-page/1881/overview).

Here's the graph that Cohere showed in their blog post:

![Performance Graph from Cohere Blog Post](https://txt.cohere.ai/content/images/size/w1600/2022/12/Cohere_Multilingual_Benchmark_Chart_v4.jpg)

(Let's set aside the fact that the bar chart does not have _y_ axis labels, which is a mistake for which faculty often chide their undergraduate students...)

Anyway, the results led to some head scratching... for example, what about a BM25 baseline?
Or an mDPR baseline that was explored by [Asai et al. (2021)](https://aclanthology.org/2021.naacl-main.46/) and later studied by [Zhang et al. (2022)](https://arxiv.org/abs/2204.02363)?
In typical social media banter, we [prodded](https://twitter.com/lintool/status/1602399696261111808) Cohere to actually participate in our leaderboard and have their models evaluated in a fair manner, exactly the same as everyone else in the community.
The "known-languages track" comprises 16 languages, and Cohere said they evaluated on 14 of those... so should be easy, right?
We [prodded](https://twitter.com/lintool/status/1602642255415754753), [prodded some more](https://twitter.com/nandan__thakur/status/1602459567904165888), and even [offered to help](https://twitter.com/lintool/status/1603564040982241281)!

There wasn't much of a response from Cohere, which perplexed us.
Our position is simple: Anyone (researchers, companies, etc.) making claims about the effectiveness of their models in the context of a community benchmark should [back up their claims](https://twitter.com/lintool/status/1602423757573963778).
We think this position is quite reasonable, especially since one of the researchers behind Cohere's multilingual models [took OpenAI to task](https://twitter.com/Nils_Reimers/status/1487014195568775173) about GPT-3 embeddings in January 2022.
So, [we issued a challenge](https://twitter.com/lintool/status/1603401397789237251) to Cohere: either they should formally submit a run to our leaderboard, or we'll do it for them.
To be clear, that latter means that we would use their commercially available product to conduct an evaluation on a community benchmark.
Actually, that's not unlike the experience of a customer who might be evaluating Cohere's model for a multilingual search application!

Having received no further response from Cohere, we did exactly that, the results of which are posted on the [official MIRACL leaderboard](https://eval.ai/web/challenges/challenge-page/1881/leaderboard/4427) on January 16, 2023.
We started with the official baseline BM25 results and applied embeddings from Cohere's `multilingual-22-12` model for reranking the top 100 hits, following [their instructions](https://txt.cohere.ai/multilingual/).
The submitted run is named "Cohere API (BM25-rerank)", which achieves an average nDCG@10 of **0.544** across 16 languages on the dev set, for the known-languages condition.
For reference, the BM25 baseline achieve 0.393 nDCG@10, so Cohere's multilingual embeddings were able to improve the baseline by an impressive 38%.
Not 3X, but that _does_ deserve a "wow"!
(Those of you who've worked in this space know that BM25 is a _tough_ baseline.)
For additional context, the mDPR dense retrieval model, which is another MIRACL baseline described [in the dataset overview paper](https://arxiv.org/abs/2210.09984), achieves an nDCG@10 score of 0.415 under the same setting.
Cohere improves over mDPR by a respectable 31%.
Note that both BM25 and mDPR can be characterized as "zero shot", since the mDPR model was trained on an entirely different dataset (MS MARCO).
The results can be summarized as follows:

| Method   | Avg nDCG@10 |
| -------- | ----------- |
| BM25     |   0.393     |
| mDPR     |   0.415     |
| Cohere   |   0.544     | 

Beyond effectiveness, we found the Cohere API quite easy to use and our implementation quite straightforward.
So kudos on the developer experience!

A bit more detail about our evaluation setup:
To be clear, we reranked the top-100 BM25 hits, which is a different evaluation approach than encoding the entire corpus and performing top-_k_ nearest-neighbor search.
However, we justify this approach in a few ways:

+ Reranking is far more computationally efficient than encoding the entire corpus. For MIRACL, this would have meant 16 separate corpora. We feel that our approach is actually quite realistic from the "customer perspective": reranking is an easy way to "kick the tires" on a product, to be able to get a sense of the result quality at relatively low cost.
+ Reranking gives results roughly in the same ballpark as top-_k_ nearest-neighbor search on the entire corpus, we feel, at least for the metric under consideration. Here, we are reranking the top 100 hits, and nDCG@10 considers only the top 10 hits. We have been playing with embeddings from OpenAI also, and with reranking top-100 BM25 results, we are able to replicate nDCG@10 numbers quite close to those reported in their papers. So we have some confidence about the veracity of these results. Once again, from the "customer perspective", reranking top 100 to get better top 10 seems like a realistic setup.

So, to circle all the way back to the beginning with Cohere's boasts of being able to deliver "3X better performance": in terms of nDCG@10 on the 16 languages in MIRACL on the dev set for the known languages condition, we were unable to reproduce anywhere close to the claimed gains, but our observed gains are quite impressive and real.

We're working on a paper that examines the effectiveness of public, commercially available "embedding services" (beyond Cohere, including OpenAI and others as well).
Included with the paper will be source code to reproduce all our experiments.
Unfortunately, there's this pesky publication embargo in the community... and it doesn't appear like we're going to be able to push out our code in time.
Nevertheless, we wanted to share this result (and explain the MIRACL leaderboard entry) before the gag order associated with the embargo period kicks in.
As to not violate these rules, we are unable to further comment publicly on these experiments for a few months (e.g., on social media).
However, if you wish to discuss these results with us in private, please directly reach out.

\- The MIRACL Team
