# Quickstart: Hardware-Aware Authentication and Personalization

**Created**: 2026-03-16
**Feature**: 001-hardware-aware-auth
**Purpose**: Get developers up and running with student authentication, PDF-specified hardware profiles, and curriculum tracking quickly

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **Node.js 20.x** installed (for Better-Auth and Docusaurus)
- **Git** for version control
- **GitHub Developer Account** (for OAuth app registration)
- **Neon Account** (free tier) for PostgreSQL database

---

## 1. Environment Setup (5 minutes)

### 1.1 Clone and Navigate

```bash
cd /home/brownie/projects/physical-ai-docusaurus-textbook
git checkout 001-hardware-aware-auth
```

### 1.2 Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New dependencies added:**
```
better-auth>=0.1.0         # Authentication framework
sqlalchemy>=2.0.0          # Database ORM
alembic>=1.13.0            # Database migrations
bcrypt>=4.1.0              # Password hashing
python-jose[cryptography]>=3.3.0  # JWT handling
```

### 1.3 Install Frontend Dependencies

```bash
cd ../docusaurus-textbook
npm install
npm install @better-auth/react better-auth
```

---

## 2. Database Setup (3 minutes)

### 2.1 Create Neon Database

1. Go to [neon.tech](https://neon.tech) and sign in
2. Create a new project: `physical-ai-auth`
3. Copy the connection string (looks like `postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname`)

### 2.2 Configure Environment Variables

**Backend `.env` file:**

```bash
# Existing variables (keep these)
GROK_API_KEY=your_grok_api_key
QDRANT_URL=http://localhost:6333
EMBEDDING_MODEL=all-MiniLM-L6-v2

# New authentication variables
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/auth?sslmode=require
BETTER_AUTH_SECRET=your_secret_key_at_least_32_characters
BETTER_AUTH_URL=http://localhost:3000

# GitHub OAuth (get these from GitHub - see next section)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# JWT Configuration
JWT_SECRET=your_jwt_secret_at_least_32_characters
JWT_EXPIRY_HOURS=24

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# PDF Hardware Configuration (optional defaults)
PDF_HARDWARE_REALITY_PAGE=5
PDF_INFERENCE_SIM_TO_REAL_PAGE=8
```

**Generate secure secrets:**

```bash
# Generate Better-Auth secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.3 Run Database Migrations

```bash
cd backend
alembic upgrade head
```

This creates the following tables:
- `users` (managed by Better-Auth)
- `student_profiles`
- `hardware_configs` (with PDF-specified hardware enums)
- `curriculum_progress` (Weeks 1-13)
- `chat_sessions`
- `chat_messages`

---

## 3. GitHub OAuth Setup (5 minutes)

### 3.1 Register GitHub OAuth App

1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Physical AI Textbook (Development)`
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization callback URL**: `http://localhost:3000/api/auth/github/callback`
4. Click "Register application"
5. Copy **Client ID**
6. Click "Generate a new client secret" and copy it

### 3.2 Add to `.env`

```bash
GITHUB_CLIENT_ID=Iv1.abcdef1234567890
GITHUB_CLIENT_SECRET=your_client_secret_here
```

---

## 4. Start Services (2 minutes)

### 4.1 Start Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### 4.2 Start Frontend

```bash
cd ../docusaurus-textbook
npm run start
```

Frontend runs at: `http://localhost:3000`

---

## 5. Verify Setup (3 minutes)

### 5.1 Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-03-16T...",
  "services": {
    "qdrant": true,
    "database": true
  }
}
```

### 5.2 Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepassword123"
  }'
```

Expected: Student created with session token

### 5.3 Test Authentication

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepassword123"
  }'
```

Expected: Login successful with session token

### 5.4 Test Protected Endpoint

```bash
curl http://localhost:8000/api/auth/me \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN"
```

Expected: User object

---

## 6. Test Hardware Configuration (3 minutes)

### 6.1 Create Sim Rig Hardware Config

```bash
curl -X PUT http://localhost:8000/api/student/hardware-config \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN" \
  -d '{
    "hardware_type": "sim_rig",
    "gpu_model": "RTX 4070 Ti",
    "gpu_vram_gb": 12,
    "ubuntu_version": "22.04",
    "robot_model": "Unitree Go2",
    "sensor_model": "RealSense D435i"
  }'
