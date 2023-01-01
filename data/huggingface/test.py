from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained("bigscience/T0pp")
model = AutoModelForSeq2SeqLM.from_pretrained("bigscience/T0pp")
# Read prompt from file
with open("prompt.txt", "r") as f:
    prompt = f.read()
inputs = tokenizer.encode(prompt, return_tensors="pt")
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))
print('done')