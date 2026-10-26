import polars as pl
from pathlib import Path
import re

def process_text_to_bigrams(file_path: str | Path):
    raw_text = Path(file_path).read_text(encoding="utf-8")

    text = re.sub(r"ick\b", "ic", raw_text)
    text = re.sub(r"\bft", "st", text)

    words = [w.lower() for w in re.findall(r"\b\w+\b", text)]
    if len(words) < 2:
        return pl.DataFrame({"phrase": []}, schema={"phrase": pl.String})

    phrase = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    return pl.DataFrame({"phrase": phrase}, schema={"phrase": pl.String}).unique()

SCRIPT_DIR = Path(__file__).parent

BASE_DIR = SCRIPT_DIR / "data" / "book_2"

file_18th = BASE_DIR / "book_18th.txt"
file_20th = BASE_DIR / "book_20th.txt"

book_18th = process_text_to_bigrams(file_18th)
book_20th = process_text_to_bigrams(file_20th)

shared_phrases = book_18th.join(book_20th, on="phrase", how="inner")
    
print(f"Shared common phrases count: {shared_phrases.height}")
if shared_phrases.height > 0:
    print("\nTop 5 shared phrases:")
    print(shared_phrases.head(5))