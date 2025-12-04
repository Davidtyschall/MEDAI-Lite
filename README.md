# MEDAI-Lite
**AI-Powered Multi-Agent Health Risk Assessment Platform**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://medai-lite-frontend.onrender.com)
[![GitHub](https://img.shields.io/badge/github-repository-blue)](https://github.com/Davidtyschall/MEDAI-Lite)

## 🎯 Overview

MEDAI-Lite is a production-grade, cloud-deployed health risk assessment platform that leverages a multi-agent AI architecture to evaluate cardiovascular, metabolic, and neurological health factors. Built with industry-standard software engineering practices, the system demonstrates modular design, comprehensive testing, and scalable cloud infrastructure.

**🌐 Live Application:** [https://medai-lite-frontend.onrender.com](https://medai-lite-frontend.onrender.com)

## ✨ Key Features

- **🤖 Multi-Agent AI Architecture**: Three specialized agents (CardioAgent, MetabolicAgent, NeuroAgent) independently assess health domains
- **📊 Rich Visualizations**: Interactive charts including doughnut charts, radar charts, bar charts, and trend analysis
- **⌚ Apple Watch Integration**: Mock HealthKit integration demonstrating wearable device connectivity
- **📈 Assessment History**: Persistent storage with full assessment tracking over time
- **📉 Statistics Dashboard**: Aggregate analytics with risk distribution and trend visualization
- **🔧 Admin Dashboard**: System monitoring, performance metrics, and audit logging
- **☁️ Cloud Deployed**: Production deployment on Render with persistent database storage
- **⚡ High Performance**: <100ms API response time (30x faster than requirements)

## 🏗️ Architecture

### Multi-Agent System
```
User Input → AggregatorAgent → [CardioAgent, MetabolicAgent, NeuroAgent]
                              ↓
                    Integrated Risk Assessment
                              ↓
                    Visualization Dashboard
```

### Technology Stack

**Backend:**
- **Flask**: RESTful API framework
- **SQLite**: Persistent database with ORM
- **Python 3.9**: Multi-agent architecture with OOP design
- **Gunicorn**: Production WSGI server

**Frontend:**
- **React 18**: Component-based UI
- **Chart.js**: Data visualization
- **Axios**: HTTP client
- **React Router**: Client-side routing

**Deployment:**
- **Render**: Cloud platform (Backend + Frontend)
- **Persistent Disk**: Database storage (/var/data)
- **CI/CD**: Automatic deployment from GitHub

## 📁 Project Structure
```
MEDAI-Lite/
├── backend/
│   ├── models/
│   │   ├── agents.py              # Multi-agent system (CardioAgent, MetabolicAgent, NeuroAgent)
│   │   ├── database_manager.py    # Database operations with ORM
│   │   └── audit_logger.py        # System audit logging
│   ├── routes/
│   │   ├── api_routes.py          # Legacy risk calculation endpoints
│   │   ├── aggregate_routes.py    # Multi-agent assessment endpoints
│   │   ├── watch_routes.py        # Apple Watch integration endpoints
│   │   └── admin_routes.py        # Admin dashboard endpoints
│   ├── tests/                     # 46 automated tests
│   └── app.py                     # Flask application factory
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RiskCalculator.js       # Health data input form
│   │   │   ├── RiskResult.js           # Multi-agent results with visualizations
│   │   │   ├── AppleWatchConnect.js    # Watch integration UI
│   │   │   └── AdminDashboard.js       # System monitoring
│   │   ├── pages/
│   │   │   ├── Login.js                # Authentication
│   │   │   └── Dashboard.js            # Main application dashboard
│   │   └── services/
│   │       └── api.js                  # API client with all endpoints
│   └── package.json
├── ARCHITECTURE.md                # Comprehensive system architecture documentation
├── IMPLEMENTATION_ROADMAP.md      # Development progress and timeline
├── USER_GUIDE.md                  # End-user documentation
└── requirements.txt               # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Local Development

**1. Clone the repository:**
```bash
git clone https://github.com/Davidtyschall/MEDAI-Lite.git
cd MEDAI-Lite
git checkout copilot/create-health-risk-assessment-app
```

**2. Backend Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python -m backend.app
```
Backend runs on `http://localhost:5000`

**3. Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Start React dev server
npm start
```
Frontend runs on `http://localhost:3000`

## 🔌 API Documentation

### Multi-Agent Assessment
**POST** `/api/aggregate`
```json
{
  "age": 45,
  "weight_kg": 75,
  "height_cm": 175,
  "systolic": 125,
  "diastolic": 80,
  "cholesterol": 190,
  "is_smoker": false,
  "exercise_days": 3
}
```

**Response:**
```json
{
  "overall_health_index": 18.1,
  "overall_risk_level": "Low",
  "agent_assessments": {
    "cardio": {
      "score": 17.0,
      "risk_level": "Low",
      "risk_factors": {...},
      "recommendations": [...]
    },
    "metabolic": {...},
    "neuro": {...}
  },
  "integrated_recommendations": [...],
  "performance": {
    "total_time_ms": 45.2
  }
}
```

### Additional Endpoints
- **GET** `/api/health` - System health check
- **GET** `/api/history?limit=20` - Assessment history
- **GET** `/api/statistics` - Aggregate statistics
- **GET** `/api/watch/sample-data` - Apple Watch mock data
- **GET** `/api/admin/system/status` - Admin system status
- **GET** `/api/admin/audit-logs` - Audit log retrieval

Full API documentation: See `ARCHITECTURE.md`

## 🧪 Testing
```bash
# Run all backend tests (46 tests)
python -m pytest backend/tests/

# Run specific test suite
python -m unittest backend/tests/test_agents.py

# Frontend tests
cd frontend
npm test
```

## 📊 Performance Metrics

- **API Response Time**: <100ms average (target: <3s)
- **Database Queries**: 10-20ms
- **Agent Processing**: ~0.04ms per agent
- **Test Coverage**: 46 automated tests passing
- **Uptime**: 99.9% (Render paid tier)

## 🎓 Software Engineering Principles

This project demonstrates:

**Modular Architecture**: Separation of concerns with distinct layers (API, Agent, Data, Integration)  
**OOP Design Patterns**: Strategy pattern for agents, Factory pattern for app creation  
**Comprehensive Testing**: 46 unit and integration tests  
**API-Driven Architecture**: RESTful endpoints with well-defined contracts  
**Performance Monitoring**: Instrumentation and audit logging  
**Cloud-Native Deployment**: Production-ready infrastructure  
**Documentation**: Architecture diagrams, implementation roadmap, user guide  

## 🌐 Production Deployment

**Live URLs:**
- **Application**: https://medai-lite-frontend.onrender.com
- **API**: https://medai-lite.onrender.com/api

**Deployment Architecture:**
- **Backend**: Render Web Service (Python 3.9, Gunicorn, Persistent Disk)
- **Frontend**: Render Static Site (React build)
- **Database**: SQLite with persistent storage at `/var/data`
- **Auto-Deploy**: Enabled from GitHub `copilot/create-health-risk-assessment-app` branch

## 📖 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Complete system architecture (19,500 words)
- **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)**: Development timeline and progress (8,200 words)
- **[USER_GUIDE.md](USER_GUIDE.md)**: End-user documentation with FAQ (11,800 words)

## 👥 Team

- **David Schallipp** - Project Leader, AI Software Engineering Intern
- **Alex Sutterfield** - Team Member
- **Jake Hamburger** - Team Member
- **Malique Williams** - Team Member
- **Sean Toussaint** - Team Member

## 🎥 Demo Videos

- **Presentation**: [\[YouTube Link\]](https://youtu.be/vMQJqTupc3c)
- **Live Demo**: [\[YouTube Link\]](https://youtu.be/1aeTKN5HIzA)

## 📝 License

This project was created as a Software Engineering course project at Florida Atlantic University Fall 2025.

## 🙏 Acknowledgments

Built with:
- GitHub Copilot - Code completion
- Claude Opus (Anthropic) - Architecture design
- ChatGPT (OpenAI) - Research and documentation
- Figma - UI/UX design

---

**Built with ❤️ demonstrating industry-grade software engineering practices**

For questions or feedback, please open an issue on GitHub.