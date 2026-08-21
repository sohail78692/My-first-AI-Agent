import json
import os


MEMORY_FILE = "memory.json"


def load_memory():
    """Load saved memory from memory.json."""

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    """Save memory to memory.json."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def remember(key, value):
    """Store information in persistent memory."""

    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return {
        "success": True,
        "message": f"Remembered {key}."
    }


def recall(key):
    """Retrieve information from persistent memory."""

    memory = load_memory()

    value = memory.get(key)

    if value is None:
        return {
            "found": False,
            "message": f"No memory found for {key}."
        }

    return {
        "found": True,
        "key": key,
        "value": value
    }