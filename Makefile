# Docker image name
IMAGE_NAME := glygen/pubmed-analyzer

# Default tag is "latest" unless overridden
TAG ?= latest
# Default data directory is "./data" unless overridden
DATA_DIRECTORY ?= ./data/
# Input for search script
SEARCH_INPUT ?=
# Input for parse script
PARSE_INPUT ?=

IMAGE := $(IMAGE_NAME):$(TAG)


.PHONY: search parse run run-dev push pull

search:
	data_retrieval/search.sh $(SEARCH_INPUT)

parse:
	python -m data_normalization.parse $(PARSE_INPUT)

pull:
	docker pull $(IMAGE)

run:
	docker run -v $(DATA_DIRECTORY):/data -p 8501:8501 $(IMAGE)

run-dev:
	docker compose up

build: 
	cd streamlit-app && docker build -t $(IMAGE) .

push:
	docker login && docker image push $(IMAGE)