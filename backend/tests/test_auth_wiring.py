"""
Test script to verify authentication middleware.

Tests that:
1. Unauthenticated requests to /api/chat return 401
2. Authenticated requests with valid token succeed
3. Hardware context is properly injected
"""

import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.session import Base, get_db

# Test database (SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_verify.db"
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


def setup_test_database():
    """Create test database tables."""
    print("Setting up test database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


def cleanup_test_database():
    """Clean up test database."""
    print("Cleaning up test database...")
    Base.metadata.drop_all(bind=engine)
    import os
    if os.path.exists(SQLALCHEMY_DATABASE_URL.replace("sqlite:///./", "")):
        os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///./", ""))
    print("Database cleaned.")


def test_unauthenticated_chat():
    """Test that unauthenticated requests to /api/chat return 401."""
    print("\n=== Test 1: Unauthenticated Chat Request ===")
    
    response = client.post(
        "/api/chat",
        json={"query": "What is ROS 2?"},
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json()["detail"]["error"] == "unauthorized"
    
    print("✅ PASSED: Unauthenticated requests are blocked\n")
    return True


def test_authenticated_chat():
    """Test that authenticated requests succeed."""
    print("\n=== Test 2: Authenticated Chat Request ===")
    
    # Register a test user
    register_response = client.post(
        "/api/auth/register",
        json={"email": "test_verify@example.com", "password": "password123"},
    )
    print(f"Register Status: {register_response.status_code}")
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"email": "test_verify@example.com", "password": "password123"},
    )
    print(f"Login Status: {login_response.status_code}")
    
    token = login_response.json()["access_token"]
    print(f"Token obtained: {token[:50]}...")
    
    # Test authenticated chat
    chat_response = client.post(
        "/api/chat",
        json={"query": "What is ROS 2?"},
        headers={"Authorization": f"Bearer {token}"},
    )
    
    print(f"Chat Status: {chat_response.status_code}")
    print(f"Chat Response: {chat_response.json()}")
    
    # Note: Chat might fail if RAG services aren't running, but auth should pass
    assert chat_response.status_code != 401, "Auth middleware failed - authenticated request rejected"
    
    print("✅ PASSED: Authenticated requests are accepted\n")
    return True


def test_hardware_profile_creation():
    """Test hardware profile creation and retrieval."""
    print("\n=== Test 3: Hardware Profile Creation ===")
    
    # Register and login
    register_response = client.post(
        "/api/auth/register",
        json={"email": "hw_test@example.com", "password": "password123"},
    )
    
    login_response = client.post(
        "/api/auth/login",
        json={"email": "hw_test@example.com", "password": "password123"},
    )
    
    token = login_response.json()["access_token"]
    
    # Create hardware profile (Sim Rig)
    hw_response = client.put(
        "/api/student/hardware-config",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "hardware_type": "sim_rig",
            "gpu_model": "RTX 4070 Ti",
            "gpu_vram_gb": 12,
            "robot_model": "Unitree Go2",
        },
    )
    
    print(f"Hardware Config Status: {hw_response.status_code}")
    print(f"Hardware Config: {hw_response.json()}")
    
    assert hw_response.status_code == 200, f"Expected 200, got {hw_response.status_code}"
    assert hw_response.json()["hardware_type"] == "sim_rig"
    assert hw_response.json()["gpu_vram_gb"] == 12
    
    print("✅ PASSED: Hardware profile created successfully\n")
    return True


def test_hardware_context_injection():
    """Test that hardware context service works correctly."""
    print("\n=== Test 4: Hardware Context Injection Service ===")
    
    from sqlalchemy.orm import Session
    from services.hardware_context_service import HardwareContextService
    from models.user import User
    from models.student_profile import StudentProfile, HardwareConfig
    
    db = TestingSessionLocal()
    
    try:
        # Create test user
        user = User(email="context_test@example.com", password_hash="test")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create profile
        profile = StudentProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        # Create hardware config
        hw_config = HardwareConfig(
            student_profile_id=profile.id,
            hardware_type="edge_kit",
            edge_kit_type="Jetson Orin Nano",
            robot_model="Unitree Go2",
        )
        db.add(hw_config)
        db.commit()
        
        # Test hardware context service
        service = HardwareContextService(db)
        context = service.get_user_context(str(user.id))
        
        print(f"Hardware Context: {context}")
        
        assert context is not None
        assert context["hardware_type"] == "edge_kit"
        assert context["pdf_pages"] == [5, 8]  # Edge Kit should reference pages 5 and 8
        
        # Test prompt injection
        system_prompt = "You are a helpful assistant."
        injected_prompt = service.inject_context(system_prompt, str(user.id))
        
        print(f"Injected Prompt contains Hardware Context: {'<Hardware Context>' in injected_prompt}")
        print(f"Injected Prompt contains Jetson: {'Jetson' in injected_prompt}")
        
        assert "<Hardware Context>" in injected_prompt
        assert "Jetson Orin Nano" in injected_prompt
        
        print("✅ PASSED: Hardware context injection working\n")
        return True
        
    finally:
        db.close()


def run_all_tests():
    """Run all authentication verification tests."""
    print("=" * 60)
    print("AUTHENTICATION MIDDLEWARE VERIFICATION TESTS")
    print("=" * 60)
    
    setup_test_database()
    
    tests = [
        ("Unauthenticated Chat", test_unauthenticated_chat),
        ("Authenticated Chat", test_authenticated_chat),
        ("Hardware Profile", test_hardware_profile_creation),
        ("Hardware Context Injection", test_hardware_context_injection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS", result))
        except AssertionError as e:
            print(f"❌ FAILED: {test_name} - {str(e)}\n")
            results.append((test_name, "FAIL", str(e)))
        except Exception as e:
            print(f"❌ ERROR: {test_name} - {str(e)}\n")
            results.append((test_name, "ERROR", str(e)))
    
    cleanup_test_database()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, status, _ in results:
        icon = "✅" if status == "PASS" else "❌"
        print(f"{icon} {test_name}: {status}")
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
