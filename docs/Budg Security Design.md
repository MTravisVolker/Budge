# Security Design Document for Budg

## Overview

This Security Design Document outlines the security architecture for **Budg**, a web-based budgeting application for managing personal finances, including bank accounts, bills, and user-defined categories. The design aligns with the Product Requirements Document (PRD), Database Schema Design, and System Architecture Design, ensuring robust protection for user data, secure authentication, and adherence to security best practices. It addresses authentication, authorization, data security, network security, monitoring, incident response, and vulnerability management to safeguard Budg’s users and infrastructure, with a reasonable alignment to GDPR, CCPA, and SOC 2 principles without strict compliance requirements.

## Security Objectives

- **Confidentiality**: Protect user data (e.g., financial details, authentication credentials) from unauthorized access.
- **Integrity**: Ensure data accuracy and prevent unauthorized modifications.
- **Availability**: Maintain system uptime and resilience against denial-of-service (DoS) attacks.
- **Auditability**: Track all changes and access to sensitive data for accountability.
- **Compliance**: Reasonably align with GDPR, CCPA, and SOC 2 principles (e.g., data minimization, user consent, audit logging) without formal certification.
- **Scalability**: Support secure growth as user base and features expand.

## Security Architecture

### 1. Authentication

**Objective**: Securely authenticate users and prevent unauthorized access.

- **User Authentication**:
  - **Login/Signup**: Users authenticate via email and password, stored as hashed values in the `User` table (`hashed_password`) using Argon2 for secure password hashing.
  - **Password Policy**: Enforce strong passwords (minimum 12 characters, including uppercase, lowercase, numbers, and symbols) via Pydantic validation in FastAPI.
  - **Multifactor Authentication (2FA)**: Support TOTP-based 2FA (flexible for any TOTP app, e.g., Google Authenticator, Authy) stored in the `mfa_enabled` field. Users are prompted to enable 2FA upon signup.
  - **Password Reset**: Secure password reset via time-limited (1-hour), single-use tokens sent to the user’s verified email (`is_verified` field).
- **OAuth2 Integration**:
  - Support OAuth2 providers (Google, GitHub, Facebook) via FastAPI Users, stored in the `OAuth_Account` table with `provider` and `account_id`.
  - OAuth2 tokens are validated and mapped to user accounts securely, with refresh tokens stored in Redis.
- **API Tokens**:
  - JWT tokens issued for API access, stored in the `Api_Token` table with `issued_at` and `expires_at` timestamps.
  - Access tokens expire after 15 minutes; refresh tokens expire after 7 days and are stored in Redis for session management.
  - Tokens signed with RS256 for stronger security, using asymmetric key pairs.
- **Security Controls**:
  - Rate limit login attempts (5 attempts per 15 minutes per IP) using Redis to prevent brute-force attacks.
  - Secure session cookies with `HttpOnly`, `Secure`, and `SameSite=Strict` flags.
  - Log failed login attempts to the `Audit_Log` table for monitoring.

### 2. Authorization

**Objective**: Enforce least privilege and role-based access control (RBAC).

- **RBAC**:
  - Two roles defined in the `User` table: regular users (`is_superuser = FALSE`) and admins (`is_superuser = TRUE`).
  - Regular users can only access their own data, enforced via `user_id` foreign keys in tables (e.g., `Bills`, `Due_Bills`, `Bank_Account`).
  - Admins can manage users, configurations, and view audit logs via FastAPI Admin, with access restricted to `is_superuser = TRUE`.
- **OAuth2 Scopes**:
  - Define granular scopes for API endpoints (e.g., `read:bills`, `write:bills`, `admin:users`) to restrict access.
  - Scopes enforced via FastAPI dependency injection, validated against JWT claims.
- **Data Isolation**:
  - All queries filter by `user_id` to prevent cross-user data access (e.g., `SELECT * FROM Bills WHERE user_id = :user_id`).
  - SQLAlchemy uses parameterized queries to prevent SQL injection.
- **Security Controls**:
  - Validate `user_id` on all CRUD operations to enforce data ownership.
  - Restrict admin endpoints to `is_superuser = TRUE` users via FastAPI middleware.
  - Follow best practices for API access by requiring JWT authentication for all endpoints, with optional IP whitelisting configurable in the future.

### 3. Data Security

**Objective**: Protect sensitive data at rest and in transit.

- **Data at Rest**:
  - **Database**: PostgreSQL encrypts sensitive fields (e.g., `hashed_password`, `default_amount_due`, `current_balance`) at rest using AES-256, leveraging database-native encryption (e.g., pgcrypto or cloud provider disk encryption).
  - **Key Management**: Encryption keys managed via a cloud-agnostic key management service (e.g., HashiCorp Vault or cloud-native KMS, configured at deployment).
  - **Audit Logs**: `Audit_Log` table stores changes to all tables except itself in `TEXT` format (`value_before_change`, `value_after_change`) without encryption, as they’re for auditing and contain no sensitive data directly.
