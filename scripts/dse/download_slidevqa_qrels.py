#!/usr/bin/env python3
"""
Download SlideVQA from Hugging Face (NTT-hil-insight/SlideVQA) and
generate TREC-style qrels from its annotations, plus download slide images
and create a corpus.jsonl file for encoding.
"""
import argparse
import json
from pathlib import Path
from typing import List, Set, Tuple

from datasets import load_dataset, Image
from tqdm import tqdm


def generate_qrels(split_data, output_path: Path, valid_doc_ids: Set[str] = None) -> Tuple[int, Set[str]]:
    """
    Write qrels lines: <qid> 0 <docid> <rel>
    docid format: <deck_name>_page<page_number>
    relevance is 1 for each evidence page.
    
    Args:
        split_data: Dataset split to process
        output_path: Path to write qrels file
        valid_doc_ids: Set of doc_ids that successfully downloaded (for pruning)
    
    Returns:
        Tuple of (number of qrels lines written, set of qids with at least one valid evidence slide)
    """
    if valid_doc_ids is None:
        valid_doc_ids = set()
    
    lines: List[str] = []
    qids_with_valid_evidence: Set[str] = set()
    
    total_questions = len(split_data)
    pbar = tqdm(total=total_questions, desc="Generating qrels", unit="question")
    
    for qa in split_data:
        # HF SlideVQA usually exposes:
        # - "qa_id"
        # - "deck_name" or similar document identifier
        # - "evidence_pages" (1-based page indices)
        qid = qa.get("qa_id") or qa.get("id")
        deck = qa.get("deck_name") or qa.get("doc_id") or qa.get("deck")
        evidence_pages = qa.get("evidence_pages") or qa.get("evidence") or []
        if qid is None or deck is None or not evidence_pages:
            pbar.update(1)
            continue
        
        # Track if this question has at least one valid evidence slide
        has_valid_evidence = False
        
        for page_num in evidence_pages:
            doc_id = f"{deck}_page{page_num}"
            # Only include qrels for slides that successfully downloaded
            if doc_id in valid_doc_ids:
                lines.append(f"{qid} 0 {doc_id} 1")
                has_valid_evidence = True
        
        # Only keep questions that have at least one valid evidence slide
        if has_valid_evidence:
            qids_with_valid_evidence.add(qid)
        
        pbar.set_postfix({
            "valid_qids": len(qids_with_valid_evidence),
            "qrels_lines": len(lines)
        })
        pbar.update(1)
    
    pbar.close()
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return len(lines), qids_with_valid_evidence


def write_queries(split_data, output_path: Path, valid_qids: Set[str] = None) -> int:
    """
    Write queries in TSV (trec-style): <qid>\\t<query_text>
    
    Args:
        split_data: Dataset split to process
        output_path: Path to write queries file
        valid_qids: Set of qids that have at least one valid evidence slide (for pruning)
    
    Returns:
        Number of queries written
    """
    if valid_qids is None:
        valid_qids = set()
    
    count = 0
    total_questions = len(split_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pbar = tqdm(total=total_questions, desc="Writing queries", unit="question")
    with output_path.open("w", encoding="utf-8") as f:
        for qa in split_data:
            qid = qa.get("qa_id") or qa.get("id")
            query = qa.get("question") or qa.get("query") or qa.get("text")
            if qid is None or query is None:
                pbar.update(1)
                continue
            # Only write queries for questions with valid evidence slides
            if valid_qids and qid not in valid_qids:
                pbar.update(1)
                continue
            f.write(f"{qid}\t{query}\n")
            count += 1
            pbar.set_postfix({"written": count})
            pbar.update(1)
    pbar.close()
    return count


def download_corpus(all_splits_data, output_dir: Path) -> Set[str]:
    """
    Download slide images and create corpus.jsonl.
    SlideVQA stores images as page_1, page_2, ..., page_20 PIL Image objects per example.
    Not all slideshows have 20 pages - they have up to 20 pages.
    
    Returns:
        Set of successfully downloaded doc_ids (for pruning qrels/queries)
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
                except:
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
        description="Download SlideVQA and generate TREC-style qrels, queries, and corpus. "
                    "Applies DSE preprocessing: removes broken slides and drops questions without valid evidence."
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        type=Path,
        help="Output directory for generated files (uses test split for qrels/queries).",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip downloading images and corpus generation.",
    )
    args = parser.parse_args()

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load all splits - we need all splits to build the full corpus
    ds_train = load_dataset("NTT-hil-insight/SlideVQA", split="train")
    ds_val = load_dataset("NTT-hil-insight/SlideVQA", split="val")
    ds_test = load_dataset("NTT-hil-insight/SlideVQA", split="test")

    # Download images and create corpus.jsonl first (to identify valid slides)
    valid_doc_ids: Set[str] = set()
    if not args.skip_images:
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
        valid_doc_ids = download_corpus(all_splits, out_dir)
    else:
        # If skipping images, try to load valid_doc_ids from existing corpus
        corpus_path = out_dir / "corpus.jsonl"
        images_dir = out_dir / "images"
        if corpus_path.exists() and images_dir.exists():
            for line in corpus_path.open("r", encoding="utf-8"):
                try:
                    doc_id = json.loads(line)["id"]
                    img_path = images_dir / f"{doc_id}.jpg"
                    if img_path.exists() and img_path.stat().st_size > 0:
                        valid_doc_ids.add(doc_id)
                except:
                    pass

    # Generate filtered qrels and queries (only for test split)
    split_name = "test"
    qrels_path = out_dir / f"qrels.slidevqa.{split_name}.txt"
    wrote_qrels, valid_qids = generate_qrels(ds_test, qrels_path, valid_doc_ids)

    queries_path = out_dir / f"queries.slidevqa.{split_name}.tsv"
    wrote_queries = write_queries(ds_test, queries_path, valid_qids)


if __name__ == "__main__":
    main()
