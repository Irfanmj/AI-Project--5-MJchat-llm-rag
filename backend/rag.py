from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize the model
embedder = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")



def ask_question(question, context): 
    """Generate an answer to a question based on provided context."""
    # Combine question and context into a single input
    input_text = f"Question: {question} Context: {context}" 
    
    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)
    
    # Generate an answer using the model
    outputs = model.generate(**inputs, max_length=50)
    
    # Decode the generated answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer