CODE = common fetcher indexer bot

format:
	poetry run black $(CODE)
	poetry run isort $(CODE)

lint:
	poetry run pylint $(CODE)

feeds:
	cat make_feeds.sql | docker exec -i goida-bot-postgres-1 psql -U postgres

indexed:
	cat indexed_count.sql | docker exec -i goida-bot-postgres-1 psql -U postgres

ask:
	poetry run python -m asker

.PHONY: format lint load_feeds ask