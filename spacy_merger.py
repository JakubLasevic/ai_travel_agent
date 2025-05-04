from spacy.matcher import Matcher
import spacy

def merge_hyphenated_tokens(doc):
    """
    Merges tokens in a spaCy Doc that are part of hyphenated words into single tokens.

    Args:
        doc (spacy.tokens.Doc): The spaCy Doc object.

    Returns:
        spacy.tokens.Doc: The Doc object with merged hyphenated tokens.
    """
    matcher = Matcher(doc.vocab)
    pattern = [
        {"IS_ALPHA": True}, # Token 1: Alphabetical character
        {"IS_PUNCT": True, "TEXT": "-"}, # Token 2: Hyphen
        {"IS_ALPHA": True}, # Token 3: Alphabetical character
    ]
    matcher.add("hyphenated", [pattern])
    matches = matcher(doc)
    spans_to_merge = []
    for match_id, start, end in matches:
        span = doc[start:end]
        spans_to_merge.append(span)

    with doc.retokenize() as retokenizer:
        for span in spans_to_merge:
            try:
                retokenizer.merge(span) 
            except ValueError:
                pass 

    return doc