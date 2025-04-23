# System Architecture Design for Budg

## Overview

This document outlines the system architecture for **Budg**, a web-based budgeting application designed to manage personal finances, including bank accounts, bills, and user-defined categories. The architecture is based on the Product Requirements Document (PRD) and Database Schema Design, leveraging a modern tech stack for scalability, security, and maintainability. It supports manual data entry, a spreadsheet-like UI, and secure authentication, with a focus on performance, monitoring, and DevOps automation.

## Architectural Goals

- **Usability**: Deliver an intuitive, responsive SPA with a spreadsheet-like interface for managing financial data.
- **Security**: Ensure data protection through JWT/OAuth2 authentication, encrypted connections, and robust access controls.
- **Scalability**: Support moderate user growth with horizontal scaling and caching.
- **Maintainability**: Use automated testing, documentation, and monitoring to streamline development and operations.
- **Performance**: Achieve low-latency API responses and efficient database queries, optimized for large bill/account datasets.

## System Components

### 1. Frontend (React SPA)

- **Framework**: React (CDN-hosted via cdn.jsdelivr.net), Bootstrap CSS for styling.
- **Functionality**:
  - Single-page application (SPA) with client-side rendering.
  - Spreadsheet-like table view for due bills and bank account instances, with drag-and-drop reordering (priority stored in DB).
  - Modal popups for CRUD operations (bills, accounts, etc.).
  - Date range selector (React component) for filtering financial data, defaulting to two weeks before and four weeks after the next account balance.
  - Inline controls (edit/delete icons) and hover effects for table rows/columns.
  - Nested tabs for navigation to management pages (e.g., Bank Accounts, Bills, Categories).
  - Dropdown selectors with “Add” options and hyperlinks for quick data entry.
- **Tools**:
  - Testing: Jest, React Testing Library, Cypress for E2E testing.
  - Documentation: Storybook for component documentation.
  - Monitoring: Sentry for error tracking, PostHog for user analytics, Google Lighthouse CI for performance.

### 2. Backend (FastAPI)

- **Framework**: FastAPI (Python) with Uvicorn as the ASGI server.
- **Functionality**:
  - RESTful API endpoints for CRUD operations on users, bank accounts, bills, due bills, categories, recurrences, and statuses.
  - Authentication via FastAPI Users (JWT, OAuth2 for Google/GitHub, 2FA support).
  - Background tasks for calculating due bill recurrences using `fastapi.BackgroundTasks`.
  - Admin panel via FastAPI Admin (Tortoise ORM + Aerich) for managing users and configurations.
- **ORM**: SQLAlchemy for database interactions, mapping Python objects to PostgreSQL tables.
- **Configuration**: Pydantic Settings for environment variables and secrets management.
- **Tools**:
  - Testing: pytest, pytest-asyncio, httpx.AsyncClient, fastapi.testclient.
  - Documentation: Swagger UI for API documentation, Sphinx for Python code.
  - Monitoring: Sentry for error logging, Prometheus for metrics, Grafana for visualization.

### 3. Database (PostgreSQL)

- **Schema**: As defined in the Database Schema Design, including tables for `User`, `Api_Token`, `OAuth_Account`, `Bill_Status`, `Recurrence`, `Category`, `Bank_Account`, `Bills`, `Due_Bills`, `Bank_Account_Instance`, and `Audit_Log`.
- **Functionality**:
  - Stores all financial and user data with indexes for performance (e.g., `due_date`, `user_id`, `priority`).
  - Audit logging via PostgreSQL triggers to capture changes to all tables (except `Audit_Log`).
  - Supports FastAPI Users for authentication (JWT, OAuth2).
- **Security**:
  - Encrypted connections (SSL/TLS).
  - SQL injection prevention via parameterized queries (SQLAlchemy).
  - Regular backups using pg_dump or cloud-native solutions.
- **Tools**:
  - Testing: pytest-postgresql for database testing.
  - Monitoring: Postgres Exporter for Prometheus, pgAdmin for GUI management.
  - Documentation: Hasura Console for schema visualization.

