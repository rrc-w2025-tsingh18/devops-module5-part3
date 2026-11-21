# Pixel River Financial — Module 5 Part 3

**Student:** Taranpreet Singh

## Project Overview

This project uses Docker Compose to run five services:

- NGINX gateway
- Static student portfolio
- Python Flask banking backend
- Node.js transactions service
- MongoDB database

## How to Run

Open a terminal in the Part 3 folder and run:

docker compose up -d --build --wait

Open http://localhost:8081 in your browser.

Click the banking link, register an account, log in, deposit money and withdraw money.

To view transactions, open:

http://localhost:8081/api/transactions/your-email@example.com


To test an invalid identifier:


http://localhost:8081/api/transactions/invalid-id

Expected result: HTTP 400.

## Testing

Check NGINX configuration:


docker compose exec nginx nginx -t

Check running containers:

docker compose ps


Run Node.js tests:

cd transactions
npm install
npm test

**Local test results:**
- Tests passed: 1
- Tests failed: 0

## GitHub Actions CI

The GitHub Actions workflow is configured in `.github/workflows/ci.yml`.

It runs automated tests and project checks.

The workflow completed successfully on the `main` branch.

**GitHub Repository:**

https://github.com/rrc-w2025-tsingh18/devops-module5-part3

## Notes

Only NGINX exposes port 8081.

MongoDB data is stored in the `mongo_data` volume.

This project is for learning purposes only and is not intended for real banking use. Transaction lookup by email would require authentication and authorization in a production application.