```

### 6.2 Create Edge Kit Hardware Config

```bash
curl -X PUT http://localhost:8000/api/student/hardware-config \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN" \
  -d '{
    "hardware_type": "edge_kit",
    "edge_kit_type": "Jetson Orin Nano",
    "jetpack_version": "5.1",
    "robot_model": "Unitree Go2",
    "sensor_model": "RealSense D435i"
  }'
```

### 6.3 Test Hardware-Aware Chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN" \
  -d '{
    "query": "How do I deploy my SLAM algorithm?"
  }'
```

**Expected for Edge Kit**: Response includes Jetson Orin-specific optimization advice, references PDF Page 8 (Inference/Sim-to-Real)

**Expected for Sim Rig**: Response includes workstation-optimized commands, assumes Ubuntu 22.04, references PDF Page 5 (Hardware Reality)

Response should include:
```json
{
  "response": "...",
  "hardware_context_used": true,
  "hardware_type_applied": "edge_kit",
  "pdf_pages_referenced": [5, 8]
}
```

---

## 7. Test Curriculum Progress Tracking (2 minutes)

### 7.1 Record Week Completion

```bash
curl -X POST http://localhost:8000/api/student/curriculum-progress \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN" \
  -d '{
    "week_number": 1,
    "module_id": "01-ros-2",
    "score_percentage": 85,
    "notes": "Completed ROS 2 fundamentals"
  }'
```

### 7.2 View Progress

```bash
curl http://localhost:8000/api/student/curriculum-progress \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_TOKEN"
```

Expected: Array of completed weeks with timestamps

---

## 8. Frontend Integration (5 minutes)

### 8.1 Create Auth Hook

Create `docusaurus-textbook/src/hooks/useAuth.js`:

```javascript
import { createAuthClient } from 'better-auth/react';

const authClient = createAuthClient({
  baseURL: 'http://localhost:3000',
});

export function useAuth() {
  const { data: session, isPending, error } = authClient.useSession();
  
  return {
    user: session?.user,
    loading: isPending,
    error,
    login: authClient.signIn,
    logout: authClient.signOut,
    register: authClient.signUp,
  };
}
```

### 8.2 Create Hardware Profile Form

Create `docusaurus-textbook/src/components/HardwareProfileForm.jsx`:

```javascript
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export function HardwareProfileForm() {
  const { user } = useAuth();
  const [hardwareType, setHardwareType] = useState('sim_rig');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const response = await fetch('/api/student/hardware-config', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(Object.fromEntries(formData)),
    });
    
    if (response.ok) {
      alert('Hardware profile saved!');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <h3>Hardware Setup (PDF Page 5)</h3>
      
      <label>
        Hardware Type:
        <select 
          name="hardware_type" 
          value={hardwareType}
          onChange={(e) => setHardwareType(e.target.value)}
        >
          <option value="sim_rig">Sim Rig (Workstation)</option>
          <option value="edge_kit">Edge Kit (Jetson)</option>
        </select>
      </label>
      
      {hardwareType === 'sim_rig' ? (
        <>
          <label>
            GPU Model:
            <select name="gpu_model">
              <option value="RTX 4070 Ti">RTX 4070 Ti (12GB)</option>
              <option value="RTX 4080">RTX 4080 (16GB)</option>
              <option value="RTX 4090">RTX 4090 (24GB)</option>
            </select>
          </label>
          <label>
            VRAM (GB):
            <input type="number" name="gpu_vram_gb" min="12" defaultValue="12" />
          </label>
        </>
      ) : (
        <>
          <label>
            Jetson Device:
            <select name="edge_kit_type">
              <option value="Jetson Orin Nano">Jetson Orin Nano</option>
              <option value="Jetson Orin NX">Jetson Orin NX</option>
              <option value="Jetson AGX Orin">Jetson AGX Orin</option>
            </select>
          </label>
        </>
      )}
      
      <label>
        Robot Model:
        <select name="robot_model">
          <option value="Unitree Go2">Unitree Go2</option>
          <option value="Unitree G1">Unitree G1</option>
          <option value="Proxy">Proxy (Simulation)</option>
        </select>
      </label>
      
      <label>
        Sensor:
        <select name="sensor_model">
          <option value="RealSense D435i">RealSense D435i</option>
          <option value="RealSense D455">RealSense D455</option>
          <option value="OAK-D">OAK-D</option>
        </select>
      </label>
      
      <button type="submit">Save Hardware Profile</button>
    </form>
  );
}
```

