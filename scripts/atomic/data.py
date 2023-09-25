import json
from collections import defaultdict
from datasets import Dataset, load_dataset
from tqdm.auto import tqdm
from pathlib import Path

class AtomicDataset(Dataset):
    def __init__(
        self,
        data_name_or_path="TREC-AToMiC/AToMiC-Images-v0.2",
        cache_file_path=None,
        id_column="image_id",
        qrel_name_or_path=None,
    ):
        dataset = load_dataset(data_name_or_path, split="train")
        super().__init__(dataset._data)

        if cache_file_path:
            self.cache_file_path = cache_file_path
        else:
            # set default cache directory as .cache/
            self.cache_file_path = Path(Path().resolve(), ".cache", f"{id_column}.row-index.json")

        if not self.cache_file_path.parent.exists():
            self.cache_file_path.parent.mkdir(parents=True)

        self.id_index_dict = self._get_info_dict(id_column)

        self.split_dict = None
        if qrel_name_or_path:
            self.cache_split_path = Path(Path().resolve(), ".cache", f"{id_column}.split.json")
            qrels = load_dataset(qrel_name_or_path)
            self.split_dict = self._get_split_dict(qrels, id_column)

    def _get_info_dict(self, id_column):

        if self.cache_file_path.exists():
            with open(self.cache_file_path, "r") as f:
                return json.load(f)
        else:
            id_index_dict = {
                row: index
                for index, row in tqdm(
                    enumerate(self[id_column]),
                    total=len(self),
                    desc="build id2row dict",
                )
            }
            with open(self.cache_file_path, "w") as f:
                json.dump(id_index_dict, f)
            return id_index_dict

    def _get_split_dict(self, qrels, id_column):
        if self.cache_split_path.exists():
            with open(self.cache_split_path, "r") as f:
                return json.load(f)
        else:
            train = set(qrels["train"][id_column])
            validation = set(qrels["validation"][id_column])
            test = set(qrels["test"][id_column])
            split_dict = defaultdict(list)
            for index, row in tqdm(
                enumerate(self[id_column]), total=len(self), desc="build split dict"
            ):
                if row in train:
                    split_dict["train"].append(index)
                elif row in validation:
                    split_dict["validation"].append(index)
                elif row in test:
                    split_dict["test"].append(index)
                else:
                    split_dict["other"].append(index)

            with open(self.cache_split_path, "w") as f:
                json.dump(split_dict, f)
            return split_dict

    def get_data_by_id(self, example_id):
        row_index = self.id_index_dict[example_id]
        return self[row_index]

    def get_split(self, split):
        if not self.split_dict:
            raise ValueError
        else:
            return self.select(self.split_dict[split])