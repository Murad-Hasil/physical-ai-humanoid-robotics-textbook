"""
Unit tests for authentication endpoints.

Tests registration, login, and session management.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.session import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Create test database tables before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_student(self):
        """Test student registration."""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        # First registration
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        # Second registration should fail
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password456"},
        )
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]["message"]
    
    def test_login_student(self):
        """Test student login."""
        # Register first
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpassword"},
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]["message"]
    
    def test_get_current_user(self):
        """Test getting current authenticated user."""
        # Register and login
        register_response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_unauthorized(self):
        """Test getting current user without authentication."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401


class TestHardwareConfig:
    """Test hardware configuration endpoints."""

    def test_create_hardware_config_sim_rig(self):
        """Test creating Sim Rig hardware config."""
        # Register and login
        register_response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]
        
        # Create hardware config
        response = client.put(
            "/api/student/hardware-config",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "hardware_type": "sim_rig",
                "gpu_model": "RTX 4070 Ti",
                "gpu_vram_gb": 12,
                "ubuntu_version": "22.04",
                "robot_model": "Unitree Go2",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["hardware_type"] == "sim_rig"
        assert data["gpu_vram_gb"] == 12
    
    def test_create_hardware_config_edge_kit(self):
        """Test creating Edge Kit hardware config."""
        # Register and login
        register_response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]
        
        # Create hardware config
        response = client.put(
            "/api/student/hardware-config",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "hardware_type": "edge_kit",
                "edge_kit_type": "Jetson Orin Nano",
                "jetpack_version": "5.1",
                "robot_model": "Unitree Go2",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["hardware_type"] == "edge_kit"
        assert data["edge_kit_type"] == "Jetson Orin Nano"
    
    def test_hardware_type_validation(self):
        """Test hardware type validation."""
        # Register and login
        register_response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]
        
        # Try invalid hardware type
        response = client.put(
            "/api/student/hardware-config",
            headers={"Authorization": f"Bearer {token}"},
            json={"hardware_type": "invalid_type"},
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_sim_rig_vram_validation(self):
        """Test Sim Rig VRAM minimum validation."""
        # Register and login
        register_response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]
        
        # Try to create Sim Rig with < 12GB VRAM
        response = client.put(
            "/api/student/hardware-config",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "hardware_type": "sim_rig",
                "gpu_vram_gb": 8,  # Should be >= 12
            },
        )
        
        assert response.status_code == 400
        assert "12GB" in response.json()["detail"]["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
