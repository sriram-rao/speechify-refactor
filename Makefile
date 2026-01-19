.PHONY: help install test test-watch clean venv setup

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup     - Create virtual environment and install dependencies"
	@echo "  make install   - Install dependencies in existing virtual environment"
	@echo "  make test      - Run all tests"
	@echo "  make test-watch - Run tests in watch mode"
	@echo "  make clean     - Remove virtual environment and cache files"
	@echo "  make venv      - Create virtual environment only"

# Create virtual environment and install dependencies
setup: venv install

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created. Run 'source venv/bin/activate' to activate it."

# Install dependencies
install:
	@echo "Installing dependencies..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed successfully."

# Run all tests
test:
	@echo "Running tests..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	. venv/bin/activate && python -m pytest src/ -v

# Run tests in watch mode (requires pytest-watch)
test-watch:
	@echo "Running tests in watch mode..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	. venv/bin/activate && python -m pytest src/ -v --tb=short

# Run specific test file
test-lru:
	@echo "Running LRU cache tests..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	. venv/bin/activate && python -m pytest src/test_lru.py -v

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	. venv/bin/activate && python -m pytest src/ --cov=src --cov-report=html --cov-report=term

# Clean up virtual environment and cache files
clean:
	@echo "Cleaning up..."
	rm -rf venv
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "Cleanup complete."

# Check if virtual environment exists
check-venv:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make setup' to create it."; \
		exit 1; \
	fi 