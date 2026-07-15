.PHONY: doctor site site-serve test validate lab-up lab-down clean

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
	npm run typecheck

validate:
	python scripts/validate_sources.py
	python scripts/validate_lessons.py
	python scripts/check_internal_links.py
	python -m unittest discover -s lab/tests -v
	npm run typecheck
	docker compose -f lab/docker-compose.yml config --quiet

lab-up:
	docker compose -f lab/docker-compose.yml up --build -d

lab-down:
	docker compose -f lab/docker-compose.yml down

clean:
	@echo "Remove generated site and telemetry with your platform's normal file tools."
