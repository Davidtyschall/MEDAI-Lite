# MEDAI-Lite Architecture Documentation

## System Overview

MEDAI-Lite is a modular, AI-assisted health risk assessment and visualization platform built with Flask backend and React frontend. The system uses a multi-agent architecture to provide comprehensive health risk analysis across cardiovascular, metabolic, and neurological domains.

**Current Status**: Core features complete, production-ready for course demonstration

## Design Philosophy

### Core Principles
1. **Modularity**: Disease-specific agents for extensibility and maintainability
2. **Separation of Concerns**: Clear boundaries between agent, data, API, and presentation layers
3. **Performance**: Sub-100ms response time achieved (requirement: ≤3s)
4. **Testability**: Comprehensive unit and integration test coverage
5. **User Experience**: Intuitive UI with data import from Apple Watch, real-time visualizations

## Architecture Layers

### 1. Agent Layer (Multi-Agent Health Assessment)

#### Base Agent Pattern
```python
BaseAgent (Abstract Base Class)
├── assess_risk() - Abstract method for risk calculation
├── get_recommendations() - Abstract method for health advice
├── assess_with_timing() - Performance monitoring wrapper
└── validate_data() - Input validation and sanitization
```

#### Specialized Assessment Agents

**1. CardioAgent (Weight: 35%)**
- Cardiovascular risk assessment
- Blood pressure classification (6 categories: Optimal → Hypertensive Crisis)
- Total cholesterol analysis (Desirable/Borderline/High)
- Smoking impact quantification
- Age-based cardiovascular risk factors
- Exercise cardio benefits calculation

**2. MetabolicAgent (Weight: 35%)**
- BMI calculation and 6-tier classification (Underweight → Obese Class III)
- Metabolic syndrome risk indicators
- Lipid profile evaluation
- Weight management recommendations
- Exercise metabolic impact assessment

**3. NeuroAgent (Weight: 30%)**
- Stroke risk assessment
- Cognitive aging evaluation
- Vascular brain health analysis
- Blood pressure impact on neurological health
- Neuroprotective lifestyle factors

#### AggregatorAgent (Orchestration)
- Coordinates all specialized agents in parallel
- Computes weighted overall health index (0-100 scale)
- Identifies critical health areas requiring attention
- Generates integrated, cross-domain recommendations
- Performance monitoring and optimization
- Response structure:
  ```json
  {
    "overall_health_index": 14.55,
    "overall_risk_level": "Low",
    "agent_assessments": {
      "cardio": {...},
      "metabolic": {...},
      "neuro": {...}
    },
    "integrated_recommendations": [...],
    "critical_areas": [],
    "performance": {"total_time_ms": 0.12}
  }
  ```

### 2. Data Layer

#### DatabaseManager
- SQLite database with indexed queries
- User CRUD operations
- Assessment history storage with timestamps
- Statistics aggregation (avg risk, BMI, counts)
- Query optimization for performance
- Schema:
  - `users` table: user demographics
  - `assessments` table: risk calculation results
  - Indexes on `user_id`, `timestamp`, `risk_level`

#### AuditLogger
- Security and compliance event tracking
- User action logging (CREATE, READ, UPDATE, DELETE, EXPORT)
- IP address and user agent capture
- Indexed timestamp queries for analytics
- Automatic log rotation (90-day default retention)
- Statistics and reporting capabilities
- Schema:
  - `audit_logs` table with indexed `timestamp` and `user_id`

### 3. Integration Layer

#### AppleWatchMock
**Purpose**: Simulates HealthKit data for demonstration and testing

**Capabilities**:
- Connection/disconnection workflow with session management
- Heart rate data generation (resting: 60-80 bpm, active: 120-160 bpm)
- Blood oxygen saturation (SpO2: 95-100%)
- Activity summaries (steps, calories, distance, active minutes)
- Sleep tracking with phases (deep/REM/light/awake)
- Multi-type workout history (running, cycling, swimming, strength)
- Current vital signs snapshot
- Full data export for form auto-population
- Sample data generation optimized for risk calculator

**Data Generation**:
- Age: 45-65 (moderate risk range)
- Vitals: Realistic ranges based on health profiles
- Activity: 3-5 days/week exercise patterns
- Smoking status: Random boolean

