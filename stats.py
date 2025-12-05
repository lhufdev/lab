def get_book_word_count(book_text: str) -> int:
    return len(book_text.split())


def get_book_character_count(book_text: str) -> dict[str, int]:
    character_counts = {}
    for ch in book_text.lower():
        if ch not in character_counts:
            character_counts[ch] = 1
        else:
            character_counts[ch] += 1
    return character_counts


def get_sorted_character_counts(character_counts: dict[str, int]) -> list[dict]:
    character_counts_list = [
        {"char": ch, "num": count} for ch, count in character_counts.items()
    ]

    character_counts_list.sort(reverse=True, key=get_num_key)
    return character_counts_list


def get_num_key(item):
    return item["num"]