### 4. Cache/Rate Limiting (Redis)

- **Role**:
  - **Caching**: Store API responses (e.g., bill lists, account balances) to reduce database load.
  - **Rate Limiting**: Enforce 100 requests per minute per user (JWT-based) and per IP, using Redis counters.
  - **Session Management**: Store JWT refresh tokens with expiration.
- **Security**:
  - Authentication enabled with strong passwords.
  - Encrypted connections (TLS).
  - Configured to bind only to localhost or trusted interfaces.
- **Tools**:
  - Testing: fakeredis, pytest-redis.
  - Monitoring: Redis Exporter for Prometheus, RedisInsight for GUI management.
  - Error Logging: Sentry for Redis-related errors.

## Data Flow

1. **User Interaction**:
   - Users access the React SPA via a modern browser, authenticated via JWT or OAuth2 (Google/GitHub).
   - The SPA sends API requests to the FastAPI backend for CRUD operations and data retrieval.
2. **API Processing**:
   - FastAPI validates requests using Pydantic, enforces rate limits via Redis, and authenticates users via JWT/OAuth2.
   - SQLAlchemy queries PostgreSQL for data, with cached responses retrieved from Redis when applicable.
   - Background tasks (e.g., due bill recurrence calculations) are scheduled via `fastapi.BackgroundTasks`.
3. **Database Operations**:
   - PostgreSQL handles data storage and retrieval, with triggers logging changes to the `Audit_Log` table.
   - Indexes optimize queries for filtering/sorting (e.g., by `due_date`, `priority`).
4. **Monitoring**:
   - Sentry captures errors across frontend, backend, and Redis.
   - Prometheus collects metrics (e.g., API latency, database query time) from Postgres Exporter, Redis Exporter, and FastAPI.
   - Grafana visualizes metrics, and PostHog tracks user interactions (e.g., bill creation, login frequency).
   - Logs are aggregated in the ELK/EFK stack for search and analysis.

## Security Architecture

- **Authentication**:
  - FastAPI Users with JWT for API tokens and OAuth2 for social logins (Google/GitHub).
  - 2FA support via TOTP (e.g., Google Authenticator).
  - Password hashing with bcrypt or Argon2.
  - JWT refresh tokens stored in Redis with short expiration.
- **Authorization**:
  - Role-Based Access Control (RBAC) with roles (e.g., user, superuser) defined in the `User` table.
  - OAuth2 scopes for least privilege (e.g., read-only vs. write access).
- **Network Security**:
  - Uvicorn serves HTTPS with SSL/TLS certificates.
  - CORS rules restrict frontend origins to the SPA domain.
  - Security headers (e.g., Content-Security-Policy, X-Frame-Options) enforced via FastAPI middleware.
- **Data Security**:
  - PostgreSQL connections use SSL/TLS.
  - Redis connections use TLS and authentication.
  - Pydantic validates all input data to prevent injection attacks.
- **Vulnerability Management**:
  - GitHub Dependabot and Snyk for dependency scanning.
  - GitHub CodeQL and Bandit for static code analysis.
  - SonarQube for code quality and security checks.
  - Safety for Python dependency scanning.
- **CI/CD Security**:
  - GitHub Signed Commits and Branch Protection for code integrity.
  - Secrets stored in GitHub Actions secrets or cloud-native secret managers.

## Monitoring and Observability

- **Golden Metrics**:
  - **Latency**: API response times, database query durations, Redis command latencies.
  - **Traffic**: Requests per second, active users, bill/account CRUD operations.
  - **Errors**: HTTP 4xx/5xx errors, database errors, Redis connection issues.
  - **Saturation**: CPU/memory usage (FastAPI, PostgreSQL, Redis), database connection pool usage.
- **Additional Metrics**:
  - User actions: Login frequency, bill creation/edit rate, date range selector usage.
  - Database: Slow queries, index usage, table growth.
  - Redis: Cache hit/miss ratio, key eviction rate.
