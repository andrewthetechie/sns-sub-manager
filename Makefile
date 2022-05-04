.DEFAULT_GOAL := help
LOCALSTACK_CONTAINER_NAME="localstack"
LOCALSTACK_DEFAULT_REGION="us-east-1"



# This help function will automatically generate help/usage text for any make target that is commented with "##".
# Targets with a singe "#" description do not show up in the help text
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


test: ## Test the python code with pytest
	pytest

lint: ## Lint the python code
	pre-commit run -a


run-local: ## Runs a local server under uvicorn on port 8000
	cd src; poetry run uvicorn sns_sub_manager.main:app --reload --log-level debug

start-localstack: # Runs localstack in docker
	docker run -it -d --rm --name $(LOCALSTACK_CONTAINER_NAME) -p 4566:4566 -p 4571:4571 localstack/localstack || echo "$(LOCALSTACK_CONTAINER_NAME) is either running or failed"

stop-fake-sqs: # Stops localstack
	docker stop $(LOCALSTACK_CONTAINER_NAME)

create-test-sns: # Creates a test sns
	AWS_ACCESS_KEY_ID=x AWS_SECRET_ACCESS_KEY=x AWS_DEFAULT_REGION=$(LOCALSTACK_DEFAULT_REGION) aws --endpoint-url http://localhost:4566 sns create-topic --name test
