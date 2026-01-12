# Horizon Test - Prototype

ASPICE-Compliant Test Automation Platform

Automated test generation and execution from Codebeamer requirements using Jinja2 templates and pytest.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Demo Flow](#demo-flow)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)

---

## Overview

This prototype demonstrates the Horizon Test system - an automated platform that:

1. Reads requirements from Mock Codebeamer (JSON format)
2. Generates pytest tests automatically using Jinja2 templates
3. Executes tests with full evidence capture
4. Displays results on a web dashboard

### Key Features

- Template-based generation: One template handles multiple tests
- ASPICE-compliant traceability: Full requirement to test to result links
- Evidence capture: JSON evidence for audit compliance
- Docker-ready: Single command deployment
- CI/CD ready: GitHub Actions workflow included

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start the complete system
docker-compose up
```

Then open: http://localhost:8000

---

### Option 2: Manual Installation

#### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2: Generate Tests

```bash
python generator/generator.py
```

**Output:**
```
============================================================
HORIZON TEST GENERATOR
============================================================
Requirements file: mock_codebeamer/requirements.json
Templates directory: generator/templates
Output directory: tests
Total requirements: 3
============================================================

Processing: REQ-001 - eSIM Profile Download - Vodafone
  Test Type: esim_profile_download
  Priority: High
  ✓ Generated: test_req_001.py

Processing: REQ-002 - eSIM Profile Download - T-Mobile
  Test Type: esim_profile_download
  Priority: High
  ✓ Generated: test_req_002.py

Processing: REQ-003 - Network Registration - 5G SA Fallback to LTE
  Test Type: network_registration
  Priority: Medium
  ✓ Generated: test_req_003.py

============================================================
GENERATION SUMMARY
============================================================
✓ Successfully generated: 3/3
✗ Failed: 0

Generation report: tests/generation_report.json
============================================================
```

#### Step 3: Run Tests

```bash
pytest tests/ -v
```

**Output:**
```
============================================================ test session starts ============================================================
platform win32 -- Python 3.12.8, pytest-7.4.3
collected 3 items

tests/test_req_001.py::TestESIMProfileDownload::test_req_001_profile_download PASSED                                                 [ 33%]
tests/test_req_002.py::TestESIMProfileDownload::test_req_002_profile_download PASSED                                                 [ 66%]
tests/test_req_003.py::TestNetworkRegistration::test_req_003_network_registration PASSED                                            [100%]

============================================================ 3 passed in 1.23s =============================================================
```

#### Step 4: View Dashboard

```bash
# Start simple web server
python -m http.server 8000 --directory dashboard
```

Open: **http://localhost:8000**

---

## Project Structure

```
horizon-test-prototype/
│
├── mock_codebeamer/              # Mock Codebeamer Requirements
│   └── requirements.json         # 3 eSIM test requirements
│
├── generator/                    # Test Generator
│   ├── generator.py              # Main generator script
│   └── templates/                # Jinja2 templates
│       ├── esim_profile_download.j2
│       └── network_registration.j2
│
├── tests/                        # Generated pytest tests (created by generator)
│   ├── test_req_001.py
│   ├── test_req_002.py
│   └── test_req_003.py
│
├── evidence/                     # Test results & evidence
│   ├── report.html               # HTML test report
│   └── *.json                    # Evidence files
│
├── dashboard/                    # Web Dashboard
│   └── index.html                # Simple dashboard showing system status
│
├── .github/workflows/            # CI/CD Configuration
│   └── ci-cd.yml                 # GitHub Actions workflow (demo)
│
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
└── README.md                     # This file
```

---

## How It Works

### 1. Mock Codebeamer (JSON)

Requirements are stored in `mock_codebeamer/requirements.json`:

```json
{
  "id": "REQ-001",
  "title": "eSIM Profile Download - Vodafone",
  "test_type": "esim_profile_download",
  "custom_fields": {
    "mno": "Vodafone",
    "smdp_address": "smdp.vodafone.com",
    "timeout_seconds": 30
  },
  "acceptance_criteria": {
    "A1": "Profile download completes successfully",
    "E1": "HTTP response status is 200",
    ...
  }
}
```

### 2. Template Selection

Generator reads `test_type` field and selects matching template:

- `test_type: "esim_profile_download"` → uses `esim_profile_download.j2`
- `test_type: "network_registration"` → uses `network_registration.j2`

**One template handles multiple similar requirements!**

### 3. Test Generation

Jinja2 template + Requirement data = pytest test file

```python
# Generated test_req_001.py
import pytest

pytestmark = pytest.mark.codebeamer(requirement_id="REQ-001")

class TestESIMProfileDownload:
    def test_req_001_profile_download(self, test_config):
        # Test logic with full traceability
        ...
```

### 4. Test Execution

pytest runs generated tests with:
- Markers for traceability (`@pytest.mark.codebeamer`)
- Evidence capture (JSON files)
- HTML reports

### 5. Dashboard

Simple HTML dashboard shows:
- Requirements
- Generated tests
- Test results
- System status

---


---

## System Architecture

```
┌─────────────────────┐
│  Mock Codebeamer    │
│  (requirements.json)│
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Generator         │
│   (Python + Jinja2) │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   pytest Tests      │
│   (Auto-generated)  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Test Results      │
│   (Evidence + HTML) │
└─────────────────────┘
```

---

## Key Concepts

### Template Philosophy

Templates = Patterns, Not Requirements

- One template handles many requirements
- Requirements hold data (MNO, timeout, endpoints)
- Templates hold logic (test structure, validation)
- Change rarely, add thoughtfully

**Example:**
- `esim_profile_download.j2` handles REQ-001 (Vodafone) AND REQ-002 (T-Mobile)
- Different data (MNO, activation codes), same test logic
- 2 templates serve 3 requirements = 1.5 requirements per template

### Traceability

ASPICE-Compliant Full Chain:

```
Requirement (REQ-001)
    ↓
Test (test_req_001.py)
    ↓
Execution (pytest run)
    ↓
Results (evidence JSON)
    ↓
Back to Codebeamer (in production)
```

---

## Requirements

### Software

- Python 3.12+
- Docker Desktop (optional but recommended)
- Git

### Python Packages (in requirements.txt)

- `pytest==7.4.3`
- `pytest-html==4.1.1`
- `jinja2==3.1.2`
- `requests==2.31.0`

---

## Troubleshooting

### Problem: `docker-compose up` fails

**Solution:**
1. Check Docker Desktop is running (whale icon in taskbar)
2. Try: `docker-compose down` then `docker-compose up --build`

### Problem: "ModuleNotFoundError: No module named 'jinja2'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Dashboard shows blank page

**Solution:**
Make sure you're opening `http://localhost:8000` not `file:///...`

### Problem: Tests not generated

**Solution:**
Check that `mock_codebeamer/requirements.json` exists and is valid JSON:
```bash
python -m json.tool mock_codebeamer/requirements.json
```

### Problem: Port 8000 already in use

**Solution:**
```bash
# Use different port
python -m http.server 8080 --directory dashboard
```

---

## Next Steps (Beyond Prototype)

### Production Enhancements:

1. **Real Codebeamer Integration**
   - REST API connection
   - OAuth authentication
   - Webhook for requirement changes

2. **PostgreSQL Database**
   - Cache requirements locally
   - Store execution history
   - Track template usage

3. **More Templates**
   - Expand to 10-20 templates
   - Cover all test categories
   - User-contributed templates

4. **Advanced Dashboard**
   - React/Vue frontend
   - Real-time test execution
   - Traceability matrix visualization

5. **Remote Access**
   - REST API for test triggering
   - CLI tool for developers
   - Role-based access control


---

## Contact

For questions or demo requests, contact the Horizon Test team.

---

## License

Prototype for demonstration purposes.

---

Built for Horizon Connect Meeting
