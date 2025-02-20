

.PHONY: volc-docker-buildx
volc-docker-buildx:
	docker buildx build --platform=linux/amd64 -t ops-tf-volc:latest -f ./volc.Dockerfile . --load