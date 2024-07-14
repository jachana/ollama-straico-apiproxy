import time
import json
from app import app
import pprint
from flask import request, jsonify, Response
from backend.straico import list_model, prompt_completion

@app.route("/api/version", methods=["GET"])
def ollamaversion():
    return {'version': '0.1.41'}, 200

@app.route("/api/delete", methods=["DELETE"])
def ollamadelete():
    print(request.data)
    return "",200

@app.route("/api/pull", methods=["POST"])
def ollamapull():
    print(request.data)
    return Response(generate_ollama_pull_stream(), content_type='application/x-ndjson')

def generate_ollama_pull_stream():
    yield '{"status":"pulling manifest"}\n'
    time.sleep(0.5)
    yield '''{"status": "downloading sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182",
     "digest": "sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182", "total": 455,
     "completed": 455}\n'''
    time.sleep(0.5)
    yield '''{{"status": "verifying sha256 digest"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "writing manifest"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "removing any unused layers"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "success"}\n'''

@app.route("/api/show", methods=["POST"])
def show_model_details():
    return jsonify({
  "modelfile": "# Modelfile generated by \"ollama show\"\n# To build a new Modelfile based on this one, replace the FROM line with:\n# FROM llava:latest\n\nFROM /Users/matt/.ollama/models/blobs/sha256:200765e1283640ffbd013184bf496e261032fa75b99498a9613be4e94d63ad52\nTEMPLATE \"\"\"{{ .System }}\nUSER: {{ .Prompt }}\nASSISTANT: \"\"\"\nPARAMETER num_ctx 4096\nPARAMETER stop \"\u003c/s\u003e\"\nPARAMETER stop \"USER:\"\nPARAMETER stop \"ASSISTANT:\"",
  "parameters": "num_keep                       24\nstop                           \"<|start_header_id|>\"\nstop                           \"<|end_header_id|>\"\nstop                           \"<|eot_id|>\"",
  "template": "{{ if .System }}<|start_header_id|>system<|end_header_id|>\n\n{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>\n\n{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ .Response }}<|eot_id|>",
  "details": {
    "parent_model": "",
    "format": "gguf",
    "family": "llama",
    "families": [
      "llama"
    ],
    "parameter_size": "8.0B",
    "quantization_level": "Q4_0"
  },
  "model_info": {
    "general.architecture": "llama",
    "general.file_type": 2,
    "general.parameter_count": 8030261248,
    "general.quantization_version": 2,
    "llama.attention.head_count": 32,
    "llama.attention.head_count_kv": 8,
    "llama.attention.layer_norm_rms_epsilon": 0.00001,
    "llama.block_count": 32,
    "llama.context_length": 8192,
    "llama.embedding_length": 4096,
    "llama.feed_forward_length": 14336,
    "llama.rope.dimension_count": 128,
    "llama.rope.freq_base": 500000,
    "llama.vocab_size": 128256,
    "tokenizer.ggml.bos_token_id": 128000,
    "tokenizer.ggml.eos_token_id": 128009,
    "tokenizer.ggml.merges": [],            # populates if `verbose=true`
    "tokenizer.ggml.model": "gpt2",
    "tokenizer.ggml.pre": "llama-bpe",
    "tokenizer.ggml.token_type": [],        # populates if `verbose=true`
    "tokenizer.ggml.tokens": []             # populates if `verbose=true`
  }
})


@app.route("/api/tags", methods=["GET"])
def list_straico_models():
    models = list_model()["data"]
    return jsonify({
  "models": [
    {
      "name": m["model"],
      "model": m["model"],
      "modified_at": "2023-11-04T14:56:49.277302595-07:00",
      "size": 7365960935,
      "digest": m["model"], #"9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
      "details": {
        "format": "gguf",
        "family": "llama",
        "families": None,
        "parameter_size": "",
        "quantization_level": "Q4_0"
      }
    } for m in models] })

@app.route("/api/generate", methods=["POST"])
def ollamagenerate():
    try:
        msg = request.json
    except:
        msg = json.loads(request.data.decode())

    pprint.pprint(msg)
    request_msg = msg["prompt"]
    model = msg.get("model")
    if msg.get("stream") == False:
        response = prompt_completion(msg["prompt"], model)
        return {
  "model": model,
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": response,
  "done": True,

  "total_duration": 10706818083,
  "load_duration": 6338219291,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 130079000,
  "eval_count": 259,
  "eval_duration": 4232710000
}
    return Response(generate_ollama_stream(request_msg, model), content_type='application/json')


@app.route("/api/chat", methods=["POST"])
def ollamachat():
    try:
        msg = request.json
        model = msg["model"]
    except:
        msg = json.loads(request.data.decode())

    if "stream" in msg:
        streaming = msg.get("stream")
    else:
        streaming = True

    # if ":" in msg["model"]:
    #     model = msg["model"].split(":")[0]
    pprint.pprint(msg)
    print(model)
    request_msg = json.dumps(msg["messages"], indent=True)
    response = prompt_completion(request_msg, model)
    try:
        response = json.loads(response)
        response = response[0]["content"]
    except:
        pass
#     return json.dumps({
#     "id": "chatcmpl-641",
#     "object": "chat.completion",
#     "created": 1709741623,
#     "model": model,
#     "system_fingerprint": "fp_ollama",
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "role": "assistant",
#                 "content": response
#             },
#             "finish_reason": "stop"
#         }
#     ],
#     "usage": {
#         "prompt_tokens": 12,
#         "completion_tokens": 11,
#         "total_tokens": 23
#     }
# }, indent=False).replace('\n', '')+ "\n"
    if streaming:
        return Response(response_stream(model,response), content_type='application/json')
    else:
        return {
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "message": {
    "role": "assistant",
    "content":response
  },
  "done": True,
  "total_duration": 5191566416,
  "load_duration": 2154458,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 383809000,
  "eval_count": 298,
  "eval_duration": 4799921000
}, 200

def response_stream(model, response):
    yield json.dumps({
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "message": {
    "role": "assistant",
    "content":response
  },
  "done": False,
  "total_duration": 5191566416,
  "load_duration": 2154458,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 383809000,
  "eval_count": 298,
  "eval_duration": 4799921000
}, indent=False).replace('\n', '')+ "\n"

    yield json.dumps({
        "model": model,
        "created_at": "2023-12-12T14:13:43.416799Z",
        "done": True,
        "total_duration": 5191566416,
        "load_duration": 2154458,
        "prompt_eval_count": 26,
        "prompt_eval_duration": 383809000,
        "eval_count": 298,
        "eval_duration": 4799921000
    }, indent=False).replace('\n', '') + "\n"



def generate_ollama_stream(msg, model):
    print(msg)
    r =  json.dumps({
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "response": "\n",
  "done": False
    }, indent=False).replace('\n', '')+ "\n"
    #print(r)
    yield r
    response = prompt_completion(msg, model)

    r = {
        "model": model,
        "created_at": "2023-12-12T14:14:43.416799Z",
        "response": response,
        "done": False}
    r = json.dumps(r, indent=False).replace('\n', '')+ "\n"
    print(r)
    yield r
    r = json.dumps({
        "model": model,
        "created_at": "2023-12-12T14:14:43.416799Z",
        "response": "",
        "done": True,
        "context": [1, 2, 3],
        "total_duration": 10706818083,
        "load_duration": 6338219291,
        "prompt_eval_count": 26,
        "prompt_eval_duration": 130079000,
        "eval_count": 259,
        "eval_duration": 4232710000
    }, indent=False).replace('\n', '')+ "\n"

    #print(r)
    yield r