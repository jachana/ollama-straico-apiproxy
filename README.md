# Ollama Straico API Proxy

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-brightgreen.svg)
[![Build and Push Docker Images](./actions/workflows/docker-image.yml/badge.svg)](./actions/workflows/docker-image.yml)

## Project Description

OllamaStraicoAPIProxy implements the same Ollama API endpoints but redirects the requests to the Straico API Server. 
This allows you to use any application that supports Ollama while leveraging Straico's available cloud LLM models instead of running a local LLM.

**Disclaimer:** This is not an official Ollama or Straico product.

## Requirements

- Python 3.12 or higher
- Docker (for containerized deployment)
- Straico API Key

Core Dependencies:
- FastAPI
- Uvicorn
- aio-straico >= 0.1.1
- python-multipart
- jinja2

Additional dependencies may be required for embedding and transcription features.

## Setup 

Please follow the [Setup Guide](./wiki/Deployment-Ollama%E2%80%90straico%E2%80%90apiproxy#basic-deployment).

## Usage

Once the container is running, you can use any Ollama-compatible application by pointing it to `http://localhost:11434` (or the appropriate host and port if you've modified the configuration).

## API Endpoints

### Ollama Endpoints

1. `/api/generate`
   - Method: POST
   - Description: Generate text completions
   - Request Body:
     ```json
     {
       "model": "string",
       "prompt": "string",
       "stream": boolean,
       "options": {
         "temperature": float,
         "max_tokens": integer
       }
     }
     ```

2. `/api/chat`
   - Method: POST
   - Description: Chat completion endpoint with support for function calling
   - Request Body:
     ```json
     {
       "model": "string",
       "messages": [
         {
           "role": "user|system|assistant",
           "content": "string"
         }
       ],
       "stream": boolean,
       "tools": [
         {
           "type": "function",
           "function": {
             "name": "string",
             "description": "string",
             "parameters": object
           }
         }
       ]
     }
     ```

3. `/api/tags`
   - Method: GET
   - Description: List available models and agents
   - Returns: List of available models with their details

4. `/api/version`
   - Method: GET
   - Description: Get API version information

### LM Studio Endpoints

1. `/v1/chat/completions` (alias: `/chat/completions`)
   - Method: POST
   - Description: OpenAI-compatible chat completion endpoint
   - Request Body:
     ```json
     {
       "model": "string",
       "messages": [
         {
           "role": "user|system|assistant",
           "content": "string|object"
         }
       ],
       "temperature": float,
       "stream": boolean,
       "tools": array
     }
     ```
   - Supports: Text completion, image analysis (via content object), function calling

2. `/v1/completions`
   - Method: POST
   - Description: OpenAI-compatible text completion endpoint
   - Request Body:
     ```json
     {
       "model": "string",
       "prompt": "string",
       "temperature": float
     }
     ```

3. `/v1/models` (aliases: `/models`, `/api/models`)
   - Method: GET
   - Description: List available models in OpenAI format
   - Returns: List of models with their IDs and permissions

## Known Working Integrations

OllamaStraicoAPIProxy has been tested and confirmed to work with the following applications and integrations:

1. **Home Assistant**
   - Integration: [Ollama for Home Assistant](https://www.home-assistant.io/integrations/ollama/)
   - Description: Use OllamaStraicoAPIProxy with Home Assistant for AI-powered home automation tasks.

2. **Logseq**
   - Plugin: [ollama-logseq](https://github.com/omagdy7/ollama-logseq)
   - Description: Integrate OllamaStraicoAPIProxy with Logseq for enhanced note-taking and knowledge management.

3. **Obsidian**
   - Plugin: [obsidian-ollama](https://github.com/hinterdupfinger/obsidian-ollama)
   - Description: Use OllamaStraicoAPIProxy within Obsidian for AI-assisted note-taking and writing.

4. **Snippety**
   - Website: [https://snippety.app/](https://snippety.app/)
   - Description: Leverage OllamaStraicoAPIProxy with Snippety for AI assisted snippet management and generation.

5. **Rivet**
   - Website: [https://rivet.ironcladapp.com/](https://rivet.ironcladapp.com/)
   - Description: Allows using Ollama Chat and OpenAI Chat (via LM Studio)

6. **Continue.dev**
   - Website: [https://www.continue.dev/](https://www.continue.dev/)
   - Description: Generate code using Ollama and LM Studio

7. **Open WebUI**
   - Website: [https://docs.openwebui.com/](https://docs.openwebui.com/)
   - Description: Allows using Ollama with Open WebUI
   - Sample Configuration: [docker-compose.yaml](https://gist.github.com/jayrinaldime/2f4442ded08c283249fbd3c568234173)

8. **Flowise**
   - Website: [https://flowiseai.com/](https://flowiseai.com/)
   - Description: Allows using Ollama with Flowise
   - Sample Configuration: [docker-compose.yaml](https://gist.github.com/jayrinaldime/f17c8eec1fe75573d06147ffb7199535)

Please note that while these integrations have been tested, you may need to adjust settings or configurations to point to your OllamaStraicoAPIProxy instance instead of a local Ollama installation.

## To-Do List 

1. Test LM Studio API Endpoints
1. Ensure integration with:
   - [aider.chat](https://aider.chat/)
   
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Ollama](https://github.com/ollama/ollama)
- [Straico](https://www.straico.com/)
