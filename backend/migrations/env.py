import os
import sys
from logging.config import fileConfig
from datetime import timezone
import time

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import your models here
from app.models.base import Base
from app.models.user import User  # Import User first since other models depend on it
from app.models.oauth_account import OAuthAccount
from app.models.api_token import ApiToken
from app.models.audit_log import AuditLog
from app.models.bank_account import BankAccount
from app.models.bank_account_instance import BankAccountInstance
from app.models.bills import Bill
from app.models.due_bills import DueBill
from app.models.category import Category
from app.models.recurrence import Recurrence
from app.models.bill_status import BillStatus

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Load DATABASE_URL from environment variables
config.set_main_option('DATABASE_URL', os.getenv('DATABASE_URL', ''))

# Set timezone to UTC
os.environ['TZ'] = 'UTC'
if sys.platform != 'win32' and hasattr(time, 'tzset'):
    time.tzset()

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
