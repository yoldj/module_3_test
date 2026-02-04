"""
Test cases for Pydantic schemas
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.schemas.firewall_log import (
    FirewallLogCreate,
    FirewallLogResponse,
    FirewallLogFilter,
    FirewallLogStats
)


class TestUserSchemas:
    """Test cases for User schemas"""

    def test_user_create_valid(self):
        """Test creating valid UserCreate schema"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
            "role": "viewer"
        }
        user = UserCreate(**user_data)

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"
        assert user.role == "viewer"

    def test_user_create_username_too_short(self):
        """Test UserCreate with username too short"""
        user_data = {
            "username": "ab",  # Too short (min 3)
            "email": "test@example.com",
            "password": "password123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_invalid_email(self):
        """Test UserCreate with invalid email"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid email format
            "password": "password123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_password_too_short(self):
        """Test UserCreate with password too short"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345"  # Too short (min 6)
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_invalid_role(self):
        """Test UserCreate with invalid role"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "invalid_role"  # Invalid role
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_valid_roles(self):
        """Test UserCreate with all valid roles"""
        valid_roles = ["admin", "operator", "viewer"]

        for role in valid_roles:
            user_data = {
                "username": f"user_{role}",
                "email": f"{role}@example.com",
                "password": "password123",
                "role": role
            }
            user = UserCreate(**user_data)
            assert user.role == role

    def test_user_update_partial(self):
        """Test UserUpdate with partial data"""
        update_data = {
            "email": "newemail@example.com",
            "full_name": "New Name"
        }
        user_update = UserUpdate(**update_data)

        assert user_update.email == "newemail@example.com"
        assert user_update.full_name == "New Name"
        assert user_update.password is None
        assert user_update.is_active is None

    def test_user_login_valid(self):
        """Test valid UserLogin schema"""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login = UserLogin(**login_data)

        assert login.username == "testuser"
        assert login.password == "password123"


class TestFirewallLogSchemas:
    """Test cases for FirewallLog schemas"""

    def test_firewall_log_create_valid(self):
        """Test creating valid FirewallLogCreate schema"""
        log_data = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "source_port": 12345,
            "destination_port": 80,
            "protocol": "TCP",
            "action": "ALLOW",
            "rule_id": "RULE-001",
            "description": "Test log entry",
            "severity": "info"
        }
        log = FirewallLogCreate(**log_data)

        assert log.source_ip == "192.168.1.100"
        assert log.destination_ip == "10.0.0.1"
        assert log.protocol == "TCP"
        assert log.action == "ALLOW"
        assert log.severity == "info"

    def test_firewall_log_invalid_protocol(self):
        """Test FirewallLogCreate with invalid protocol"""
        log_data = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "protocol": "INVALID",  # Invalid protocol
            "action": "ALLOW",
            "severity": "info"
        }

        with pytest.raises(ValidationError):
            FirewallLogCreate(**log_data)

    def test_firewall_log_invalid_action(self):
        """Test FirewallLogCreate with invalid action"""
        log_data = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "protocol": "TCP",
            "action": "INVALID",  # Invalid action
            "severity": "info"
        }

        with pytest.raises(ValidationError):
            FirewallLogCreate(**log_data)

    def test_firewall_log_invalid_severity(self):
        """Test FirewallLogCreate with invalid severity"""
        log_data = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "protocol": "TCP",
            "action": "ALLOW",
            "severity": "invalid"  # Invalid severity
        }

        with pytest.raises(ValidationError):
            FirewallLogCreate(**log_data)

    def test_firewall_log_port_range(self):
        """Test FirewallLogCreate with port validation"""
        # Valid port
        log_data = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "source_port": 80,
            "destination_port": 443,
            "protocol": "TCP",
            "action": "ALLOW",
            "severity": "info"
        }
        log = FirewallLogCreate(**log_data)
        assert log.source_port == 80
        assert log.destination_port == 443

        # Invalid port (too high)
        log_data_invalid = {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "source_port": 70000,  # Greater than 65535
            "protocol": "TCP",
            "action": "ALLOW",
            "severity": "info"
        }

        with pytest.raises(ValidationError):
            FirewallLogCreate(**log_data_invalid)

    def test_firewall_log_case_insensitive_protocol(self):
        """Test that protocol accepts both upper and lower case"""
        protocols = ["TCP", "tcp", "UDP", "udp", "ICMP", "icmp"]

        for protocol in protocols:
            log_data = {
                "timestamp": datetime.now(),
                "source_ip": "192.168.1.100",
                "destination_ip": "10.0.0.1",
                "protocol": protocol,
                "action": "ALLOW",
                "severity": "info"
            }
            log = FirewallLogCreate(**log_data)
            assert log.protocol == protocol

    def test_firewall_log_filter_pagination(self):
        """Test FirewallLogFilter with pagination"""
        filter_data = {
            "page": 2,
            "limit": 100
        }
        log_filter = FirewallLogFilter(**filter_data)

        assert log_filter.page == 2
        assert log_filter.limit == 100

    def test_firewall_log_filter_defaults(self):
        """Test FirewallLogFilter default values"""
        log_filter = FirewallLogFilter()

        assert log_filter.page == 1
        assert log_filter.limit == 50
        assert log_filter.source_ip is None
        assert log_filter.action is None

    def test_firewall_log_filter_invalid_page(self):
        """Test FirewallLogFilter with invalid page number"""
        filter_data = {
            "page": 0  # Invalid (must be >= 1)
        }

        with pytest.raises(ValidationError):
            FirewallLogFilter(**filter_data)

    def test_firewall_log_filter_limit_too_high(self):
        """Test FirewallLogFilter with limit too high"""
        filter_data = {
            "limit": 2000  # Too high (max 1000)
        }

        with pytest.raises(ValidationError):
            FirewallLogFilter(**filter_data)

    def test_firewall_log_filter_date_range(self):
        """Test FirewallLogFilter with date range"""
        now = datetime.now()
        filter_data = {
            "date_from": now,
            "date_to": now
        }
        log_filter = FirewallLogFilter(**filter_data)

        assert log_filter.date_from == now
        assert log_filter.date_to == now

    def test_firewall_log_stats_schema(self):
        """Test FirewallLogStats schema"""
        stats_data = {
            "total_logs": 1000,
            "allowed_count": 800,
            "denied_count": 150,
            "dropped_count": 50,
            "critical_count": 10,
            "warning_count": 40,
            "top_source_ips": [
                {"ip": "192.168.1.1", "count": 100},
                {"ip": "192.168.1.2", "count": 80}
            ],
            "top_destination_ips": [
                {"ip": "8.8.8.8", "count": 200},
                {"ip": "1.1.1.1", "count": 150}
            ]
        }
        stats = FirewallLogStats(**stats_data)

        assert stats.total_logs == 1000
        assert stats.allowed_count == 800
        assert len(stats.top_source_ips) == 2
        assert len(stats.top_destination_ips) == 2