- **Data in Transit**:
  - All connections (browser to React SPA, SPA to FastAPI, FastAPI to PostgreSQL/Redis) use TLS 1.3 with strong ciphers (e.g., ECDHE-RSA-AES256-GCM-SHA384).
  - SSL/TLS certificates managed via Let’s Encrypt for cloud-agnostic deployments.
- **Input Validation**:
  - Pydantic validates all API inputs, enforcing constraints (e.g., `url` with regex `^https?://`, `font_color_hex` with `^#[0-9A-Fa-f]{6}$`, `recurrence_value` with `CHECK (recurrence_value > 0)`).
  - SQLAlchemy uses parameterized queries to prevent SQL injection.
- **Security Controls**:
  - Encrypt database backups using AES-256 and store securely (e.g., in a cloud storage bucket with server-side encryption).
  - Redis authentication enabled with strong, randomly generated passwords and TLS for connections.
  - Implement data minimization by only storing essential fields (e.g., no unnecessary personal data beyond `email`).

### 4. Network Security

**Objective**: Secure network communications and prevent unauthorized access.

- **HTTPS**:
  - Uvicorn serves FastAPI over HTTPS with valid SSL/TLS certificates, redirecting HTTP requests to HTTPS via FastAPI middleware.
- **CORS**:
  - Restrict CORS to the React SPA’s domain (e.g., `https://budg.app`) to prevent unauthorized frontend access, configured via FastAPI’s CORS middleware.
- **Security Headers**:
  - Enforce headers via FastAPI middleware:
    - `Content-Security-Policy`: Restrict script sources to trusted CDNs (e.g., `cdn.jsdelivr.net` for React, Bootstrap).
    - `X-Frame-Options: DENY`: Prevent clickjacking.
    - `X-Content-Type-Options: nosniff`: Prevent MIME-type sniffing.
    - `Strict-Transport-Security`: Enforce HTTPS for 1 year with `includeSubDomains`.
- **Firewall/WAF**:
  - No WAF required at this stage, but deploy a basic firewall to restrict inbound traffic to ports 443 (HTTPS) and 80 (HTTP redirect).
  - Use cloud-agnostic network security groups or iptables to limit access to trusted IPs if needed in the future.
- **Rate Limiting**:
  - Enforce 100 requests per minute per user (JWT-based) and per IP via Redis counters, returning HTTP 429 with a retry-after header on limit exceeded.
- **Security Controls**:
  - Bind Redis to localhost or trusted interfaces to prevent external access.
  - Use network segmentation to isolate FastAPI, PostgreSQL, and Redis in private subnets (configured at deployment).
  - Log all network access attempts for analysis in the ELK/EFK stack.

### 5. Monitoring and Logging

**Objective**: Detect and respond to security events promptly.

- **Error Tracking**:
  - Sentry captures errors across React SPA, FastAPI, PostgreSQL, and Redis, with user context (e.g., `user_id`) for traceability.
  - Configured to filter sensitive data (e.g., `hashed_password`, `token`) from logs using Sentry’s data scrubbing.
- **Metrics**:
  - Prometheus collects golden metrics:
    - **Latency**: API response times, database query durations, Redis command latencies.
    - **Traffic**: Requests per second, active users, bill/account CRUD operations.
    - **Errors**: HTTP 4xx/5xx errors, database errors, Redis connection issues.
    - **Saturation**: CPU/memory usage, database connection pool usage.
  - Security-specific metrics: Failed login attempts, 2FA enablement rate, rate limit violations, audit log growth.
- **Logging**:
  - `Audit_Log` table tracks all CRUD operations (`add`, `update`, `delete`) with `user_id`, `table_name`, `row_id`, `field_name`, `value_before_change`, `value_after_change`, and `timestamp`.
  - Application logs aggregated in ELK/EFK stack for search and analysis, retained for 1 year (aligned with reasonable GDPR/CCPA practices).
  - Logs encrypted at rest using AES-256.
- **Visualization**:
  - Grafana dashboards display security metrics (e.g., failed logins, rate limit violations, audit log activity).
  - PostHog tracks user actions (e.g., login frequency, bill creation, modal usage) for behavioral analysis.
- **Distributed Tracing**:
  - OpenTelemetry with Grafana Tempo traces requests across React SPA, FastAPI, PostgreSQL, and Redis to identify anomalies (e.g., slow queries indicating enumeration attacks).
- **Security Controls**:
  - Alert on anomalies (e.g., >5 failed logins in 5 minutes, >100 rate limit violations per hour) via Grafana to an admin email or messaging service (e.g., Slack).
  - Conduct monthly log reviews to detect unauthorized access attempts.
  - Rotate logging encryption keys annually.

### 6. Incident Response

**Objective**: Respond effectively to security incidents.

- **Incident Detection**:
  - Monitor Sentry, Prometheus, and ELK/EFK for signs of compromise (e.g., unauthorized API access, SQL injection attempts, unusual audit log activity).
  - Audit logs queried to trace actions (e.g., `SELECT * FROM Audit_Log WHERE user_id = :user_id AND timestamp > :time`).