**Production Notes**: 
- Replace with actual HealthKit API integration
- Implement OAuth 2.0 authentication
- Add HIPAA-compliant data encryption
- Implement real-time data streaming
- Add user consent management

### 4. API Layer

#### REST Endpoints (18 Total)

**Health Check**
- `GET /api/health` - System health verification

**Assessment APIs**
- `POST /api/risk` - Simple single-agent risk calculation (legacy, maintained for compatibility)
- `POST /api/aggregate` - **PRIMARY ENDPOINT** - Multi-agent comprehensive assessment
- `GET /api/aggregate/performance` - Performance metrics and timing data
- `GET /api/aggregate/agents` - Available agents information

**History & Statistics**
- `GET /api/history` - User assessment history (paginated, filterable by user_id)
- `GET /api/history/<id>` - Single assessment details
- `DELETE /api/history/<id>` - Delete assessment record
- `GET /api/statistics` - Aggregated statistics (avg risk, BMI, counts by risk level)

**Apple Watch Integration**
- `POST /api/watch/connect` - Establish watch connection (returns session_key)
- `POST /api/watch/disconnect` - Terminate watch session
- `GET /api/watch/vitals` - Current vital signs snapshot
- `GET /api/watch/heart-rate` - Heart rate history data
- `GET /api/watch/activity` - Activity summaries and metrics
- `GET /api/watch/sleep` - Sleep tracking data with phases
- `GET /api/watch/workouts` - Workout history by type
- `GET /api/watch/export` - Full health data export
- `GET /api/watch/sample-data` - **USED BY FRONTEND** - Form-ready sample data

**Admin APIs**
- `GET /api/admin/system/status` - System health and assessment statistics
- `GET /api/admin/system/metrics` - Detailed performance metrics with risk distribution
- `GET /api/admin/audit-logs` - Paginated audit logs with filtering (max 200 per request)
- `GET /api/admin/audit-logs/stats` - Audit statistics for specified time period
- `POST /api/admin/audit-logs/cleanup` - Manual log cleanup trigger

**API Design Principles**:
- RESTful conventions
- JSON request/response format
- HTTP status codes (200, 400, 404, 500)
- Error messages with context
- CORS enabled for development
- Request validation and sanitization

### 5. Frontend Layer (React)

#### Component Hierarchy

```
App.js
├── LoginPage.js (Simple username-based auth)
└── Dashboard.js (Main application shell)
    ├── Navigation Tabs
    │   ├── 📊 Risk Calculator (default)
    │   ├── 📋 History
    │   ├── 📈 Statistics
    │   └── 🔧 Admin (NEW)
    │
    ├── RiskCalculator.js ✅ COMPLETE
    │   ├── AppleWatchConnect.js ✅ COMPLETE
    │   │   ├── Connect/disconnect button with loading states
    │   │   ├── Connection status indicator (pulsing green dot)
    │   │   ├── Data preview modal with health metrics grid
    │   │   └── Import functionality with success toast
    │   ├── Health Metrics Form (8 fields)
    │   └── RiskResult.js ✅ COMPLETE (Enhanced)
    │       ├── Overall Health Index (doughnut chart)
    │       ├── BMI Display with classification
    │       ├── Three Agent Cards (gradient backgrounds)
    │       │   ├── CardioAgent (pink gradient)
    │       │   ├── MetabolicAgent (blue gradient)
    │       │   └── NeuroAgent (purple gradient)
    │       ├── Radar Chart (all 3 agents simultaneously)
    │       ├── Risk Factor Breakdown (per-agent metrics)
    │       │   └── Color-coded progress bars
    │       ├── Agent Comparison (bar chart)
    │       └── Integrated Recommendations List
    │
    ├── HistoryList.js
    │   └── Assessment cards with timestamp, risk level
    │
    ├── StatisticsPanel.js
    │   ├── Metric cards (total, average risk, average BMI)
    │   ├── Risk distribution pie chart
    │   └── Risk level breakdown
    │
    └── AdminDashboard.js ✅ COMPLETE
        ├── System Status Card (health indicator)
        ├── Metrics Grid (4 cards)
        │   ├── Total Assessments
        │   ├── Average Risk Score
        │   ├── Average BMI
        │   └── Response Time
        ├── Risk Distribution Visualization
        │   └── Horizontal bars (Low/Moderate/High)
        └── Recent Activity (Audit Logs Table)
            └── Columns: Timestamp, Action, Resource, Status, User
```

