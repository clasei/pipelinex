.PHONY: help install dev build clean lint format

	@echo "formatter not configured yet"
format:

	@echo "linting not configured yet"
lint:

	npm cache clean --force
	rm -rf node_modules dist dist-ssr *.local
clean:

	npm run preview
preview:

	npm run build
build:

	npm run dev
dev:

	npm install
install:

	@echo "make format     - format code (when added)"
	@echo "make lint       - run linter (when added)"
	@echo "make clean      - remove node_modules & build"
	@echo "make preview    - preview production build"
	@echo "make build      - build for production"
	@echo "make dev        - start dev server (port 3000)"
	@echo "make install    - install dependencies"
	@echo ""
	@echo "pipelinex frontend - makefile commands"
help:

