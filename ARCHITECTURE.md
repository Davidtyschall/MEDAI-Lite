# MEDAI-Lite Architecture Documentation

## System Overview

MEDAI-Lite is a modular, AI-assisted health risk assessment and visualization platform designed for Software Engineering principles demonstration.

## Design Philosophy

### Core Principles
1. **Modularity**: Disease-specific agents for extensibility
2. **Separation of Concerns**: Clear boundaries between layers
3. **Performance**: ≤3s response time requirement
4. **Testability**: Comprehensive unit and integration tests
5. **Maintainability**: Clean code, documentation, UML compliance

## Architecture Layers

### 1. Agent Layer (AI Assessment)

#### Base Agent Pattern
```python
BaseAgent (ABC)
├── assess_risk() - Abstract method
├── get_recommendations() - Abstract method
├── assess_with_timing() - Performance monitoring
└── validate_data() - Input validation
```

#### Specialized Agents
1. **CardioAgent** (weight: 0.35)
   - Cardiovascular risk assessment
   - Blood pressure classification
   - Cholesterol analysis
   - Smoking impact
   - Exercise cardio benefits

2. **MetabolicAgent** (weight: 0.35)
   - BMI calculation & classification
   - Metabolic syndrome detection
   - Lipid profile analysis
   - Exercise metabolic impact

3. **NeuroAgent** (weight: 0.30)
   - Stroke risk assessment
   - Cognitive aging evaluation
   - Vascular brain health
   - Neuroprotective factors

#### Aggregator Agent
- Orchestrates all specialized agents
- Computes weighted overall health index
- Identifies critical areas
- Generates integrated recommendations
- Performance monitoring (≤3s requirement)

### 2. Data Layer

#### DatabaseManager
- User CRUD operations
- Assessment history storage
- Statistics aggregation
- Query optimization with indexes

#### AuditLogger
- Security event tracking
- Compliance logging
- User action auditing
- Log analytics and statistics
- Automatic log rotation

### 3. Integration Layer

#### AppleWatchMock
- HealthKit data simulation
- Heart rate monitoring
- Activity tracking
- Sleep analysis
- Workout history
- Real-time vitals

**Production Notes**: Replace with actual HealthKit API integration using proper OAuth and data privacy compliance.

### 4. API Layer

#### REST Endpoints

**Core APIs** (`/api/*`)
- `GET /api/health` - Health check
- `POST /api/risk` - Simple risk calculation (legacy)
- `GET /api/history` - Assessment history
- `GET /api/statistics` - Aggregated statistics

**Aggregate APIs** (`/api/aggregate/*`)
- `POST /api/aggregate` - Multi-agent comprehensive assessment
- `GET /api/aggregate/performance` - Performance metrics
- `GET /api/aggregate/agents` - Available agents info

**Watch APIs** (`/api/watch/*`)
- `POST /api/watch/connect` - Connect Apple Watch
- `GET /api/watch/vitals` - Current vital signs
- `GET /api/watch/heart-rate` - Heart rate history
- `GET /api/watch/activity` - Activity summaries
- `GET /api/watch/sleep` - Sleep tracking
- `GET /api/watch/workouts` - Workout history
- `GET /api/watch/export` - Full data export
- `GET /api/watch/sample-data` - Sample data generation

**Admin APIs** (To be implemented)
- User management
- Threshold configuration
- Audit log access
- System monitoring

### 5. Frontend Layer

#### Planned React Components

```
App
├── LoginPage
├── Dashboard
│   ├── NavigationTabs
│   ├── RiskCalculator
│   │   ├── AppleWatchConnect (NEW)
│   │   ├── MetricsForm
│   │   └── ResultsDisplay (Chart.js)
│   ├── History
│   │   └── AssessmentCards
│   ├── Statistics
│   │   ├── MetricCards
│   │   ├── PieChart (risk distribution)
│   │   └── LineChart (trends)
│   └── Chatbot (NEW - guided assessment)
└── AdminDashboard (NEW)
    ├── UserManagement
    ├── AuditLogs
    └── ThresholdConfig
```

## Data Flow

### Standard Assessment Flow
```
User Input → RiskCalculator → DatabaseManager → Response
```

### Enhanced Multi-Agent Flow
```
User/Watch Data → AggregatorAgent
                      ├→ CardioAgent → Risk Score
                      ├→ MetabolicAgent → Risk Score
                      └→ NeuroAgent → Risk Score
                            ↓
                   Weighted Aggregation
                            ↓
                   Overall Health Index
                            ↓
                   DatabaseManager + AuditLogger
                            ↓
                   Comprehensive Response
```

