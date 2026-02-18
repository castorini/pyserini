# Pyserini: Performance Comparison of Python versus Java  RM3 and Rocchio Implementations  

We fully re-implmented the RM3 and Rocchio implementations from Anserini in Python. Below is a comparison of the performance of RM3 and Rocchio in Python versus in Java. 

For example, to run RM3 in Python over TREC DL21, 

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage \
  --topics dl21 \
  --output run.msmarco-v2-passage.bm25-rm3-default.dl21.txt \
  --bm25 --rm3-py
```

Rocchio follows similar style:

```
python -m pyserini.search.lucene \
  --threads 16 --batch-size 128 \
  --index msmarco-v2-passage \
  --topics dl21 \
  --output run.msmarco-v2-passage.bm25-rm3-default.dl21.txt \
  --bm25 --rocchio-py
```

## Performance Comparison

For this experiment, there were the computer specs:

-  OS: Windows 11 (x64), WSL
- Machine: Intel NUC11PHi7
- CPU: 11th Gen Intel Core i7
- RAM: 16 GB

### Effectiveness Comparison

<table align="center" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th rowspan="2" style="border-bottom: 1px solid #ddd; padding: 8px;">Implementation</th>
      <th colspan="3" align="center" style="border-bottom: 1px solid #ddd; border-right: 2px solid #444; padding: 8px;">RM3</th>
      <th colspan="3" align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">Rocchio</th>
    </tr>
    <tr>
      <th align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">MAP</th>
      <th align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">nDCG@10</th>
      <th align="center" style="border-bottom: 1px solid #ddd; border-right: 2px solid #444; padding: 8px;">Recall@1000</th>
      <th align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">MAP</th>
      <th align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">nDCG@10</th>
      <th align="center" style="border-bottom: 1px solid #ddd; padding: 8px;">Recall@1000</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #f6f8fa;">
      <td colspan="7" align="center" style="padding: 8px;"><b>TREC DL19</b></td>
    </tr>
    <tr>
      <td style="padding: 8px;">Python</td>
      <td align="center">0.3420</td>
      <td align="center">0.5216</td>
      <td align="center" style="border-right: 2px solid #444;">0.8136</td>
      <td align="center">0.3476</td>
      <td align="center">0.5275</td>
      <td align="center">0.8007</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Java</td>
      <td align="center">0.3416</td>
      <td align="center">0.5216</td>
      <td align="center" style="border-right: 2px solid #444;">0.8136</td>
      <td align="center">0.3474</td>
      <td align="center">0.5275</td>
      <td align="center">0.8007</td>
    </tr>
    <tr style="background-color: #f6f8fa;">
      <td colspan="7" align="center" style="padding: 8px;"><b>TREC DL20</b></td>
    </tr>
    <tr>
      <td style="padding: 8px;">Python</td>
      <td align="center">0.3010</td>
      <td align="center">0.4896</td>
      <td align="center" style="border-right: 2px solid #444;">0.8236</td>
      <td align="center">0.3118</td>
      <td align="center">0.4887</td>
      <td align="center">0.8156</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Java</td>
      <td align="center">0.3006</td>
      <td align="center">0.4896</td>
      <td align="center" style="border-right: 2px solid #444;">0.8236</td>
      <td align="center">0.3115</td>
      <td align="center">0.4910</td>
      <td align="center">0.8156</td>
    </tr>
    <tr style="background-color: #f6f8fa;">
      <td colspan="7" align="center" style="padding: 8px;"><b>TREC DL21</b></td>
    </tr>
    <tr>
      <td style="padding: 8px;">Python</td>
      <td align="center">0.2115</td>
      <td align="center">0.4454</td>
      <td align="center" style="border-right: 2px solid #444;">0.6618</td>
      <td align="center">0.2153</td>
      <td align="center">0.4550</td>
      <td align="center">0.6709</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Java</td>
      <td align="center">0.2115</td>
      <td align="center">0.4455</td>
      <td align="center" style="border-right: 2px solid #444;">0.6616</td>
      <td align="center">0.2152</td>
      <td align="center">0.4546</td>
      <td align="center">0.6709</td>
    </tr>
    <tr style="background-color: #f6f8fa;">
      <td colspan="7" align="center" style="padding: 8px;"><b>TREC DL22</b></td>
    </tr>
    <tr>
      <td style="padding: 8px;">Python</td>
      <td align="center">0.0446</td>
      <td align="center">0.2683</td>
      <td align="center" style="border-right: 2px solid #444;">0.3559</td>
      <td align="center">0.0478</td>
      <td align="center">0.2755</td>
      <td align="center">0.3637</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Java</td>
      <td align="center">0.0446</td>
      <td align="center">0.2686</td>
      <td align="center" style="border-right: 2px solid #444;">0.3559</td>
      <td align="center">0.0475</td>
      <td align="center">0.2743</td>
      <td align="center">0.3639</td>
    </tr>
    <tr style="background-color: #f6f8fa;">
      <td colspan="7" align="center" style="padding: 8px;"><b>TREC DL23</b></td>
    </tr>
    <tr>
      <td style="padding: 8px;">Python</td>
      <td align="center">0.0968</td>
      <td align="center">0.2602</td>
      <td align="center" style="border-right: 2px solid #444;">0.4745</td>
      <td align="center">0.0968</td>
      <td align="center">0.2626</td>
      <td align="center">0.4788</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Java</td>
      <td align="center">0.0969</td>
      <td align="center">0.2602</td>
      <td align="center" style="border-right: 2px solid #444;">0.4748</td>
      <td align="center">0.0970</td>
      <td align="center">0.2653</td>
      <td align="center">0.4810</td>
    </tr>
  </tbody>
</table>


### Latency Differences: Python versus Java

<table align="center">
  <thead>
    <tr>
      <th rowspan="2">Dataset</th>
      <th colspan="3" align="center">RM3</th>
      <th colspan="3" align="center">Rocchio</th>
    </tr>
    <tr>
      <th>Python</th>
      <th>Java</th>
      <th>Diff</th>
      <th>Python</th>
      <th>Java</th>
      <th>Diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>TREC DL19</b></td>
      <td>3.67</td>
      <td>2.30</td>
      <td>1.37</td>
      <td>4.14</td>
      <td>3.15</td>
      <td>0.99</td>
    </tr>
    <tr>
      <td><b>TREC DL20</b></td>
      <td>13.81</td>
      <td>11.67</td>
      <td>2.14</td>
      <td>19.51</td>
      <td>15.84</td>
      <td>3.67</td>
    </tr>
    <tr>
      <td><b>TREC DL21</b></td>
      <td>2338.80</td>
      <td>3293.97</td>
      <td>-955.17</td>
      <td>4637.96</td>
      <td>4735.69</td>
      <td>-97.73</td>
    </tr>
    <tr>
      <td><b>TREC DL22</b></td>
      <td>1282.89</td>
      <td>1503.62</td>
      <td>-220.73</td>
      <td>1944.76</td>
      <td>2042.32</td>
      <td>-97.56</td>
    </tr>
    <tr>
      <td><b>TREC DL23</b></td>
      <td>2112.62</td>
      <td>2758.77</td>
      <td>-646.15</td>
      <td>4002.54</td>
      <td>3445.50</td>
      <td>557.04</td>
    </tr>
  </tbody>
</table>
