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

## Demo Flow (For Meeting Presentation)

### 5-Minute Demo Script

#### Step 1: Show Requirements (30 sec)

Open: `mock_codebeamer/requirements.json`

> "Here are 3 realistic automotive requirements from our Mock Codebeamer. Two eSIM profile downloads (Vodafone and T-Mobile) and one network registration fallback test. Notice the custom fields: MNO, timeout, activation codes - this is the data that varies between tests."

#### Step 2: Show Templates (30 sec)

Open: `generator/templates/esim_profile_download.j2`

> "This is our Jinja2 template. One template handles both Vodafone and T-Mobile tests. The template contains the test logic and structure, while requirements provide the data. This is our philosophy: Templates = Patterns, Not Requirements."

#### Step 3: Generate Tests (1 min)

```bash
python generator/generator.py
```

> "The generator reads the JSON, looks at the test_type field, selects the matching template, and generates pytest code automatically. Watch - 3 requirements become 3 complete test files in 2 seconds."

#### Step 4: Show Generated Code (1 min)

Open: `tests/test_req_001.py`

> "Here's the generated pytest file. Full traceability with markers, evidence capture, acceptance criteria validation. This is production-quality code - not a toy. It includes proper fixtures, error handling, and ASPICE-compliant documentation."

#### Step 5: Run Tests (1 min)

```bash
pytest tests/ -v
```

> "Now we execute the tests. In this prototype they're simulating API calls, but the structure is identical to production. Green checkmarks - all tests pass. Evidence is captured for each test."

#### Step 6: Show Dashboard (1 min)

Open: http://localhost:8000

> "Here's the dashboard. Shows requirements, generated tests, system flow. In production, this would display real-time test execution status and sync results back to Codebeamer."

#### Step 7: Show CI/CD Config (30 sec)

Open: `.github/workflows/ci-cd.yml`

> "And here's the GitHub Actions workflow. This shows how it runs in production: on every push, tests generate automatically, execute, and results sync back. Zero maintenance - it's SaaS."

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

## Demo Tips

### What to Show

- Requirements JSON - Real automotive scenarios
- Template code - Show Jinja2 variables
- Generation process - Live terminal output
- Generated tests - Production-quality code
- Test execution - Green checkmarks
- Dashboard - Visual overview

### What to Say

> "This prototype demonstrates the complete flow from requirement to execution. The key innovation is template-based generation - one template handles many similar requirements. This is how we achieve 90% reduction in manual test writing while maintaining ASPICE compliance."

### Questions to Expect

**Q: How do you handle edge cases?**
> "Templates include error handling and validation. Edge cases are captured in acceptance criteria, which drive the test assertions."

**Q: What about maintenance?**
> "That's the beauty - when we update a template, all tests using it are automatically improved. No need to modify 100+ individual test files."

**Q: How long to implement for real?**
> "Phase 1 (infrastructure + 5 tests): 4 weeks. Phase 2 (scale to 50+ tests): 4 weeks. Phase 3 (advanced features): 4 weeks. Total: 3 months to production."

---

## Contact

For questions or demo requests, contact the Horizon Test team.

---

## License

Prototype for demonstration purposes.

---

Built for Horizon Connect Meeting
