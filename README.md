# Competitive Programming Platform API

## Overview

Competitive Programming Platform API is a cutting-edge API designed to support local (offline) competitive programming competitions. It provides a robust backend system for compiling, executing, and validating code submissions across multiple programming languages including C++, Java, Rust, Python, and Go. Tailored for organizers and participants of coding contests, this API aims to streamline the process of managing submissions, testing solutions, and ensuring a fair and efficient competition environment.

## Features

- **Multi-Language Support**: Seamless execution of code in C++, Java, Rust, Python, and Go.
- **Code Execution**: Compile and run submissions with custom input, capturing output for validation.
- **Output Validation**: Automatically validate code output against expected results for quick and accurate judging.
- **Output Comparison**: Compare outputs from different submissions to detect similarities and ensure originality.
- **Secure Execution**: Designed with security in mind to safely execute user-submitted code.
- **Easy Integration**: RESTful API allows for easy integration with existing systems or platforms.

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Compiler/Interpreter for each supported language (GCC for C++, OpenJDK for Java, etc.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/henihaddad/CodeChamp.git
   ```

2. Navigate to the project directory:
   ```bash
   cd CompetitiveProgrammingPlatformAPI
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## Usage

Refer to the `/docs` endpoint for detailed API documentation and interactive testing features.

### Example: Compile and Execute C++ Code

```bash
curl -X 'POST'   'http://localhost:8000/compile_execute_all_file_types'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'code=<C++ Code Here>'   -F 'input=<Input Data Here>'   -F 'programming_language=CPP'
```

## Contributing

We welcome contributions from the community! Please refer to the `CONTRIBUTING.md` file for guidelines on how to make contributions.

## Security

If you discover a security vulnerability within the project, please send an email to hanihaddad111@gmail.com. All security vulnerabilities will be promptly addressed.

## License

This project is licensed under the MIT License 

## Acknowledgments

- Special thanks to all contributors and users of the Competitive Programming Platform API.
- Inspired by the needs of local competitive programming communities.

## About the Author

Competitive Programming Platform API was created by Hani Haddad, a passionate developer and advocate for competitive programming. For more information, visit [GitHub](https://github.com/henihaddad).
