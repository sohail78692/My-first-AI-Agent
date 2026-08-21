from memory import remember, recall


# Save information
remember("favorite_language", "Python")

# Read information
value = recall("favorite_language")

print("Remembered:", value)