def extract_hashtags(text):
    """
    Extract hashtags from a given text string and return them as a list.

    Args:
    text (str): The text from which to extract hashtags.

    Returns:
    list: A list of extracted hashtags without the '#' character.
    """
    hashtags = []
    for word in text.split():
        if word.startswith("#"):
            hashtags.append(word[1:])  # Exclude the '#' character
    return hashtags
