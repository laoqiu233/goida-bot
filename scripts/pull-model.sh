docker run -d --name ollama-model -v $(pwd)/.ollama:/root/.ollama --rm ollama/ollama:latest
docker exec ollama-model ollama pull $1
docker stop ollama-model