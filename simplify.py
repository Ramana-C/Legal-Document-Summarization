from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load T5 model (you can swap with 'google/flan-t5-base' or 't5-small')
MODEL_NAME = "t5-base"

tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def simplify_text(text: str) -> str:
    """Rephrases input text into simpler, plain English."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Prepend instruction for T5
    input_text = "simplify: " + text.strip()

    # Tokenize input
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

    # Generate simplified output
    output_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return output_text
