.PHONY: all

.DEFAULT_GOAL: help

help: ## Shows this help
	@fgrep -h "##" $(MAKEFILE_LIST) | \
		fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build the Docker image
	@docker build -t $(LOCAL_TAG):$(shell cat VERSION) .

push: ## Push the Docker image
	@docker push $(LOCAL_TAG):$(shell cat VERSION)

run: ## Run the Docker image
	@docker run --rm -it -p 3000:3000/tcp \
		-e SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET} \
		-e SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} \
		$(LOCAL_TAG):$(shell cat VERSION)