- **Tools**:
  - **Error Tracking**: Sentry for frontend, backend, and Redis errors.
  - **Metrics**: Prometheus with Postgres Exporter, Redis Exporter, and FastAPI instrumentation.
  - **Visualization**: Grafana dashboards for golden metrics and user activity.
  - **Distributed Tracing**: OpenTelemetry (OTel) with Grafana Tempo for request tracing.
  - **Log Aggregation**: ELK/EFK stack for log search and dashboards.
  - **User Analytics**: PostHog for tracking user interactions (e.g., modal usage, drag-and-drop).
  - **Performance**: Google Lighthouse CI for frontend performance audits.

## DevOps Automation

- **Version Control**: Git with GitHub for source code management.
- **CI/CD Pipeline**:
  - **Build**: GitHub Actions to frontend (React) and backend (FastAPI).
  - **Test**: Run unit tests (pytest, Jest), integration tests (Cypress), and coverage reports (pytest-cov, Codecov).
  - **Security Scans**: Dependabot, CodeQL, Snyk, Bandit, SonarQube.
- **Local Development**:
  - `.env.test` files managed via pytest-env for test environments.
- **Documentation**:
  - Swagger UI for API endpoints.
  - Hasura Console for PostgreSQL schema.
  - Sphinx with autodoc for Python code.
  - Storybook for React components.

## Scalability Considerations

- **Horizontal Scaling**:
  - PostgreSQL read replicas for read-heavy queries (e.g., bill lists).
  - Redis cluster for high availability if needed.
- **Caching**:
  - Redis caches API responses (e.g., bill lists) with TTLs (e.g., 5 minutes).
  - Cache invalidation on CRUD operations via FastAPI middleware.
- **Database Optimization**:
  - Indexes on `user_id`, `due_date`, `priority`, and foreign keys for fast queries.
  - Partitioning of `Audit_Log` table by `timestamp` for large datasets.
- **Future Enhancements**:
  - Kubernetes for orchestration if user base grows significantly.
  - Multi-region PostgreSQL for low-latency global access.
  - Advanced caching strategies (e.g., Redis sharding).

## Testing Strategy

- **Unit Testing**:
  - Backend: pytest, pytest-asyncio, pytest-mock for FastAPI and SQLAlchemy.
  - Frontend: Jest and React Testing Library for React components.
- **Integration Testing**:
  - httpx.AsyncClient and fastapi.testclient for API endpoints.
  - pytest-postgresql for database interactions.
  - fakeredis for Redis interactions.
- **E2E Testing**:
  - Cypress for full-stack testing (frontend + backend + database).
  - Spin up test environments.
- **Auth Testing**:
  - fastapi-users test utils and PyJWT for JWT token testing.
- **Coverage**:
  - pytest-cov for backend coverage.
  - Codecov for coverage reporting and GitHub integration.
  - Allure/pytest-html for test report visualization.

## Future Considerations

- **Multi-Currency Support**: Add `currency` fields to `Bank_Account` and `Bills` tables, with exchange rate integration.
- **Custom Recurrence Logic**: Extend `Recurrence` table with user-defined calculations, possibly using a scriptable field.
- **Mobile App**: Develop a React Native or Progressive Web App (PWA) version.
- **Advanced Monitoring**: Add Jaeger for deeper tracing if Grafana Tempo is insufficient.
- **Performance Tuning**: Add composite indexes (e.g., `due_date` + `draft_account`) and query optimization based on production data.

## Conclusion

The Budg architecture leverages a modern, secure, and scalable tech stack to deliver a user-friendly budgeting application. By combining a React SPA, FastAPI backend, PostgreSQL database, and Redis for caching/rate limiting, it meets the PRD’s requirements for simplicity, manual data entry, and a spreadsheet-like UI. Robust security, monitoring, and DevOps automation ensure reliability and maintainability, with flexibility for future enhancements like multi-currency support.