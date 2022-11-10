# Pyserini Known Issues (v0.19.0)

+ Index statistics for new Lucene 9 indexes are invalid. Thus, `validate_prebuilt_index` on an `IndexReader` will fail. See [#1334](https://github.com/castorini/pyserini/issues/1334).
