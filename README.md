# Budg - Personal Budgeting Application

Budg is a web-based budgeting application designed to help users manage personal finances by tracking bank accounts, credit card accounts, and bills. It provides a clear view of current account balances, upcoming and paid bills, and projected balances after bill payments.

## Features

- Manual data entry for bills and account balances
- User-configurable categories
- Customizable date ranges for viewing financial data
- Spreadsheet-like interface with drag-and-drop functionality
- Secure authentication with OAuth2 support
- Real-time balance projections

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: React, Bootstrap, TypeScript
- **Authentication**: JWT, OAuth2 (Google, Facebook)
- **Monitoring**: Prometheus, Grafana, Sentry
- **Testing**: pytest, Jest, Cypress

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Git

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   alembic upgrade head
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 