#### Key Frontend Features

**Chart.js Integration**:
- Registered components: ArcElement, CategoryScale, LinearScale, BarElement, RadialLinearScale, PointElement, LineElement, Filler
- Doughnut charts for overall health index
- Radar charts for multi-agent comparison (max scale: 100, step: 20)
- Bar charts for agent comparison and risk factors
- Custom tooltips and responsive sizing

**Apple Watch Connection Flow**:
1. User clicks "Connect Apple Watch" button
2. Loading spinner during connection
3. Connection established → green status indicator appears
4. "View Data" button shows preview modal
5. "Import to Form" auto-populates all 8 form fields
6. Success toast notification (3s duration)
7. User can immediately calculate risk

**Enhanced Visualizations**:
- Agent-specific cards with hover effects (translateY -4px)
- Breakdown items with color-coded progress bars:
  - Red: >50% (high risk)
  - Orange: >30% (moderate risk)
  - Green: ≤30% (low risk)
- Responsive grid layouts (auto-fit minmax)
- Smooth animations (0.3s ease transitions)

**Admin Dashboard Features**:
- Real-time system health monitoring
- Risk distribution percentages
- Audit log filtering and pagination
- Refresh button to reload all data concurrently (Promise.all)
- Badge styling for action/status indicators
- Responsive design for various screen sizes

#### Styling Architecture

**CSS Organization**:
- Component-scoped CSS files
- Shared color palette (purple gradient theme)
- Responsive breakpoints for mobile/tablet/desktop
- Animation keyframes for smooth transitions
- Accessibility considerations (focus states, contrast)

**Design System**:
- Primary gradient: #667eea → #764ba2 (purple)
- Agent gradients: Pink (cardio), Blue (metabolic), Purple (neuro)
- Status colors: Green (healthy/low), Orange (moderate), Red (high)
- Typography: System fonts with fallbacks
- Spacing: 8px grid system

## Data Flow

### Standard Assessment Flow
```
User Input (Form)
    ↓
Frontend Validation
    ↓
POST /api/aggregate
    ↓
AggregatorAgent
    ├→ CardioAgent (35%) → Risk Score + Recommendations
    ├→ MetabolicAgent (35%) → Risk Score + BMI + Recommendations
    └→ NeuroAgent (30%) → Risk Score + Recommendations
        ↓
    Weighted Aggregation (sum of weighted scores)
        ↓
    Overall Health Index Calculation
        ↓
    Risk Level Classification (Low/Moderate/High)
        ↓
    Critical Areas Identification
        ↓
    Integrated Recommendations Generation
        ↓
    DatabaseManager.save_assessment()
        ↓
    AuditLogger.log() (optional)
        ↓
    JSON Response to Frontend
        ↓
    RiskResult Component Rendering
        ├→ Charts (doughnut, radar, bars)
        ├→ Agent Cards
        └→ Recommendations
```

### Apple Watch Integration Flow
```
Frontend: Click "Connect Apple Watch"
    ↓
POST /api/watch/connect
    ↓
AppleWatchMock.connect()
    ├→ Generate session_key
    ├→ Simulate device info
    └→ Return session data
        ↓
Frontend: Store session_key, show green status
        ↓
User: Click "View Data"
        ↓
GET /api/watch/sample-data?session_key=xxx
    ↓
AppleWatchMock.generate_sample_data()
    ├→ Age: 45-65 range
    ├→ Weight: 70-95 kg
    ├→ Height: 165-185 cm
    ├→ BP: 110-135/65-85 mmHg
    ├→ Cholesterol: 150-220 mg/dL
    ├→ Exercise: 2-5 days/week
    └→ Smoking: Random boolean
        ↓
Frontend: Display in preview modal
        ↓
User: Click "Import to Form"
        ↓
Auto-populate all 8 form fields
        ↓
Success toast notification
        ↓
User: Click "Calculate Risk"
        ↓
[Standard Assessment Flow continues...]
```

