import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# Load tokenizer and model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set the pad_token to be the same as the eos_token
tokenizer.pad_token = tokenizer.eos_token

# Load your JSON data
with open('personal-data.json') as f:
    data = json.load(f)

# Transform the data into a Hugging Face Dataset
dataset = Dataset.from_dict({"text": [item['text'] for item in data]})

# Tokenize the texts


def tokenize_function(examples):
    tokenized = tokenizer(
        examples['text'], padding=True, truncation=True, max_length=512)
    # Copy input_ids to labels
    tokenized['labels'] = tokenized['input_ids'].copy()

    # Replace padding token IDs in labels with -100 to ignore them in loss calculation
    tokenized['labels'] = [
        [-100 if token == tokenizer.pad_token_id else token for token in label]
        for label in tokenized['labels']
    ]
    return tokenized


# Apply the tokenization
tokenized_datasets = dataset.map(
    tokenize_function, batched=True, remove_columns=["text"])

# Use Hugging Face's built-in train_test_split method
train_test_split = tokenized_datasets.train_test_split(test_size=0.1)

# Extract the training and evaluation datasets
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']


# Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,  # Save only the last two checkpoints
    logging_dir='./logs',
)

# Create the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets
)

# Start training
trainer.train()

# Save the model and tokenizer
model.save_pretrained("mon_modele")
tokenizer.save_pretrained("mon_modele")

print("training ended")
