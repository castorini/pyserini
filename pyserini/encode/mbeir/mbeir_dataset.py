
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from torch.utils.data import Dataset
from PIL import Image


class MBEIRCorpusDataset(Dataset):
    def __init__(self, batch_info, img_preprocess_fn, **kwargs):
        data = []
        num_records = len(batch_info["did"])
        for i in range(num_records):
            record = {
                "did": batch_info["did"][i],
                "img_path": batch_info["img_path"][i],
                "modality": batch_info["modality"][i],
                "txt": batch_info["txt"][i],
            }
            data.append(record)
        self.data = data
        self.img_preprocess_fn = img_preprocess_fn
        self.kwargs = kwargs

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        entry = self.data[idx]
        img_path = entry.get("img_path", None)
        if img_path:
            try:
                img = Image.open(img_path).convert("RGB")
                img = self.img_preprocess_fn(img)
            except Exception:
                raise ValueError(f"Could not open image at {img_path}. Please check the file path or format.")
        else:
            img = None

        instance = {
            "did": entry["did"],
            "txt": entry.get("txt", ""),
            "img": img,
            "modality": entry["modality"],
        }
        return instance


class MBEIRQueryDataset(Dataset):
    def __init__(self, query_info, img_preprocess_fn, **kwargs):
        self.query_info = query_info
        self.img_preprocess_fn = img_preprocess_fn
        self.kwargs = kwargs

    def __len__(self):
        return len(self.query_info)

    def __getitem__(self, idx):
        entry = self.query_info[idx]

        query_img_path = entry.get("query_img_path", None)
        if not query_img_path:
            img = None
        else:
            img = Image.open(query_img_path).convert("RGB")
            img = self.img_preprocess_fn(img)

        query_txt = entry.get("query_txt", "")

        query = {"txt": query_txt, "img": img, "qid": entry["qid"]}

        instance = {  
            "query": query,  
            "qid": entry["qid"] 
        }

        return instance
