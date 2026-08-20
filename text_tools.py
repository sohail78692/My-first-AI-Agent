def analyze_text(text):
    words = text.split()
    characters = len(text)

    return {
        "word_count": len(words),
        "character_count": characters
    }