### Admin Dashboard Data Flow
```
Admin Tab Click
    ↓
AdminDashboard.useEffect()
    ↓
Promise.all([
    GET /api/admin/system/status,
    GET /api/admin/system/metrics,
    GET /api/admin/audit-logs
])
    ↓
Parallel Backend Calls
    ├→ DatabaseManager.get_assessment_stats()
    ├→ DatabaseManager.get_risk_distribution()
    └→ AuditLogger.get_logs()
        ↓
Data Aggregation
    ↓
Frontend State Update
    ↓
Component Rendering
    ├→ System Status (healthy/error)
    ├→ Metric Cards (4 cards)
    ├→ Risk Distribution Bars
    └→ Audit Logs Table
        ↓
User: Click "Refresh"
    ↓
[Repeat data fetch cycle]
```

## Performance Requirements & Achievements

### Target Metrics
- API response time: ≤3000ms ✅ **Achieved: <100ms average**
- Database query time: <50ms ✅ **Achieved: ~10-20ms**
- Agent processing time: <30ms per agent ✅ **Achieved: ~0.04ms**
- Overall assessment time: <100ms ✅ **Achieved: ~0.12ms**
- Frontend render time: <500ms ✅ **Achieved: ~200ms**

### Performance Monitoring
- Built into AggregatorAgent (assess_with_timing wrapper)
- Per-agent timing tracked
- Overall assessment timing logged
- Performance statistics endpoint available
- Frontend console logging for debugging

### Optimization Techniques
- Database indexing on frequently queried columns
- Concurrent agent execution (could parallelize further)
- Efficient JSON serialization
- Frontend component memoization
- Lazy loading for charts

## Security & Compliance

### Audit Logging
- **All user actions logged**: CREATE, READ, UPDATE, DELETE, EXPORT
- **Metadata captured**: IP address, user agent, timestamp
- **Indexed queries**: Fast retrieval by user_id, action, date range
- **Retention policy**: 90-day default (configurable)
- **Statistics tracking**: Action counts, status distribution, user activity
- **Manual cleanup**: Admin-triggered log cleanup API

### Data Privacy Considerations
- **Current**: Demo-level security (username-only login)
- **Production needs**:
  - User authentication (JWT tokens, OAuth 2.0)
  - Password hashing (bcrypt, scrypt)
  - Data encryption at rest (database encryption)
  - HTTPS/TLS for transport
  - HIPAA compliance (PHI handling)
  - GDPR compliance (right to erasure, data export)
  - Session management with expiration
  - Rate limiting and CSRF protection

### Access Control
- **Current**: Single-user demo mode
- **Planned**: Role-based access control (Admin, User, Guest)
- **Admin capabilities**:
  - View all users and assessments
  - Access audit logs
  - Configure system thresholds
  - Generate reports
  - Manage user accounts

## Testing Strategy

### Current Test Coverage
- **46 automated tests** - All passing ✅
- **Test categories**:
  - Agent assessment tests (risk calculation accuracy)
  - Performance requirement validation
  - Error handling and edge cases
  - Data validation tests
  - Integration tests (multi-agent coordination)
  - Database operation tests
  - API endpoint tests

### Test Framework
- **Backend**: Python unittest
- **Test execution**: `python -m pytest` or `python -m unittest discover`
- **Coverage tracking**: Available via pytest-cov
- **CI/CD ready**: Can integrate with GitHub Actions

### Testing Gaps (Future Work)
- [ ] End-to-end UI tests (Playwright, Cypress)
- [ ] Load testing (concurrent users, stress testing)
- [ ] Security penetration testing
- [ ] Accessibility testing (aXe, WAVE, WCAG 2.1 AA)
- [ ] Cross-browser compatibility
- [ ] Mobile responsiveness testing
- [ ] API contract testing

## Deployment Architecture

### Current Development Setup
```
Development Environment
├── Backend: Flask Dev Server (Port 5000)
│   ├── app.py (main application)
│   ├── SQLite database (medai.db)
│   └── Virtual environment (venv)
│
└── Frontend: React Dev Server (Port 3000)
    ├── Webpack dev server
    ├── Hot module replacement
    └── Proxy to backend (/api → localhost:5000)
```

