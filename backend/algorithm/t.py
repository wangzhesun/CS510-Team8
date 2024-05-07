import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Define a function to check if a phrase is meaningful
# def is_meaningful(phrase):
#     words = nltk.word_tokenize(phrase)
#     if len(words) >= 1 and not any(word in stop_words for word in words):
#         return True
#     return False

# Define a function to check if a phrase is meaningful
def is_meaningful(phrase):
    words = nltk.word_tokenize(phrase)
    pos_tags = nltk.pos_tag(words)
    
    # Check if the phrase contains at least one meaningful word
    # meaningful_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
    meaningful_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBN', 'VBZ']
    # remove 'vbp' , 'VBG','JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'
    
    if len(words) == 1:
        word = words[0]
        tag = pos_tags[0][1]
        # print(word,tag)
        return tag in meaningful_tags and word.lower() not in stop_words
    else:
        return any(tag in meaningful_tags for word, tag in pos_tags)


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
sentence = "I've been experiencing a persistent cough and mild fever over the last week. Initially, I thought it was just a common cold, but now I also have shortness of breath and occasional chest pains. I haven't been around anyone sick and I'm worried it might be something more serious. My energy levels are quite low and I've been feeling unusually tired."
chunked_phrases = chunk_sentence(sentence)


# Define a set of stopwords
stop_words = set(stopwords.words('english'))

# Filter out less meaningful phrases
meaningful_phrases = [phrase for phrase in chunked_phrases if is_meaningful(phrase)]

print(chunked_phrases)
print(meaningful_phrases)