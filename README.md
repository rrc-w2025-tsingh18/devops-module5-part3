# Pixel River Financial — Module 5 Part 3
Student: Taranpreet Singh

Services: NGINX gateway, static portfolio, Python Flask banking backend, Node.js transactions reporting, MongoDB.

## Run
`docker compose up -d --build --wait`
Visit http://localhost:8081. Follow the banking link, register, log in, deposit, and withdraw.
To view recorded transactions use `http://localhost:8081/api/transactions/your-email@example.com` after making transactions.
Test invalid IDs at `http://localhost:8081/api/transactions/invalid-id` (expected HTTP 400).
Check `docker compose exec nginx nginx -t` and `docker compose ps`.

## CI
Push this folder to your own GitHub repository on the main branch. `.github/workflows/ci.yml` runs Node tests, builds Docker images, validates NGINX and checks endpoints. Confirm the run is green in the Actions tab; capture your own screenshot. The workflow has not been executed by this package generator.

## Notes
Only NGINX publishes port 8081. MongoDB data persists in `mongo_data`. This is a learning demo, not production banking software. Transaction lookup by email is intentionally simplified and must not be exposed publicly without authentication and authorization. Add screenshots, personal test results and your own GitHub URL to the report before submitting.