### Recommended Production Architecture
```
Production Environment
├── Load Balancer (AWS ALB / Nginx)
│   ├── SSL/TLS termination
│   ├── Request routing
│   └── Health checks
│
├── Web Server (Nginx)
│   ├── Static file serving (React build)
│   ├── Reverse proxy to app servers
│   ├── Caching (static assets)
│   └── Compression (gzip/brotli)
│
├── Application Servers (Gunicorn, 4-8 workers)
│   ├── Flask application instances
│   ├── Process pooling
│   └── Graceful restarts
│
├── Database
│   ├── PostgreSQL (recommended for production)
│   ├── Connection pooling
│   ├── Automated backups
│   └── Read replicas (optional)
│
└── Caching Layer (Redis, optional)
    ├── Session storage
    ├── Frequently accessed data
    └── Rate limiting
```

### Container Deployment (Docker)
```dockerfile
# Example Dockerfile structure
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

### Cloud Deployment Options
1. **AWS EC2** - Full control, manual scaling
2. **AWS Elastic Beanstalk** - Managed platform
3. **Docker Container** - AWS ECS/EKS, Google Cloud Run
4. **Heroku** - Quick deployment, limited free tier
5. **Vercel/Netlify** - Frontend, serverless backend

### Environment Configuration
```bash
# Required environment variables
FLASK_ENV=production
SECRET_KEY=<random-secret-key>
DATABASE_URL=postgresql://user:pass@host:5432/medai
REDIS_URL=redis://host:6379/0
ALLOWED_ORIGINS=https://yourdomain.com
```

## Extensibility

### Adding New Assessment Agents

**Step 1: Create Agent Class**
```python
# backend/models/agents/respiratory_agent.py
from backend.models.agents.base_agent import BaseAgent

class RespiratoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RespiratoryAgent",
            weight=0.20  # Adjust weights accordingly
        )
    
    def assess_risk(self, data):
        # Implement respiratory risk logic
        # Consider: smoking history, lung function, etc.
        risk_score = self._calculate_respiratory_risk(data)
        return risk_score
    
    def get_recommendations(self, risk_score):
        # Return respiratory-specific recommendations
        recommendations = []
        if risk_score > 50:
            recommendations.append("Consider pulmonary function testing")
        return recommendations
```

**Step 2: Register in AggregatorAgent**
```python
# backend/models/agents/aggregator_agent.py
from backend.models.agents.respiratory_agent import RespiratoryAgent

class AggregatorAgent:
    def __init__(self):
        self.agents = {
            'cardio': CardioAgent(),
            'metabolic': MetabolicAgent(),
            'neuro': NeuroAgent(),
            'respiratory': RespiratoryAgent()  # Add new agent
        }
```

**Step 3: Add Tests**
```python
# backend/tests/test_agents.py
def test_respiratory_agent():
    agent = RespiratoryAgent()
    test_data = {...}
    result = agent.assess_risk(test_data)
    assert result['risk_score'] >= 0
    assert result['risk_score'] <= 100
```

**Step 4: Update Frontend**
- Add respiratory agent card to RiskResult.js
- Update radar chart to include 4th dimension
- Add respiratory-specific visualizations

### Adding New Data Sources

**Pattern to follow** (based on AppleWatchMock):

1. **Create integration class** (e.g., `FitbitIntegration`)
2. **Implement data retrieval methods**
3. **Create API routes blueprint**
4. **Register blueprint in app.py**
5. **Add frontend component**
6. **Document in ARCHITECTURE.md**

**Example: Fitbit Integration**
```python
# backend/models/integrations/fitbit_integration.py
class FitbitIntegration:
    def __init__(self):
        self.api_base = "https://api.fitbit.com/1"
    
    def connect(self, user_id, oauth_token):
        # Implement OAuth connection
        pass
    
    def get_heart_rate(self, user_id):
        # Fetch from Fitbit API
        pass
```

### Adding New Visualizations

**Chart.js Pattern**:
```javascript
// Register required components
import {
    Chart as ChartJS,
    NewChartType,  // e.g., ScatterController
    // ... other components
} from 'chart.js';

