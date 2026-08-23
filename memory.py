import json
import os


MEMORY_FILE = "memory.json"


def load_memory():
    """Load all saved memories."""

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    """Save all memories."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def remember(key, value):
    """Store or update a memory."""

    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return {
        "success": True,
        "key": key,
        "value": value,
        "message": f"Remembered {key}."
    }


def recall(key):
    """Retrieve one specific memory."""

    memory = load_memory()

    if key not in memory:
        return {
            "found": False,
            "key": key,
            "message": f"No memory found for {key}."
        }

    return {
        "found": True,
        "key": key,
        "value": memory[key]
    }


def get_all_memories():
    """Return all stored memories."""

    memory = load_memory()

    return {
        "count": len(memory),
        "memories": memory
    }