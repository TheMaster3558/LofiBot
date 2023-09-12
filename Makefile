.PHONY: format_and_isort

format:
	black . && isort . --profile black