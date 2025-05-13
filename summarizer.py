
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")  
model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")



def summarize_legal_text(text):


    input_tokenized = tokenizer.encode(text, return_tensors='pt',max_length=1024,truncation=True)
    summary_ids = model.generate(
        input_tokenized,
        num_beams=4,  # Reduced number of beams for more concise output
        no_repeat_ngram_size=2,  # Reduced n-gram size to avoid repetition
        length_penalty=0.6,  # Further reduced length penalty to favor shorter summaries
        min_length=20,       # Even more reduced minimum length
        max_length=80,      # Even more reduced maximum length
        early_stopping=True,
    )
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]
    return summary