#
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

import os
import tarfile
import yaml
import random
import pandas as pd
from pyserini.util import download_url, get_cache_home

def get_mbeir_instructions(instruction_config: str | None, query_modality: str) -> str | None:
    def _get_instruction_config(instr_file: str = None) -> str | None:
        if instr_file is None:
            return None

        cache_dir = get_cache_home()
        instructions_dir = os.path.join(cache_dir, 'query_instructions')

        if not os.path.exists(instructions_dir):
            query_images_and_instructions_url = "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/mbeir_query_images_and_instructions.tar.gz"
            tar_path = os.path.join(cache_dir, 'mbeir_query_images_and_instructions.tar.gz')

            try:  
                download_url(query_images_and_instructions_url, cache_dir, force=False)
                with tarfile.open(tar_path, 'r:gz') as tar:
                    tar.extractall(cache_dir)
            except Exception as e:
                raise Exception(f"Could not download default instructions: {e}")

        if instr_file:
            return os.path.join(instructions_dir, instr_file)
        else:
            return None

    def _load_instruction_config(instruction_config):
        try:
            with open(instruction_config, "r") as f:
                config = yaml.safe_load(f)
            instruction_file = config.get("instruction_file", None)
            candidate_modality = config.get("candidate_modality", None)
            dataset_id = config.get("dataset_id", None)
            randomize_instructions = config.get("randomize_instructions", False)
            if instruction_file is None or candidate_modality is None or dataset_id is None:
                raise ValueError(
                    "Instruction file, candidate_modality, or dataset_id is missing in the config. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv"
                )
        except Exception as e:
            raise ValueError(f"Error loading instruction config: {e}")

        try:
            df = pd.read_csv(instruction_file, sep="\t")
            filtered = df[df["dataset_id"].astype(int) == int(dataset_id)]
            instructions = filtered.to_dict(orient="records")

            return instructions, candidate_modality, randomize_instructions
        except Exception as e:
            raise ValueError(
                f"Error reading instruction or corpus file: {e}. Please download the instruction file from https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv"
            )

    def _get_instruction_prompt(instructions, c_modality, q_modality, randomize_instructions) -> str | None:
        for instruction in instructions:
            if instruction["query_modality"] == q_modality and instruction["cand_modality"] == c_modality:
                if randomize_instructions:
                    prompts = [instruction[k] for k in instruction if k.startswith("prompt_")]
                    return random.choice(prompts) if prompts else None
                else:
                    return instruction["prompt_1"]

    instruction_config = _get_instruction_config(instr_file=instruction_config)
    if instruction_config is None:
        return None

    instructions, candidate_modality, randomize_instructions = _load_instruction_config(instruction_config)
    instruction = _get_instruction_prompt(
        instructions=instructions,
        c_modality=candidate_modality,
        q_modality=query_modality,
        randomize_instructions=randomize_instructions,
    )
    return instruction
