# Go RESTful API with In-Memory Data

This project demonstrates how to write a simple RESTful API in Go using in-memory data. The API provides endpoints to retrieve NBA shot data, post new shot entries, and filter shots by player ID. 
All data is stored in memory for simplicity.

## API Endpoints
- **GET /shots**: Retrieve all shot data.
- **GET /shots/{player_id}**: Retrieve all shots for a specific player.
- **POST /shots**: Add a new shot entry.

## Prerequisites
- Go (version 1.18 or above)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sadesh123/Golang-lambda.git
cd Golang-lambda

### 2. Build the Go Binary
Build the binary using the following command

```bash
go build -o main .

