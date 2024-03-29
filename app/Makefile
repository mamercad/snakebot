LOCAL_TAG := "registry:5000/snakebot"
QUAY_TAG := "quay.io/mamercad/snakebot"
DOCKER_TAG := "mamercad/snakebot"
VERSION := $(shell cat VERSION)

.PHONY: all

.DEFAULT_GOAL: help

help: ## Shows this help
	@fgrep -h "##" $(MAKEFILE_LIST) | \
		fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build the Docker image
	# @docker build --no-cache -t $(LOCAL_TAG):$(VERSION) .
	# @docker build --no-cache --tag $(QUAY_TAG):$(VERSION) .
	@docker build --no-cache --tag $(DOCKER_TAG):$(VERSION) .

push: ## Push the Docker image
	# @docker push $(LOCAL_TAG):$(VERSION)
	# @docker push $(QUAY_TAG):$(VERSION)
	@docker push $(DOCKER_TAG):$(VERSION)

deploy: ## Deploy the app
	cd ../ansible && ansible-playbook -i localhost, -c local deployment.yml -v

shipit: ## build push deploy ## Ship it!
	git tag $(shell cat VERSION)
	git push
	git push --tags

run: ## Run the Docker image
	@docker run --rm -it -p 3000:3000/tcp \
		-e SLACK_SIGNING_SECRET \
		-e SLACK_BOT_TOKEN \
		-e DISCORD_WEBHOOK \
		$(DOCKER_TAG):$(VERSION)
