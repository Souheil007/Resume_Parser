import torch
from transformers import BertTokenizer, BertForTokenClassification

# Load your trained model and tokenizer
model_path = "path_to_your_trained_model_directory"  # Example model path
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForTokenClassification.from_pretrained(model_path)

# Set the model to evaluation mode
model.eval()

# Input text
input_text = "Apple is looking at buying U.K. startup for $1 billion"

# Tokenize input text
tokens = tokenizer.tokenize(input_text)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# Add special tokens [CLS] and [SEP]
token_ids = [tokenizer.cls_token_id] + token_ids + [tokenizer.sep_token_id]

# Convert token IDs to tensor
input_tensor = torch.tensor([token_ids])

# Generate attention mask
attention_mask = torch.ones_like(input_tensor)

# Model prediction
with torch.no_grad():
    outputs = model(input_tensor, attention_mask=attention_mask)

# Get predicted labels
predicted_labels = torch.argmax(outputs.logits, dim=2)[0].tolist()

# Map token IDs back to tokens
predicted_tags = [model.config.id2label[label_id] for label_id in predicted_labels[1:-1]]  # Exclude [CLS] and [SEP] tokens

# Print token-tag pairs
for token, tag in zip(tokens, predicted_tags):
    print(f"{token}: {tag}")