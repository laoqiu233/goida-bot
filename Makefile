CODE = common fetcher indexer

format:
	poetry run black $(CODE)
	poetry run isort $(CODE)

lint:
	poetry run pylint $(CODE)

.PHONY: format lint