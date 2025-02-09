# Phishing Detector in Go

This is a phishing detection tool written in Go to test our AWS ECS with Fargate deployment. The application checks email addresses to detect potential phishing attempts based on:

- **Levenshtein Distance**: A string similarity metric is used to compare the email domain against known legitimate domains.
- **WhoIsAPI**: This API is used to fetch domain registration details to verify the legitimacy of the email domain.

## Features
- **Domain Validation**: Uses WhoIsAPI to check the registration details of the domain.
- **Levenshtein Distance Check**: String Similarity check.


## Setup and Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/AWS-ECS.git
    cd AWS-ECS
    ```

2. Install dependencies:

    You need to install the `whois` library or set up the API for WhoIsAPI in your Go environment.

    ```bash
    go get github.com/domainr/whois
    ```

3. Set up your API key for WhoIsAPI from https://apilayer.com/marketplace

## Usage

Run the application using:

```bash
go run app/main.go

