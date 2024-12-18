import os

def load_glove_embeddings(file_path):
    """
    Load pre-trained GloVe embeddings into a dictionary, 
    where keys are words and values are corresponding vectors (300d floats).
    Format: {word: vector}.
    """
    embeddings = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = list(map(float, values[1:]))
            embeddings[word] = vector
    return embeddings

def split_and_map_terms(terms, embeddings, phrase_level=False):
    """
    Map terms to embeddings as either individual word-level mappings (default) 
    or multi-word phrase mappings.
    """
    term_vectors = {}

    for term in terms:
        words = term.split()  

        if phrase_level:
            # Map entire term to a list of word vectors
            vectors = [embeddings[word] for word in words if word in embeddings]
            if vectors:
                term_vectors[term] = vectors
            else:
                print(f"No embeddings found for term '{term}'.")  
        else:
            # Map individual words to their vectors
            for word in words:
                if word in embeddings and word not in term_vectors:
                    term_vectors[word] = embeddings[word]
                elif word not in embeddings:
                    print(f"No embedding found for word '{word}'.") 

    return term_vectors

if __name__ == "__main__":
    # File paths
    glove_file_path = "data/embeddings/glove.42B.300d.txt"
    corpus_file_path = "data/intermediate/corpus.txt" 
    output_file = "data/intermediate/split_term_vectors.txt"

    # Load embeddings
    print("Loading GloVe embeddings...")
    embeddings = load_glove_embeddings(glove_file_path)
    print(f"Loaded {len(embeddings)} embeddings.")

    # Load tokenized corpus
    print("Loading tokenized corpus...")
    with open(corpus_file_path, "r") as f:
        terms = [line.strip() for line in f.readlines()]

    # Map terms to vectors by splitting multi-word phrases
    print("Processing corpus and splitting multi-words...")
    term_vectors = split_and_map_terms(terms, embeddings)

    # Save term vectors
    print(f"Saving split word vectors to {output_file}...")
    with open(output_file, "w") as f:
        for term, vectors in term_vectors.items():
            f.write(f"{term}: {vectors}\n")

    print("Processing completed.")
