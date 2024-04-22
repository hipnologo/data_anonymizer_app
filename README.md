# Data Anonymizer App

[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Forks](https://img.shields.io/github/forks/hipnologo/data_anonymizer_app)](https://github.com/hipnologo/data_anonymizer_app/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/data_anonymizer_app)](https://github.com/hipnologo/data_anonymizer_app/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/data_anonymizer_app)](https://github.com/hipnologo/data_anonymizer_app/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/hipnologo/data_anonymizer_app)](https://github.com/hipnologo/data_anonymizer_app/graphs/contributors)

Data Anonymizer App is a simple Flask-based web application that helps users anonymize sensitive data in CSV and Excel files. The app provides functionalities such as pseudonymization, redaction, and column removal to protect personal information.

## Table of Contents

- [Data Anonymizer App](#data-anonymizer-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Upload CSV and Excel files
- Select different anonymization methods for each column:
  - Pseudonymization: Replace the original data with a unique, irreversible hash
  - Redaction: Replace the original data with a "REDACTED" string
  - Removal: Remove the entire column from the dataset
- Download anonymized files in their original format (CSV or Excel)
- Calculate reidentification risk score (placeholder implementation)

## Installation

1. Clone the repository:

``git clone https://github.com/hipnologo/data_anonymizer_app.git``


2. Change to the project directory:

``cd data_anonymizer_app``


3. Install the required dependencies using pip:

``pip install -r requirements.txt``


4. Generate a secret key and create a `.env` file in the project directory by running the `genkey.py` script:

``python genkey.py``


This will create a `.env` file containing the `SECRET_KEY` variable with a randomly generated 32-byte hexadecimal value. Alternatively you can use: 
`echo "SECRET_KEY=your_secret_key_here" > .env`

5. Generate fake random data into a `.csv` file which will be placed under `data` folder for testing purposes.
``python gendata.py``

Bonus: create a .gitignore for the project.
``curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore``

## Usage

1. Start the Flask development server:

``python app.py``


2. Open a web browser and navigate to `http://127.0.0.1:5000`.

3. Upload a CSV or Excel file and choose the desired anonymization actions for each column.

4. Download the anonymized file.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests to help improve this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