### 8.3 Add to Docusaurus Navbar

Edit `docusaurus-textbook/docusaurus.config.js`:

```javascript
themeConfig: {
  navbar: {
    items: [
      // ... existing items
      {
        type: 'custom-loginButton',
        position: 'right',
      },
    ],
  },
  customFields: {
    authConfig: {
      backendUrl: 'http://localhost:8000',
    },
  },
},
```

---

## 9. Common Issues and Solutions

### Issue: Database connection fails

**Error**: `could not connect to server`

**Solution**:
1. Check DATABASE_URL format
2. Ensure `?sslmode=require` is appended
3. Verify Neon project is active
4. Check firewall settings

### Issue: GitHub OAuth returns 401

**Error**: `redirect_uri_mismatch`

**Solution**:
1. Verify callback URL in GitHub OAuth app matches exactly
2. Ensure no trailing slashes
3. Check BETTER_AUTH_URL is set correctly

### Issue: Hardware config validation fails

**Error**: `invalid_hardware_config`

**Solution**:
1. Ensure hardware_type is "sim_rig" or "edge_kit"
2. Verify robot_model is one of: "Unitree Go2", "Unitree G1", "Proxy"
3. Check edge_kit_type is one of: "Jetson Orin Nano", "Jetson Orin NX", "Jetson AGX Orin"
4. Ensure GPU VRAM >= 12GB for sim_rig (PDF Page 5 requirement)

### Issue: Hardware context not injected in chat

**Error**: Chat responses don't include hardware context

**Solution**:
1. Verify hardware config exists: `GET /api/student/hardware-config`
2. Check backend logs for hardware_context_service
3. Ensure session token is included in chat request
4. Verify PDF Page 5 and Page 8 references are being applied

### Issue: Week number validation fails

**Error**: `invalid_week_number`

**Solution**:
- Ensure week_number is between 1 and 13 (inclusive)
- Verify module_id matches pattern (e.g., "01-ros-2", "02-gazebo")

---

## 10. Next Steps

After completing quickstart:

1. **Read API Documentation**: `/specs/001-hardware-aware-auth/contracts/api-contracts.yaml`
2. **Review Data Model**: `/specs/001-hardware-aware-auth/data-model.md`
3. **Implement Tasks**: See `/specs/001-hardware-aware-auth/tasks.md` (created by `/sp.tasks`)
4. **Run Tests**: `cd backend && pytest tests/`

---

## 11. Development Workflow

### Running Tests

```bash
cd backend
pytest tests/unit/test_auth.py -v
pytest tests/integration/test_hardware_context_service.py -v
pytest tests/integration/test_curriculum_progress.py -v
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Debugging

Enable debug logging in `.env`:

```bash
LOG_LEVEL=DEBUG
BETTER_AUTH_DEBUG=true
HARDWARE_CONTEXT_DEBUG=true
```

View logs:

```bash
# Backend logs
tail -f backend/logs/app.log

# Hardware context injections
grep "hardware_context" backend/logs/app.log

# Database queries
docker logs postgres
```

---

## 12. PDF Reference Guide

**PDF Page 5 - "Hardware Reality"**:
- Sim Rig: RTX 4070 Ti+ (12GB VRAM minimum), Ubuntu 22.04
- Edge Kit: Jetson Orin Nano/NX, resource-constrained deployment
- Robots: Unitree Go2 (quadruped), Unitree G1 (humanoid), Proxy (simulation)
- Sensors: RealSense D435i (depth + IMU)

**PDF Page 8 - "Inference / Sim-to-Real"**:
- Edge Kit users should receive inference-optimized advice
- Sim-to-Real deployment guidance for Jetson devices
- Resource-efficient commands and configurations

---

**Estimated Total Setup Time**: 25 minutes

**Support**: For issues not covered here, check the full documentation or open an issue.
