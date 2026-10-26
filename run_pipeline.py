import polars as pl
from pathlib import Path

dict_path = Path(__file__).parent / "data" / "scowl" / "comp-60.txt"
modern_dict = pl.read_csv(
    dict_path,
    has_header=False,
    columns=[0],
    new_columns=["word"],
    extra_columns="ignore",
).with_columns(
    pl.col("word").str.to_lowercase().str.strip_chars()
)

modern_words_set = set(modern_dict["word"].to_list())

books_dir = Path(__file__).parent / "data" / "raw_books"

records = []
for file_path in books_dir.glob("*.txt"):
    try:
        # maxsplit=1 ensures we only split from the very last underscore
        title, year_str = file_path.stem.rsplit("_", maxsplit=1)
        year = int(year_str)
    except ValueError:
        print(f"Skipping file {file_path.name} due to unexpected filename format (Requires 'Title_Year.txt').")
        continue
    
    records.append({
        "title": title, 
        "year": year, 
        "text": file_path.read_text(encoding="utf-8")
    })

df_books = pl.DataFrame(
    records, 
    schema={"title": pl.String, "year": pl.Int64, "text": pl.String}
)


if df_books.is_empty():
    print(f"\n WARNING: No valid book files were loaded from directory: {books_dir.resolve()}")
    print("Ensure files are named like 'MyBook_1900.txt' and placed in the correct folder.\n")


results = (
    df_books
    .with_columns(
        pl.col("text")
        .str.to_lowercase()
        .str.replace_all("[þÞð]", "th", literal=False)
        .str.replace_all("[æÆ]", "e", literal=False)
        .str.replace_all(r"[^a-z\s]", "", literal=False)
        .str.strip_chars()
        .str.split(" ")
        .alias("word")
    )
    .explode("word")
    .filter(pl.col("word") != "")
    .filter(~pl.col("word").is_in(modern_words_set))
    .sort("year")
)
import polars as pl
from pathlib import Path

dict_path = Path(__file__).parent / "data" / "scowl" / "comp-60.txt"
modern_dict = pl.read_csv(
    dict_path,
    has_header=False,
    columns=[0],
    new_columns=["word"],
    extra_columns="ignore",
).with_columns(
    pl.col("word").str.to_lowercase().str.strip_chars()
)

modern_words_set = set(modern_dict["word"].to_list())

words_to_ignore = {
    "the", "and", "of", "to", "a", "in", "that", "is", "was", "he", "for", "it", "with", "as", "his", "on", "be",
    "at", "by", "this", "from", "but", "not", "or", "an", "which", "are", "were", "they", "their", "has",
    "have", "had", "will", "would", "can", "could", "should", "may", "might",
    # Old English verbs
    "eom", "eart", "is", "sint", "sindon", "syndon", "waes", "waeron", "beo", "beon", "bist", "bith",
    # Pronouns
    "ic", "me", "pu", "thu", "thee", "he", "heo", "hit", "him", "hiene", "hi", "we", "ge",
    "se", "thaet", "thaes", "thone", "tham", "tha", "thes", "this",
    # Conjunctions & Prepositions
    "ond", "thaer", "mid", "ac", "swa", "gif",
    # Auxiliaries & Past Tense
    "maeg", "sceal", "scolde", "wille", "wolde", "haefde", "dyde",
    "this", "that", "these", "those", "here", "there", "where", "when", "why", "how",
    # Common adverbs
    "so", "then", "now", "again", "ever", "never", "always", "sometimes", "often", "once",
    # Common adjectives
    "good", "bad", "big", "small", "new", "old", "young", "older", "better", "worse", "first", "last", "next", "same", "different",
    # Connective words
    "also", "even", "just", "only", "still", "yet", "more", "most", "less", "least", "many", "much", "few", "several", "all", "any", "some", "each", "every", "either", "neither",
    }
exclusion_set = modern_words_set | words_to_ignore

books_dir = Path(__file__).parent / "data" / "raw_books"

records = []
for file_path in books_dir.glob("*.txt"):
    try:
        title, year_str = file_path.stem.rsplit("_", maxsplit=1)
        year = int(year_str)
    except ValueError:
        print(f"Skipping file {file_path.name} due to unexpected filename format (Requires 'Title_Year.txt').")
        continue
    
    records.append({
        "title": title, 
        "year": year, 
        "text": file_path.read_text(encoding="utf-8")
    })


df_books = pl.DataFrame(
    records, 
    schema={"title": pl.String, "year": pl.Int64, "text": pl.String}
)


if df_books.is_empty():
    print(f"\nWARNING: No valid book files were loaded from directory: {books_dir.resolve()}")
    print("Ensure files are named like 'MyBook_1900.txt' and placed in the correct folder.\n")


results = (
    df_books
    .with_columns(
        pl.col("text")
        .str.to_lowercase()
        .str.replace_all("[þÞð]", "th", literal=False)
        .str.replace_all("[æÆ]", "e", literal=False)
        .str.replace_all(r"[^a-z\s]", "", literal=False)
        .str.strip_chars()
        .str.split(" ")
        .alias("word")
    )
    .explode("word")
    .filter(pl.col("word") != "")
    .filter(pl.col("word").is_in(exclusion_set))
    .sort("year")
)
if results.height > 0:
    winner = results[0, "word"]

    print(f"The first non-modern word found is: {winner}")
    print (f"Found in the book: {results[0, 'title']} published in {results[0, 'year']}.")
else:
    print("No non-modern words found in the provided books.")
