"""
Test cases for database models
"""
import pytest
from datetime import datetime
from app.models.user import User
from app.models.firewall_log import FirewallLog
from app.models.system_setting import SystemSetting
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestUserModel:
    """Test cases for User model"""

    def test_create_user(self, test_db):
        """Test creating a new user"""
        user = User(
            username="newuser",
            email="newuser@example.com",
            password_hash=pwd_context.hash("password123"),
            full_name="New User",
            is_active=True,
            role="viewer"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.is_active is True
        assert user.role == "viewer"
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_unique_username(self, test_db, sample_user):
        """Test that username must be unique"""
        duplicate_user = User(
            username=sample_user.username,  # Same username
            email="different@example.com",
            password_hash=pwd_context.hash("password123"),
            full_name="Duplicate User",
            is_active=True,
            role="viewer"
        )
        test_db.add(duplicate_user)

        with pytest.raises(Exception):  # Should raise IntegrityError
            test_db.commit()

    def test_user_unique_email(self, test_db, sample_user):
        """Test that email must be unique"""
        test_db.rollback()  # Clear any previous errors

        duplicate_user = User(
            username="differentuser",
            email=sample_user.email,  # Same email
            password_hash=pwd_context.hash("password123"),
            full_name="Duplicate Email User",
            is_active=True,
            role="viewer"
        )
        test_db.add(duplicate_user)

        with pytest.raises(Exception):  # Should raise IntegrityError
            test_db.commit()

    def test_user_roles(self, test_db):
        """Test different user roles"""
        roles = ["admin", "operator", "viewer"]

        for role in roles:
            user = User(
                username=f"user_{role}",
                email=f"{role}@example.com",
                password_hash=pwd_context.hash("password123"),
                full_name=f"{role.capitalize()} User",
                is_active=True,
                role=role
            )
            test_db.add(user)
            test_db.commit()
            test_db.refresh(user)

            assert user.role == role

    def test_user_repr(self, sample_user):
        """Test user __repr__ method"""
        repr_str = repr(sample_user)
        assert "User" in repr_str
        assert str(sample_user.id) in repr_str
        assert sample_user.username in repr_str
        assert sample_user.role in repr_str


class TestFirewallLogModel:
    """Test cases for FirewallLog model"""

    def test_create_firewall_log(self, test_db):
        """Test creating a new firewall log entry"""
        log = FirewallLog(
            timestamp=datetime.now(),
            source_ip="192.168.1.10",
            destination_ip="8.8.8.8",
            source_port=54321,
            destination_port=443,
            protocol="TCP",
            action="ALLOW",
            rule_id="RULE-100",
            description="HTTPS connection allowed",
            severity="info"
        )
        test_db.add(log)
        test_db.commit()
        test_db.refresh(log)

        assert log.id is not None
        assert log.source_ip == "192.168.1.10"
        assert log.destination_ip == "8.8.8.8"
        assert log.source_port == 54321
        assert log.destination_port == 443
        assert log.protocol == "TCP"
        assert log.action == "ALLOW"
        assert log.severity == "info"
        assert log.created_at is not None

    def test_firewall_log_actions(self, test_db):
        """Test different firewall log actions"""
        actions = ["ALLOW", "DENY", "DROP"]

        for action in actions:
            log = FirewallLog(
                timestamp=datetime.now(),
                source_ip="192.168.1.1",
                destination_ip="10.0.0.1",
                source_port=1234,
                destination_port=80,
                protocol="TCP",
                action=action,
                severity="info"
            )
            test_db.add(log)
            test_db.commit()
            test_db.refresh(log)

            assert log.action == action

    def test_firewall_log_protocols(self, test_db):
        """Test different network protocols"""
        protocols = ["TCP", "UDP", "ICMP"]

        for protocol in protocols:
            log = FirewallLog(
                timestamp=datetime.now(),
                source_ip="192.168.1.1",
                destination_ip="10.0.0.1",
                protocol=protocol,
                action="ALLOW",
                severity="info"
            )
            test_db.add(log)
            test_db.commit()
            test_db.refresh(log)

            assert log.protocol == protocol

    def test_firewall_log_severity_levels(self, test_db):
        """Test different severity levels"""
        severities = ["critical", "warning", "info", "debug"]

        for severity in severities:
            log = FirewallLog(
                timestamp=datetime.now(),
                source_ip="192.168.1.1",
                destination_ip="10.0.0.1",
                protocol="TCP",
                action="ALLOW",
                severity=severity
            )
            test_db.add(log)
            test_db.commit()
            test_db.refresh(log)

            assert log.severity == severity

    def test_firewall_log_ipv6_support(self, test_db):
        """Test IPv6 address support"""
        log = FirewallLog(
            timestamp=datetime.now(),
            source_ip="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            destination_ip="fe80::1",
            protocol="TCP",
            action="ALLOW",
            severity="info"
        )
        test_db.add(log)
        test_db.commit()
        test_db.refresh(log)

        assert log.source_ip == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        assert log.destination_ip == "fe80::1"

    def test_firewall_log_repr(self, sample_firewall_log):
        """Test firewall log __repr__ method"""
        repr_str = repr(sample_firewall_log)
        assert "FirewallLog" in repr_str
        assert str(sample_firewall_log.id) in repr_str
        assert sample_firewall_log.source_ip in repr_str
        assert sample_firewall_log.destination_ip in repr_str
        assert sample_firewall_log.action in repr_str


class TestSystemSettingModel:
    """Test cases for SystemSetting model"""

    def test_create_system_setting(self, test_db):
        """Test creating a new system setting"""
        setting = SystemSetting(
            setting_key="test_setting",
            setting_value="test_value",
            description="Test setting description",
            value_type="string"
        )
        test_db.add(setting)
        test_db.commit()
        test_db.refresh(setting)

        assert setting.id is not None
        assert setting.setting_key == "test_setting"
        assert setting.setting_value == "test_value"
        assert setting.description == "Test setting description"
        assert setting.value_type == "string"

    def test_system_setting_unique_key(self, test_db):
        """Test that setting_key must be unique"""
        setting1 = SystemSetting(
            setting_key="duplicate_key",
            setting_value="value1",
            description="First setting",
            value_type="string"
        )
        test_db.add(setting1)
        test_db.commit()

        setting2 = SystemSetting(
            setting_key="duplicate_key",  # Same key
            setting_value="value2",
            description="Second setting",
            value_type="string"
        )
        test_db.add(setting2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            test_db.commit()

    def test_system_setting_value_types(self, test_db):
        """Test different value types"""
        value_types = ["string", "integer", "boolean", "json"]

        for value_type in value_types:
            setting = SystemSetting(
                setting_key=f"setting_{value_type}",
                setting_value="test_value",
                description=f"Test {value_type} setting",
                value_type=value_type
            )
            test_db.add(setting)
            test_db.commit()
            test_db.refresh(setting)

            assert setting.value_type == value_type
