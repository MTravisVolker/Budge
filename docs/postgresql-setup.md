# PostgreSQL Setup for Local Development

This guide will help you set up a local PostgreSQL instance for Budg development.

## Installation

1. Download PostgreSQL installer for Windows:

   - Go to https://www.postgresql.org/download/windows/
   - Click on the "Download the installer" button
   - Choose the latest version (PostgreSQL 16.x)

2. Run the installer:

   - Choose installation directory (default is fine)
   - Select components to install:
     - PostgreSQL Server
     - pgAdmin 4
     - Command Line Tools
   - Choose data directory (default is fine)
   - Set password for the postgres superuser (remember this password!)
   - Keep the default port (5432)
   - Choose locale (default is fine)

3. Complete the installation

## Configuration

1. Create a database for Budg:

   ```sql
   CREATE DATABASE budg;
   ```

2. Create a user for Budg:

   ```sql
   CREATE USER budg_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE budg TO budg_user;
   ```

3. Update your `.env` file with the database connection details:
   ```
   DATABASE_URL=postgresql://budg_user:your_password@localhost:5432/budg
   ```

## Using pgAdmin 4

1. Open pgAdmin 4 from the Start menu
2. Connect to your server:
   - Right-click on "Servers" → "Register" → "Server"
   - Name: Local PostgreSQL
   - Host: localhost
   - Port: 5432
   - Username: postgres
   - Password: (the password you set during installation)

## Troubleshooting

1. If you can't connect to the database:

   - Check if PostgreSQL service is running (Services → postgresql-x64-16)
   - Verify the port (5432) is not blocked by firewall
   - Ensure the password is correct

2. If you forgot the postgres password:
   - Open pgAdmin 4
   - Right-click on the server → Properties
   - Go to the Connection tab
   - Update the password

## Next Steps

After setting up PostgreSQL:

1. Run database migrations:

   ```bash
   cd backend
   alembic upgrade head
   ```

2. Verify the connection:
   ```bash
   python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://budg_user:your_password@localhost:5432/budg'); engine.connect()"
   ```
