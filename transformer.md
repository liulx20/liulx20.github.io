### load_dataset

```python
from datasets import load_dataset
dataset = load_dataset('csv', data_files='my_file.csv')
dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])
dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'],
                                              'test': 'my_test_file.csv'})
dataset = load_dataset('text', data_files={'train': ['my_text_1.txt', 'my_text_2.txt'], 'test': 'my_test_file.txt'})
```

```python
from transformers import BertTokenizer, T5ForConditionalGeneration
tokenizer = BertTokenizer.from_pretrained("uer/t5-small-chinese-cluecorpussmall")
model = T5ForConditionalGeneration.from_pretrained("uer/t5-small-chinese-cluecorpussmall")
from datasets import load_dataset

raw_datasets = load_dataset('json',data_files = "./train.json")
input_data = raw_datasets['train']
input_encodings = tokenizer(input_data['query-01'],input_data['response-01'],input_data['query-02'],pad_to_max_length=True,max_length=256,truncation=True)
target_encodings = tokenizer.batch_encode_plus(input_data['query-02-rewrite'],pad_to_max_length=True,max_length=256,truncation=True)
labels = target_encodings['input_ids']
def shift_tokens_right(input_ids, pad_token_id):
    """Shift input ids one token to the right, and wrap the last non pad token (usually <eos>)."""
    prev_output_tokens = input_ids.clone()
    index_of_eos = (input_ids.ne(pad_token_id).sum(dim=1) - 1).unsqueeze(-1)
    prev_output_tokens[:, 0] = input_ids.gather(1, index_of_eos).squeeze()
    prev_output_tokens[:, 1:] = input_ids[:, :-1]
    return prev_output_tokens
decoder_input_ids = shift_tokens_right(labels, model.config.pad_token_id)
labels[labels[:, :] == model.config.pad_token_id] = -100
encodings = {
        'input_ids': input_encodings['input_ids'],
        'attention_mask': input_encodings['attention_mask'],
        'decoder_input_ids': decoder_input_ids,
        'labels': labels,
    }
columns = ['input_ids', 'labels', 'decoder_input_ids','attention_mask',] 
dataset.set_format(type='torch', columns=columns)
```







```python
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig

tok = BartTokenizer.from_pretrained("facebook/bart-large")
model = BartForConditionalGeneration(BartConfig())

input_string = "My dog is <mask> </s>"
decoder_input_string = "<s> My dog is cute"
labels_string = "My dog is cute </s>"

input_ids = tok(input_string, add_special_tokens=False, return_tensors="pt").input_ids
decoder_input_ids =tok(decoder_input_string, add_special_tokens=False, return_tensors="pt").input_ids
labels = tok(labels_string, add_special_tokens=False, return_tensors="pt").input_ids
 
loss = model(input_ids=input_ids, decoder_input_ids=decoder_input_ids, labels=labels)[0]
```



```python
from transformers import MT5ForConditionalGeneration, T5Tokenizer
model = MT5ForConditionalGeneration.from_pretrained("google/mt5-small")
tokenizer = T5Tokenizer.from_pretrained("google/mt5-small")
article = "UN Offizier sagt, dass weiter verhandelt werden muss in Syrien."
summary = "Weiter Verhandlung in Syrien."
batch = tokenizer.prepare_seq2seq_batch(src_texts=[article], tgt_texts=[summary], return_tensors="pt")
outputs = model(**batch)
loss = outputs.loss
```

```python
from transformers import BertTokenizer, T5ForConditionalGeneration,TrainingArguments,Trainer,default_data_collator
tokenizer = BertTokenizer.from_pretrained("uer/t5-small-chinese-cluecorpussmall")
model = T5ForConditionalGeneration.from_pretrained("uer/t5-small-chinese-cluecorpussmall")
from datasets import load_dataset

raw_datasets = load_dataset('json',data_files = "./train.json")
input_data = raw_datasets['train']
split = 0.2
train_dataset, eval_dataset = random_split(input_data, lengths=[int((1-split)*len(input_data))+1, int(split*len(input_data))])
src = list(map(lambda x:[x[0],x[1],x[2]],list(zip(input_data['query-01'],input_data['response-01'],input_data['query-02']))))
batch = tokenizer.prepare_seq2seq_batch(src_texts=src, tgt_texts=input_data['query-02-rewrite'], return_tensors="pt",pad_to_max_length=True,max_length=256,truncation=True)

arg = TrainingArguments(
    "test",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=100,
)
trainer =Trainer(
    model,
    args,
    train_dataset=tokenized_datasets['train'],#?
    eval_dataset=tokenizered_datasets['validation'],#?
    data_collator=default_data_collator,
    tokenizer=tokenizer,
)
trainer.train()
```

```pyhton
train_size = int(0.8 * len(full_dataset))
test_size = len(full_dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])

```

```
src = list(map(lambda x:x[0]+" "+x[1]+" "+x[2],list(zip(input_data['query-01'],input_data['response-01'],input_data['query-02']))))
```

