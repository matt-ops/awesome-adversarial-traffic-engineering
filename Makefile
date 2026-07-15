.PHONY: doctor docs docs-serve test validate progress lab-up lab-down lab-client lab-analyze clean

doctor:
	@python --version
	@node --version
	@docker --version
	@docker compose version

docs:
	python scripts/build_docs.py
	mkdocs build --strict

docs-serve:
	python scripts/build_docs.py
	mkdocs serve

test:
	python -m unittest discover -s tests -v
	python -m unittest discover -s lab/tests -v

progress:
	python scripts/progress.py

validate:
	python scripts/progress.py --check
	python scripts/validate_curriculum.py
	python scripts/validate_links.py
	python -m unittest discover -s tests -v
	python -m unittest discover -s lab/tests -v
	docker compose -f lab/docker-compose.yml config --quiet

lab-up:
	docker compose -f lab/docker-compose.yml up --build

lab-down:
	docker compose -f lab/docker-compose.yml down

lab-client:
	python -m lab.clients.safe_client --dry-run

lab-analyze:
	python -m lab.analysis.analyze

clean:
	@echo "Remove generated site, telemetry, and reports using your platform's normal file tools."
