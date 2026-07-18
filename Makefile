.PHONY: doctor site site-serve test lint typecheck format-check markdown-lint external-links secret-scan validate lab-up lab-down clean

doctor:
	@python --version
	@node --version
	@docker --version
	@docker compose version

site:
	python scripts/build_docs.py
	mkdocs build --strict

site-serve:
	python scripts/build_docs.py
	mkdocs serve

test:
	python -m unittest discover -s lab/tests -v

lint:
	ruff check .
	npm run lint

typecheck:
	python -m mypy lab scripts
	npm run typecheck

format-check:
	npm run format:check

markdown-lint:
	npm run markdown:lint

external-links:
	python scripts/check_external_links.py

secret-scan:
	python scripts/scan_public_tree.py

validate:
	python scripts/validate_sources.py
	python scripts/validate_curriculum.py
	python scripts/validate_lessons.py
	python scripts/validate_labs.py
	python scripts/validate_load_scripts.py
	python scripts/check_internal_links.py
	python scripts/build_docs.py
	python -m unittest discover -s lab/tests -v
	python -m mypy lab scripts
	ruff check .
	npm test
	npm run lint
	npm run format:check
	npm run markdown:lint
	npm run typecheck
	python scripts/scan_public_tree.py
	docker compose -f lab/docker-compose.yml config --quiet
	mkdocs build --strict

lab-up:
	docker compose -f lab/docker-compose.yml up --build -d

lab-down:
	docker compose -f lab/docker-compose.yml down

clean:
	@echo "Remove generated site and telemetry with your platform's normal file tools."