### Apple Watch Integration Flow
```
Frontend → POST /api/watch/connect
              ↓
       AppleWatchMock.connect()
              ↓
       Session Created
              ↓
       GET /api/watch/export
              ↓
       Health Data Retrieved
              ↓
       Auto-populate Assessment Form
              ↓
       POST /api/aggregate
              ↓
       Multi-Agent Assessment
```

## Performance Requirements

### Target Metrics
- API response time: ≤3000ms (currently ~100ms)
- Database query time: <50ms
- Agent processing time: <30ms per agent
- Overall assessment time: <100ms

### Performance Monitoring
- Built into AggregatorAgent
- Per-agent timing
- Overall assessment timing
- Performance statistics tracking

## Security & Compliance

### Audit Logging
- All user actions logged
- IP address tracking
- User agent recording
- Timestamp indexing
- Configurable retention (default: 90 days)

### Data Privacy
- User data encryption (to be implemented)
- HIPAA compliance considerations
- Data anonymization options
- Export/delete user data (GDPR)

## Testing Strategy

### Current Coverage
- **46 automated tests** passing
- Unit tests for all agents
- Integration tests for aggregator
- API endpoint tests
- Database operation tests

### Test Categories
1. Agent Assessment Tests
2. Performance Requirement Tests
3. Error Handling Tests
4. Data Validation Tests
5. Integration Tests

### Future Testing
- End-to-end UI tests
- Load testing (concurrent users)
- Security penetration testing
- Accessibility testing (WCAG 2.1 AA)

## Deployment Architecture

### Development
```
Flask Dev Server (5000)
├── Backend APIs
└── React Dev Server (3000) - proxied
```

### Production (Recommended)
```
Load Balancer
├── Nginx (reverse proxy)
│   ├── Static Files (React build)
│   └── API Proxy → Gunicorn
│       └── Flask App (workers: 4-8)
│           ├── SQLite (or PostgreSQL)
│           └── Redis (session cache)
```

### Cloud Deployment Options
1. **AWS EC2** - Direct deployment
2. **Docker Container** - Containerized app
3. **AWS Lambda** - Serverless functions
4. **Heroku** - PaaS deployment

## Extensibility

### Adding New Agents

1. Create new agent class inheriting from `BaseAgent`:
```python
from backend.models.agents.base_agent import BaseAgent

class RespiratoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RespiratoryAgent", weight=0.20)
    
    def assess_risk(self, data):
        # Implementation
        pass
    
    def get_recommendations(self, risk_score):
        # Implementation
        pass
```

2. Register in `AggregatorAgent`:
```python
self.agents['respiratory'] = RespiratoryAgent()
```

3. Add tests in `test_agents.py`

### Adding New Data Sources

Follow the pattern in `AppleWatchMock`:
1. Create integration class
2. Implement data retrieval methods
3. Create API routes
4. Add to Flask app blueprints
5. Document in ARCHITECTURE.md

## Future Enhancements

### Short Term
- [ ] Admin dashboard implementation
- [ ] PDF report generation
- [ ] Chatbot UI component
- [ ] Enhanced visualizations (Recharts)
- [ ] Accessibility improvements

### Medium Term
- [ ] Real HealthKit API integration
- [ ] User authentication system
- [ ] Multi-language support
- [ ] Mobile-responsive optimizations
- [ ] Progressive Web App (PWA)

### Long Term
- [ ] Machine learning risk prediction
- [ ] Microservices architecture
- [ ] Real-time notifications
- [ ] Telemedicine integration
- [ ] Wearable device ecosystem

## UML Compliance

The implementation follows the UML diagrams provided in the design documents:

- **Class Diagrams**: Agent hierarchy, inheritance patterns
- **Sequence Diagrams**: API call flows, data processing
- **Component Diagrams**: System architecture, module boundaries

## Maintenance & Operations

### Monitoring
- Application logs
- Audit logs
- Performance metrics
- Error tracking
- User analytics

### Backup Strategy
- SQLite database backups (daily)
- Audit log archives (monthly)
- Configuration backups
- Code repository (Git)

### Update Procedures
1. Database migrations
2. API versioning
3. Backward compatibility
4. Gradual rollout
5. Rollback procedures

## Contact & Support

For questions about the architecture:
- Review design documents (PDFs)
- Check UML diagrams
- Consult this ARCHITECTURE.md
- Review inline code documentation

---

**Last Updated**: Phase 2 Complete  
**Version**: 2.0.0  
**Status**: Active Development
