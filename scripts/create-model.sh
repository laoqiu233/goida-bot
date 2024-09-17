docker run -d --name ollama-model -v $(pwd)/.ollama:/root/.ollama -v $(pwd)/models:/models --rm ollama/ollama:latest
docker exec ollama-model ollama create my-model -f /models/Modelfile
docker stop ollama-model
