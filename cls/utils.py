from transformers import pipeline

# Load the zero-shot classification pipeline using the specified model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the labels for Bloom's Taxonomy levels
labels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"]

def determine_taxonomy_level(question):
    # Enhance the question with context to provide better results
    context_question = f"In which Bloom's Taxonomy level does the following question fall: '{question}'?"

    # Use the classifier to get the labels and scores
    result = classifier(context_question, candidate_labels=labels)
    
    # Find the label with the highest score
    best_label = result['labels'][0]
    best_score = result['scores'][0]

    return best_label, best_score