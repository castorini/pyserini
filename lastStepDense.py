import faiss
import numpy as np
from pyserini.search.faiss import FaissSearcher
from pyserini.encode import AutoQueryEncoder
from tqdm import tqdm

index = faiss.read_index('indexes/nfcorpus.bge-base-en-v1.5/index')
num_vectors = index.ntotal

#for i in range(10):
    #vector = index.reconstruct(i)
    #print(f"Vector {i}: {vector}")

docids = []
with open('indexes/nfcorpus.bge-base-en-v1.5/docid', 'r') as fin:
    docids = [line.rstrip() for line in fin.readlines()]

v1 = index.reconstruct(docids.index('MED-4555'))

# This is the string contents of doc MED-4555
doc_text = 'Analysis of risk factors for abdominal aortic aneurysm in a cohort of more than 3 million individuals. BACKGROUND: Abdominal aortic aneurysm (AAA) disease is an insidious condition with an 85% chance of death after rupture. Ultrasound screening can reduce mortality, but its use is advocated only for a limited subset of the population at risk. METHODS: We used data from a retrospective cohort of 3.1 million patients who completed a medical and lifestyle questionnaire and were evaluated by ultrasound imaging for the presence of AAA by Life Line Screening in 2003 to 2008. Risk factors associated with AAA were identified using multivariable logistic regression analysis. RESULTS: We observed a positive association with increasing years of smoking and cigarettes smoked and a negative association with smoking cessation. Excess weight was associated with increased risk, whereas exercise and consumption of nuts, vegetables, and fruits were associated with reduced risk. Blacks, Hispanics, and Asians had lower risk of AAA than whites and Native Americans. Well-known risk factors were reaffirmed, including male gender, age, family history, and cardiovascular disease. A predictive scoring system was created that identifies aneurysms more efficiently than current criteria and includes women, nonsmokers, and individuals aged <65 years. Using this model on national statistics of risk factors prevalence, we estimated 1.1 million AAAs in the United States, of which 569,000 are among women, nonsmokers, and individuals aged <65 years. CONCLUSIONS: Smoking cessation and a healthy lifestyle are associated with lower risk of AAA. We estimated that about half of the patients with AAA disease are not eligible for screening under current guidelines. We have created a high-yield screening algorithm that expands the target population for screening by including at-risk individuals not identified with existing screening criteria.'

from pyserini.encode import AutoDocumentEncoder
encoder = AutoDocumentEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)

v2 = encoder.encode(doc_text)

print(np.linalg.norm(v2[0] - v1))

#Working through a query

encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)
searcher = FaissSearcher('indexes/nfcorpus.bge-base-en-v1.5', encoder)
hits = searcher.search('How to Help Prevent Abdominal Aortic Aneurysms')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')

q_encoder = AutoQueryEncoder('BAAI/bge-base-en-v1.5', device='cpu', pooling='mean', l2_norm=True)
q_vec = q_encoder.encode('How to Help Prevent Abdominal Aortic Aneurysms')

print(q_vec)

print(np.dot(q_vec, v1))

#Retrieval by hand
scores = []
# Iterate through all document vectors and compute dot product.
#for i in tqdm(range(num_vectors)):
    #vector = index.reconstruct(i)
    #score = np.dot(q_vec, vector)
    #scores.append([docids[i], score])

# Sort by score descending.
scores.sort(key=lambda x: -x[1])

#for s in scores[:10]:
    #print(f'{s[0]} {s[1]:.6f}')