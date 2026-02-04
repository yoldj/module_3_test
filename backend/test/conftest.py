"""
Test configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.firewall_log import FirewallLog
from app.models.alert_setting import AlertSetting
from app.models.system_setting import SystemSetting
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user(test_db):
    """Create a sample user for testing"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=pwd_context.hash("password123"),
        full_name="Test User",
        is_active=True,
        role="viewer"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_admin(test_db):
    """Create a sample admin user for testing"""
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=pwd_context.hash("admin123"),
        full_name="Admin User",
        is_active=True,
        role="admin"
    )
    test_db.add(admin)
    test_db.commit()
    test_db.refresh(admin)
    return admin


@pytest.fixture
def sample_firewall_log(test_db):
    """Create a sample firewall log for testing"""
    from datetime import datetime

    log = FirewallLog(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        destination_ip="10.0.0.1",
        source_port=12345,
        destination_port=80,
        protocol="TCP",
        action="ALLOW",
        rule_id="RULE-001",
        description="Test log entry",
        severity="info"
    )
    test_db.add(log)
    test_db.commit()
    test_db.refresh(log)
    return log