- **Incident Response Plan**:
  - **Identification**: Use Sentry/Grafana alerts to identify incidents (e.g., rate limit violations, 5xx errors, failed logins).
  - **Containment**: Revoke compromised JWT tokens via Redis, suspend user accounts via `is_active = FALSE`, or isolate affected services (e.g., pause FastAPI instances).
  - **Eradication**: Patch vulnerabilities, rotate credentials (e.g., Redis password, PostgreSQL user, API token secrets), and update SSL certificates if compromised.
  - **Recovery**: Restore from encrypted backups, verify data integrity, and re-enable services.
  - **Lessons Learned**: Document incidents in a post-mortem, update security controls, and train the team (e.g., Travis Volker as lead).
- **Security Controls**:
  - Designate Travis Volker as the incident response lead, with support from the development team.
  - Test incident response plan quarterly via tabletop exercises, simulating scenarios (e.g., stolen JWT, database breach).
  - Notify users of data breaches within 72 hours (aligned with GDPR/CCPA best practices) via email, including remediation steps.

### 7. Vulnerability Management

**Objective**: Identify and remediate vulnerabilities proactively.

- **Dependency Scanning**:
  - GitHub Dependabot and Snyk scan Python (FastAPI, SQLAlchemy, Pydantic) and JavaScript (React, Bootstrap) dependencies nightly.
  - Safety scans Python dependencies for known vulnerabilities during CI/CD builds.
- **Code Scanning**:
  - GitHub CodeQL and Bandit analyze Python code for security issues (e.g., hardcoded credentials, unsafe deserialization).
  - SonarQube enforces code quality and security standards (e.g., no `eval()` usage, proper error handling).
- **Penetration Testing**:
  - Conduct nightly automated penetration tests using open-source tools (e.g., OWASP ZAP) integrated into CI/CD.
  - Perform annual manual penetration tests by a third-party firm to test for vulnerabilities (e.g., XSS, CSRF, privilege escalation).
- **Patch Management**:
  - Apply security patches to FastAPI, PostgreSQL, Redis, and React dependencies within 7 days of release.
  - **Security Controls**:
  - Enforce GitHub signed commits and branch protection to prevent unauthorized code changes.
  - Run scans in CI/CD pipeline (GitHub Actions) and block merges on critical vulnerabilities (CVSS score >7.0).
  - Maintain a vulnerability register in a secure document (e.g., encrypted Notion page) to track remediation status.

### 8. Compliance

**Objective**: Reasonably align with GDPR, CCPA, and SOC 2 principles.

- **GDPR Alignment**:
  - **Data Minimization**: Collect only essential data (`email`, financial details) and avoid unnecessary fields.
  - **User Consent**: Obtain explicit consent for OAuth2 logins (Google, GitHub, Facebook) via provider flows.
  - **Right to Erasure**: Support user deletion via `DELETE FROM User WHERE id = :user_id`, cascading to related tables (`Bills`, `Due_Bills`, etc.).
  - **Data Portability**: Allow users to export their data (e.g., CSV of `Bills`, `Due_Bills`) via a secure API endpoint.
- **CCPA Alignment**:
  - Provide clear privacy policy linked in the React SPA, detailing data usage (e.g., no sharing with third parties).
  - Support opt-out of data collection (not applicable, as no data sharing is in scope).
- **SOC 2 Alignment**:
  - Implement audit logging (`Audit_Log` table) to track all data changes.
  - Enforce access controls (RBAC, JWT authentication) to ensure authorized access.
  - Conduct regular security reviews (quarterly) to verify controls.
- **Audit Readiness**:
  - Generate audit reports via SQL queries (e.g., `SELECT * FROM Audit_Log WHERE timestamp BETWEEN :start AND :end`).
  - Store audit logs for 1 year to support potential audits.
- **Security Controls**:
  - Document security controls (this document) for internal review.
  - Publish a privacy policy and terms of service in the React SPA footer.

## Future Considerations

- **Multi-Tenancy**:
  - Enforce tenant-specific `user_id` checks in all queries to prevent data leakage.
- **Mobile App**:
  - Secure mobile app data with device-level encryption (e.g., iOS Keychain, Android Keystore).
  - Implement certificate pinning to prevent man-in-the-middle attacks.
- **Advanced Threat Detection**:
  - Integrate a SIEM (e.g., Splunk) for real-time threat analysis if user base grows.
  - Use machine learning to detect anomalies (e.g., unusual bill creation patterns via PostHog data).
- **Zero Trust**:
  - Adopt zero-trust principles (e.g., verify every request with JWT and user context) for large-scale deployments.

## Conclusion

The Budg Security Design ensures robust protection for user data and system integrity through secure authentication (JWT, OAuth2, 2FA), authorization (RBAC, data isolation), data encryption (AES-256, TLS 1.3), network security (HTTPS, CORS, rate limiting), monitoring (Sentry, Prometheus, Grafana), incident response (72-hour breach notification), and vulnerability management (nightly scans, annual pentests). By leveraging FastAPI Users, PostgreSQL, Redis, and modern DevSecOps tools (Dependabot, Snyk, CodeQL, SonarQube), Budg meets the PRD’s requirements for a secure, user-friendly budgeting application. Reasonable alignment with GDPR, CCPA, and SOC 2 principles ensures user trust, with a cloud-agnostic design supporting future scalability.