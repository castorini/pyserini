## UniCOIL with ElasticSearch
1. Setup ElasticSearch with Docker by following document [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.2.3
docker network create elastic
docker run --name es01 --net elastic -d -p 9200:9200 -p 9300:9300 \
           -e "discovery.type=single-node" \
           -e "xpack.security.enabled=false" \
           -it docker.elastic.co/elasticsearch/elasticsearch:8.2.2
```
2. (Optional) Setup Kibana by following document [here](https://www.elastic.co/guide/en/kibana/current/docker.html).
```bash
docker pull docker.elastic.co/kibana/kibana:8.2.2
docker run -d --name kib-01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.2.2
```

3. Create ES index
```bash
python create_es.py
```
This will create index based on two search field:

- `document`: contains raw text for BM25 search
- `vector`: contains pseudo text from uniCOIL for impact search

4. Create document entry for BM25 index
```bash
python index_bm25.py
```

5. Add uniCOIL encoded document for impact search
```bash
python index_unicoil_update.py
```

6. BM25 search
```bash
python search_bm25.py
```

7. uniCOIL search
```bash
python search_unicoil.py
```

8. Hybrid Search

```bash
python search_unicoil.py
```