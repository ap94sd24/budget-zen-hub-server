def extract_hashtags(text, trends):
    """
    Extract hashtags from a given text string and return them as a list.

    Args:
    text (str): The text from which to extract hashtags.

    Returns:
    list: A list of extracted hashtags without the '#' character.
    """
    for word in text.split():
        if word.startswith("#"):
            trends.append(word[1:])  # Exclude the '#' character
    print(trends)
    return trends
