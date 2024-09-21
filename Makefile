CODE = common fetcher indexer

format:
	poetry run black $(CODE)
	poetry run isort $(CODE)

lint:
	poetry run pylint $(CODE)

feeds:
	cat make_feeds.sql | docker exec -i goida-bot-postgres-1 psql -U postgres

.PHONY: format lint load_feeds