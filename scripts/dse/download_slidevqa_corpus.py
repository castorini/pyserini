#!/usr/bin/env python3
"""
Download SlideVQA from Hugging Face (NTT-hil-insight/SlideVQA), download slide images,
and create a corpus.jsonl file for encoding.
"""
import argparse
import json
from pathlib import Path
from typing import List, Set

from datasets import load_dataset, Image
from tqdm import tqdm


def download_corpus(all_splits_data, output_dir: Path) -> Set[str]:
    """
    Download slide images and create corpus.jsonl.
    SlideVQA stores images as page_1, page_2, ..., page_20 PIL Image objects per example.
    Not all slideshows have 20 pages - they have up to 20 pages.

    Returns:
        Set of successfully downloaded doc_ids.
    """
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = output_dir / "corpus.jsonl"

    # Track successfully downloaded doc_ids
    valid_doc_ids: Set[str] = set()

    # Collect all unique (deck_name, page_num) pairs
    seen_pages: Set[tuple] = set()

    # Check for existing progress
    existing_ids = set()
    if corpus_path.exists():
        with corpus_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    doc_id = json.loads(line)["id"]
                    existing_ids.add(doc_id)
                    # Also check if image file exists and is non-empty
                    img_path = images_dir / f"{doc_id}.jpg"
                    if img_path.exists() and img_path.stat().st_size > 0:
                        valid_doc_ids.add(doc_id)
                except Exception:
                    pass

    # Count total items for progress bar
    total_items = sum(len(split_data) for split_data in all_splits_data)

    mode = "a" if existing_ids else "w"
    downloaded = 0
    failed = 0
    processed_images = 0
    skipped_existing = 0

    with corpus_path.open(mode, encoding="utf-8") as corpus_file:
        pbar = tqdm(total=total_items, desc="Processing slideshows", unit="slideshow")
        for split_data in all_splits_data:
            for item in split_data:
                deck = item.get("deck_name")
                if deck is None:
                    pbar.update(1)
                    continue

                # Extract pages (up to page_20, but not all slideshows have all pages)
                for page_num in range(1, 21):
                    page_key = f"page_{page_num}"
                    # Check if page exists and is not None
                    if page_key not in item or item[page_key] is None:
                        continue

                    doc_id = f"{deck}_page{page_num}"
                    processed_images += 1

                    if doc_id in existing_ids:
                        # Already processed, skip (but it's already in valid_doc_ids if file exists)
                        skipped_existing += 1
                        continue

                    # Check if we've already processed this page
                    if (deck, page_num) in seen_pages:
                        continue
                    seen_pages.add((deck, page_num))

                    # Get raw image dict (cast_column with Image(decode=False) ensures this)
                    page_image = item[page_key]

                    # Save image using original JPEG bytes (no re-encoding)
                    img_path = images_dir / f"{doc_id}.jpg"
                    try:
                        if isinstance(page_image, dict) and page_image.get("bytes"):
                            # Write original bytes directly (no recompression)
                            with img_path.open("wb") as img_file:
                                img_file.write(page_image["bytes"])

                            # Verify file was written successfully
                            if img_path.exists() and img_path.stat().st_size > 0:
                                # Write corpus entry
                                entry = {"id": doc_id, "contents": str(img_path)}
                                corpus_file.write(json.dumps(entry) + "\n")
                                valid_doc_ids.add(doc_id)
                                downloaded += 1
                                pbar.set_postfix({
                                    "images": processed_images,
                                    "downloaded": downloaded,
                                    "valid": len(valid_doc_ids),
                                    "failed": failed
                                })
                            else:
                                failed += 1
                                pbar.set_postfix({
                                    "images": processed_images,
                                    "downloaded": downloaded,
                                    "valid": len(valid_doc_ids),
                                    "failed": failed
                                })
                                tqdm.write(f"Warning: Failed to save {doc_id}: file not created or empty")
                        else:
                            # If it's not a raw-bytes dict, skip (we expect decode=False)
                            failed += 1
                            pbar.set_postfix({
                                "images": processed_images,
                                "downloaded": downloaded,
                                "valid": len(valid_doc_ids),
                                "failed": failed
                            })
                            continue
                    except Exception as e:
                        failed += 1
                        pbar.set_postfix({
                            "images": processed_images,
                            "downloaded": downloaded,
                            "valid": len(valid_doc_ids),
                            "failed": failed
                        })
                        tqdm.write(f"Warning: Failed to save {doc_id}: {e}")
                        continue

                pbar.update(1)
        pbar.close()

    return valid_doc_ids


def main():
    parser = argparse.ArgumentParser(
        description="Download SlideVQA and build a corpus.jsonl of slide images for encoding."
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Output directory for generated files (corpus.jsonl and images/).",
    )
    args = parser.parse_args()

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load all splits - we need all splits to build the full corpus
    ds_train = load_dataset("NTT-hil-insight/SlideVQA", split="train")
    ds_val = load_dataset("NTT-hil-insight/SlideVQA", split="val")
    ds_test = load_dataset("NTT-hil-insight/SlideVQA", split="test")

    # Cast page_* columns to Image(decode=False) so we get raw JPEG bytes, no recompression
    def cast_pages_to_bytes(ds):
        for page_num in range(1, 21):
            col = f"page_{page_num}"
            if col in ds.features:
                ds = ds.cast_column(col, Image(decode=False))
        return ds

    ds_train_bytes = cast_pages_to_bytes(ds_train)
    ds_val_bytes = cast_pages_to_bytes(ds_val)
    ds_test_bytes = cast_pages_to_bytes(ds_test)

    all_splits = [ds_train_bytes, ds_val_bytes, ds_test_bytes]
    download_corpus(all_splits, out_dir)


if __name__ == "__main__":
    main()
