import os
from huggingface_hub import snapshot_download
import shutil

output_dir = "collections/m-beir"
os.makedirs(output_dir, exist_ok=True)

repo_id = "TIGER-Lab/M-BEIR"

print("Downloading M-BEIR datasets...")

# Download cand_pool files
print("Downloading corpus files...")
snapshot_download(
    repo_id=repo_id,
    repo_type="dataset",
    allow_patterns="cand_pool/local/*.jsonl",
    local_dir=output_dir,
    local_dir_use_symlinks=False
)

# Download query files
print("Downloading topic files...")
snapshot_download(
    repo_id=repo_id,
    repo_type="dataset",
    allow_patterns="query/test/*.jsonl",
    local_dir=output_dir,
    local_dir_use_symlinks=False
)

# Download qrels files
print("Downloading qrel files...")
snapshot_download(
    repo_id=repo_id,
    repo_type="dataset",
    allow_patterns="qrels/test/*.txt",
    local_dir=output_dir,
    local_dir_use_symlinks=False
)

# Move files from subdirectories to main directory
print("🔄 Organizing files...")
subdirs_to_clean = [
    "cand_pool/local",
    "query/test",
    "qrels/test"
]

for subdir in subdirs_to_clean:
    full_path = os.path.join(output_dir, subdir)
    if os.path.exists(full_path):
        for file in os.listdir(full_path):
            src = os.path.join(full_path, file)
            dst = os.path.join(output_dir, file)
            shutil.move(src, dst)

        os.rmdir(full_path)
        os.rmdir(os.path.dirname(full_path))

print("✅ Download complete!")
print(f"All files are in: {output_dir}")
