#import asyncio
from aiohttp import web
import os
import json
import torch
from transformers import MBartTokenizer, MBartForConditionalGeneration
from datetime import datetime

# init summarizer
model_name = "IlyaGusev/mbart_ru_sum_gazeta"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
#device = os.environ.get('DEVICE', '')
tokenizer = MBartTokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name).to(device)
print(datetime.now(), 'ready', device)


async def call_test(request):
        content = "get ok"
        return web.Response(text=content, content_type="text/html")


async def call_inference(request):
	request_str = json.loads(str(await request.text()))
	request = json.loads(request_str)
	print(datetime.now(), 'received request:',len(request['in_text']))

	input_ids = tokenizer.prepare_seq2seq_batch(
		[request['in_text']],
		src_lang="en_XX", # fairseq training artifact
		return_tensors="pt",
		padding="max_length",
		truncation=True,
		max_length=int(request['in_max_length']) # 600
	).to(device)["input_ids"]

	output_ids = model.generate(
		input_ids=input_ids,
		max_length=162,
		no_repeat_ngram_size=request['out_no_repeat_ngram_size'], # 3
		num_beams=request['out_num_beams'], # 5
		top_k=request['out_top_k'] # 0
	)[0]

	summary = tokenizer.decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
	print(datetime.now(), 'response:',len(summary))

	return web.Response(text=str(summary),content_type="text/html")


def main():
	app = web.Application(client_max_size=1024**3)
	app.router.add_route('GET', '/test', call_test)
	app.router.add_route('POST', '/inference', call_inference)
	web.run_app(app, port=os.environ.get('PORT', ''))


if __name__ == "__main__":
        main()