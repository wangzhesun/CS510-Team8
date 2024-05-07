import nltk
from nltk.tokenize import word_tokenize

def chunk_sentence(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Define the grammar for chunking
    grammar = r"""
        NP: {<DT|JJ|NN.*>+}  # Noun Phrase
        PP: {<IN><NP>}       # Prepositional Phrase
        VP: {<VB.*><NP|PP>*} # Verb Phrase
    """

    # Create a chunk parser
    chunk_parser = nltk.RegexpParser(grammar)

    # Part-of-speech tag the words
    tagged_words = nltk.pos_tag(words)

    # Chunk the tagged words
    tree = chunk_parser.parse(tagged_words)

    # Extract phrases from the parse tree
    phrases = []
    for subtree in tree.subtrees(filter=lambda t: t.label() != 'S'):
        phrase = ' '.join([word for word, tag in subtree.leaves()])
        phrases.append(phrase)

    return phrases

# Example usage
sentence = "The quick brown fox jumps over the lazy dog."
chunked_phrases = chunk_sentence(sentence)
print(chunked_phrases)