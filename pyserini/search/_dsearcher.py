from typing import List


class SimpleDenseSearcher:
    """Simple Searcher for dense representation

    Parameters
    ----------
    index_dir : str
        Path to faiss index directory.
    """

    def __init__(self, index_dir: str):
        pass

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        SimpleDenseSearcher
            Searcher built from the prebuilt faiss index.
        """
        pass

    def search(self, q: str, k: int = 10) -> List[str]:
        """Search the collection.

        Parameters
        ----------
        q : str
            Query string
        k : int
            Number of hits to return.
        Returns
        -------
        List[FaissSearcherResult]
            List of search results.
        """
        pass
