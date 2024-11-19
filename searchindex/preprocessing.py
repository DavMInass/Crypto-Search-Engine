import Stemmer
import re 

# The file 'datasets/stopwords_en.txt' contains a list of stopwords - one per line.
with open("searchindex/datasets/stopwords_en.txt") as f:
    enStopWords = set(f.read().splitlines())

# Initialze the SnowballStemmer
enStemmer = Stemmer.Stemmer('english')

def preprocess_line_en(line: str) -> list[str]:
    # Convert to lower case
    tokens = line.lower()
    
    # Split into tokens with no punctuation
    tokens = re.split("[^\w]", tokens)
    
    # Remove empty strings and stop words and apply the stemmer
    tokens = [enStemmer.stemWord(x) for x in tokens if x and x not in enStopWords]
    
    # Return the tokens
    return tokens