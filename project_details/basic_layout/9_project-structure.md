# Project structure

dewey-bot/
├── .editorconfig                    # Configuration for consistent coding styles
├── .env                             # Environment variables
├── .flake8                          # Linting configuration for code quality
├── .gitignore                       # Specifies files and directories ignored by git
├── .gitlab-ci.yml                   # CI/CD pipeline configuration for GitLab
├── .pre-commit-config.yaml          # Configuration for pre-commit hooks
├── environment.yml                  # Environment configuration for package dependencies
├── LICENSE                          # Project license information
├── README.md                        # Overview and documentation of the project
├── requirements.txt                 # List of dependencies for the project
├── sync_branch.sh                   # Shell script for syncing branches
├── sync_feature.sh                  # Shell script for syncing features
├── sync_repos.sh                    # Shell script for syncing repositories
├── project_details/                 # Contains project-related documents and information
├── src/                             # Main source code directory
│   ├── __pycache__/                 # Directory for compiled Python files
│   ├── commands/                    # Contains all bot commands
│   │   ├── __pycache__/             # Directory for compiled Python command files
│   │   ├── add_book.py              # Command to add a new book reference
│   │   ├── generate_summary.py      # Command to generate a summary report
│   │   ├── list_books.py            # Command to list all book references
│   │   ├── set_language.py          # Command to set user language
│   │   └── export_data.py           # Command to export book references
│   ├── config/                      # Configuration files
│   │   └── config.yaml              # Configuration file for bot settings
│   ├── database/                    # Database directory
│   │   └── library.db               # Database file for storing book references
│   ├── migrations/                  # Database migration scripts
│   │   └── migrate_library.py       # Script for managing database migrations
│   ├── utils/                       # Utility files for shared functionalities
│   │   ├── __pycache__/             # Directory for compiled Python utility files
│   │   ├── ai.py                    # AI-related utilities
│   │   ├── database.py              # Database connection utility
│   │   ├── db.py                    # Database utility functions
│   │   ├── lang.py                  # Language translations utility
│   │   ├── logging_config.py        # Logging configuration utility
│   │   ├── nlu.py                   # Natural Language Understanding-related utility
│   │   ├── scheduler.py             # Scheduling utility
│   │   ├── shared.py                # Shared variables and utilities
│   │   ├── validation.py            # Input validation utilities
│   │   └── __init__.py              # Initializes the utility module
│   └── bot.py                       # Main bot logic
├── tests/                           # Contains all test scripts for the project
│   ├── __pycache__/                 # Directory for compiled Python test files
│   ├── test_commands/               # Contains all tests for bot commands
│   │   ├── __pycache__/             # Directory for compiled Python test files
│   │   ├── test_add_book.py         # Test for adding a new book reference
│   │   ├── test_generate_summary.py # Test for generating a summary report
│   │   ├── test_list_books.py       # Test for listing book references
│   │   ├── test_set_language.py     # Test for setting user language
│   │   └── test_export_data.py      # Test for exporting book references
│   ├── test_utils/                  # Contains all tests for utility functions
│   │   ├── __pycache__/             # Directory for compiled Python test files
│   │   ├── test_ai.py               # Test for AI-related utilities
│   │   ├── test_database.py         # Test for database connection utilities
│   │   ├── test_lang.py             # Test for language translation utilities
│   │   ├── test_logging.py          # Test for logging configuration utilities
│   │   ├── test_nlu.py              # Test for Natural Language Understanding utilities
│   │   ├── test_scheduler.py        # Test for scheduling utilities
│   │   ├── test_validation.py       # Test for input validation utilities
│   │   └── __init__.py              # Initializes the test utility module
│   ├── test_bot.py                  # Test for the main bot functionality
│   ├── test_database.py             # Test for database-related functions
│   └── test_lang.py                 # Test for language-related functions