ChartJS.register(NewChartType, ...);

// Create chart component
const NewChart = ({ data }) => {
    const chartData = {
        datasets: [...]
    };
    
    return <Scatter data={chartData} options={options} />;
};
```

## Future Enhancements

### High Priority (Next Sprint)
- [ ] PDF report generation (reportlab/weasyprint)
- [ ] User authentication system (JWT tokens)
- [ ] Email notifications for high-risk assessments
- [ ] Data export (CSV, JSON)
- [ ] Multi-language support (i18n)

### Medium Priority
- [ ] Real HealthKit API integration (iOS)
- [ ] Progressive Web App (PWA) support
- [ ] Mobile-responsive optimizations
- [ ] Dark mode theme
- [ ] Historical trend analysis
- [ ] Goal setting and tracking

### Long Term
- [ ] Machine learning risk prediction models
- [ ] Microservices architecture (agent services)
- [ ] Real-time WebSocket notifications
- [ ] Telemedicine integration
- [ ] Wearable device ecosystem (Fitbit, Garmin, etc.)
- [ ] Social features (share progress, challenges)
- [ ] Gamification (achievements, streaks)

### Research & Innovation
- [ ] AI-powered personalized recommendations (GPT integration)
- [ ] Predictive analytics (future risk forecasting)
- [ ] Natural language query interface
- [ ] Voice-activated assessment
- [ ] AR/VR health visualization

## Known Issues & Limitations

### Current Limitations
1. **Authentication**: Username-only, no password protection
2. **Apple Watch**: Mock data only, not real device integration
3. **Database**: SQLite not suitable for high concurrency
4. **Scalability**: Single-server architecture
5. **Security**: HTTPS/TLS not enforced in development
6. **Testing**: No E2E or load testing yet
7. **Documentation**: API documentation not in Swagger/OpenAPI format

### Technical Debt
- Refactor RiskCalculator.js (too large, split into smaller components)
- Add Redux/Context for global state management
- Implement proper error boundaries in React
- Add database migration system
- Improve CSS architecture (consider CSS-in-JS or Tailwind)
- Add comprehensive logging (Winston, Loggly)

## Maintenance & Operations

### Monitoring Checklist
- [ ] Application logs (Flask logging)
- [ ] Audit logs (user actions)
- [ ] Performance metrics (response times)
- [ ] Error tracking (Sentry, Rollbar)
- [ ] Uptime monitoring (Pingdom, UptimeRobot)
- [ ] Database health (query times, connection pool)
- [ ] User analytics (Google Analytics, Mixpanel)

### Backup Strategy
- **SQLite database**: Daily automated backups to S3/Google Cloud Storage
- **Audit logs**: Monthly archives with 7-year retention
- **Configuration files**: Version controlled in Git
- **User uploads**: Separate backup schedule if applicable

### Update Procedures
1. **Database migrations**: Use Alembic or Flask-Migrate
2. **API versioning**: /api/v1/, /api/v2/ for breaking changes
3. **Backward compatibility**: Maintain old endpoints for 6 months
4. **Gradual rollout**: Canary deployment, A/B testing
5. **Rollback procedures**: Keep 3 previous versions deployable

### Support & Documentation
- **User Guide**: USER_GUIDE.md with screenshots
- **API Documentation**: Generate from code (Swagger UI)
- **Developer Docs**: This ARCHITECTURE.md file
- **Troubleshooting**: Common issues and solutions
- **FAQ**: Frequently asked questions

## Contact & Resources

### Project Documentation
- **README.md** - Quick start guide
- **ARCHITECTURE.md** - This file (system design)
- **IMPLEMENTATION_STATUS.md** - Current progress tracking
- **USER_GUIDE.md** - End-user instructions

### External Resources
- **UML Diagrams** - Design documents (PDF)
- **Figma Design** - UI mockups
- **Course Materials** - Software Engineering requirements

### Getting Help
1. Check documentation files
2. Review inline code comments
3. Consult UML diagrams for design intent
4. Check test files for usage examples

---

**Document Version**: 3.0.0  
**Last Updated**: 2025-11-30  
**Current Phase**: Core Features Complete  
**Status**: Production-Ready for Course Demo  
**Estimated Completion**: 93%