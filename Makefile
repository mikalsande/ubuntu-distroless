.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

builder:  ## Build the nodejs builder container.
	docker build -f Dockerfile.builder -t builder-nodejs16 .

runner:  ## Buld the nodejs application runner container.
	docker build -f Dockerfile.runner -t runner-nodejs16 .

app:  ## Build an example application container and run it.
	docker build -f Dockerfile.test -t test-nodejs16 .
	docker run -ti --rm test-nodejs16

