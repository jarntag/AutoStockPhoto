from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load a pre-trained model (replace with a suitable model)
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_keywords(image_description):
  inputs = tokenizer(image_description, return_tensors="pt")
  outputs = model.generate(**inputs)
  generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
  # Extract keywords from generated text
  keywords = generated_text.split(",")
  return keywords