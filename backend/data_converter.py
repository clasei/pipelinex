"""Data preparation for training"""
import json
import csv
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def jsonl_from_csv(csv_file: str, output_path: str,
                   prompt_column: str = "user",
                   completion_column: str = "ai") -> int:
    """Convert CSV to JSONL training format"""
    count = 0
    with open(csv_file, 'r', encoding='utf-8') as inf:
        reader = csv.DictReader(inf)
        with open(output_path, 'w') as outf:
            for row in reader:
                if prompt_column in row and completion_column in row:
                    outf.write(json.dumps({
                        "prompt": row[prompt_column],
                        "completion": row[completion_column]
                    }) + '\n')
                    count += 1
    logger.info(f"wrote {count} examples to {output_path}")
    return count


def validate_jsonl(file_path: str) -> Dict[str, Any]:
    """Validate JSONL file"""
    stats = {
        "total": 0,
        "valid": 0,
        "invalid": 0,
    }
    with open(file_path, 'r') as f:
        for line in f:
            stats["total"] += 1
            try:
                example = json.loads(line)
                if "prompt" in example and "completion" in example:
                    stats["valid"] += 1
                else:
                    stats["invalid"] += 1
            except:
                stats["invalid"] += 1
    return stats

