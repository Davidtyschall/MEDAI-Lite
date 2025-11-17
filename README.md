<<<<<<< HEAD
# Health Risk Assessment Application

This application allows users to calculate and track personal health risk assessments based on various clinical and lifestyle factors. It provides interactive charts, historical results, and statistical summaries.

---

## Usage

1. **Login**  
   Enter any username on the login page (demo mode)

2. **Risk Calculator**  
   - Complete the health information form
   - Click **"Calculate Risk"** to generate your risk score
   - View detailed results and data visualizations

3. **History**  
   Review previous assessments and remove outdated entries

4. **Statistics**  
   View personalized statistical insights over time

---

## Health Risk Factors

The system evaluates the following health risk components:

- **Age** — Risk increases with age
- **BMI** — Calculated using height and weight
- **Blood Pressure** — Systolic & diastolic measurements
- **Cholesterol** — Total cholesterol level
- **Smoking** — Current smoking status
- **Exercise** — Frequency of physical activity

---

## Risk Levels

| Risk Category | Score Range | Meaning |
|---------------|-------------|---------|
| **Low Risk** | 0–24 | Healthy parameters |
| **Moderate Risk** | 25–49 | Some factors may require attention |
| **High Risk** | 50+ | Multiple concerning health indicators |

---

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build

### Commands

python -m backend.app

GET /api/statistics?user_id=1

python -m pytest backend/tests/

python -m unittest backend/tests/test_risk_calculator.py

cd frontend
npm test

git checkout -b feature-name

git commit -am "Add feature"

git push origin feature-name
=======
# MEDAI-Lite

Health Risk Assessment & Visualization Platform (Flask + React + SQLite)

## Overview

MEDAI-Lite is a full-stack web application for calculating and visualizing health risk assessments. It provides an intuitive interface for users to input health parameters and receive comprehensive risk scores with beautiful data visualizations.

## Features

- **Risk Calculator**: Calculate health risk scores based on multiple health parameters
- **Interactive Dashboard**: User-friendly interface with real-time data visualization
- **Assessment History**: Track and review past health assessments
- **Statistics Panel**: View trends and insights with Chart.js visualizations
- **RESTful API**: Well-documented backend API for programmatic access
- **Responsive Design**: Mobile-friendly interface that works on all devices

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database for data persistence
- **Flask-CORS**: Enable cross-origin requests
- **Python Classes**: 
  - `RiskCalculator`: Calculates health risk scores
  - `DatabaseManager`: Manages database operations

### Frontend
- **React**: Modern UI library
- **React Router**: Client-side routing
- **Chart.js**: Data visualization library
- **Axios**: HTTP client for API calls

## Project Structure

```
MEDAI-Lite/
├── backend/
│   ├── models/
│   │   ├── risk_calculator.py      # Health risk calculation logic
│   │   └── database_manager.py     # Database operations
│   ├── routes/
│   │   └── api_routes.py           # REST API endpoints
│   ├── tests/
│   │   ├── test_risk_calculator.py
│   │   ├── test_database_manager.py
│   │   └── test_api_routes.py
│   └── app.py                      # Flask application entry point
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── RiskCalculator.js   # Risk calculation form
│   │   │   ├── RiskResult.js       # Results with charts
│   │   │   ├── HistoryList.js      # Assessment history
│   │   │   └── StatisticsPanel.js  # Statistics dashboard
│   │   ├── pages/
│   │   │   ├── Login.js            # Login page
│   │   │   └── Dashboard.js        # Main dashboard
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.js                  # Main application
│   │   └── index.js                # React entry point
│   └── package.json
├── requirements.txt                 # Python dependencies
└── README.md

```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Davidtyschall/MEDAI-Lite.git
cd MEDAI-Lite
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask backend:
```bash
python -m backend.app
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000`
>>>>>>> copilot-scaffold

## API Endpoints

### Health Check
<<<<<<< HEAD
```bash
GET /api/health

=======
```
GET /api/health
```
Check API status

### Calculate Risk
```
>>>>>>> copilot-scaffold
POST /api/risk
Content-Type: application/json

{
  "age": 30,
  "weight_kg": 70,
  "height_cm": 175,
  "systolic": 120,
  "diastolic": 80,
  "cholesterol": 190,
  "is_smoker": false,
  "exercise_days": 3
}
<<<<<<< HEAD

GET /api/history?limit=10&user_id=1

GET /api/history/{assessment_id}

DELETE /api/history/{assessment_id}

pip install -r requirements.txt

python -m backend.app

cd frotnend 

npm install

npm start



=======
```

### Get Assessment History
```
GET /api/history?limit=10&user_id=1
```

### Get Specific Assessment
```
GET /api/history/{assessment_id}
```

### Delete Assessment
```
DELETE /api/history/{assessment_id}
```

### Get Statistics
```
GET /api/statistics?user_id=1
```

## Testing

### Backend Tests

Run all backend tests:
```bash
python -m pytest backend/tests/
```

Run specific test file:
```bash
python -m unittest backend/tests/test_risk_calculator.py
```

### Frontend Tests

Run frontend tests:
```bash
cd frontend
npm test
```

## Usage

1. **Login**: Enter any username on the login page (demo mode)
2. **Risk Calculator**: 
   - Fill in your health information
   - Click "Calculate Risk" to see your assessment
   - View detailed breakdown with charts
3. **History**: Review past assessments and delete old records
4. **Statistics**: View overall trends and insights

## Health Risk Factors

The application evaluates the following risk factors:

- **Age**: Risk increases with age
- **BMI**: Calculated from height and weight
- **Blood Pressure**: Systolic and diastolic readings
- **Cholesterol**: Total cholesterol levels
- **Smoking**: Current smoking status
- **Exercise**: Physical activity frequency

## Risk Levels

- **Low Risk** (0-24): Healthy parameters
- **Moderate Risk** (25-49): Some areas need attention
- **High Risk** (50+): Multiple risk factors present

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

The built files will be in `frontend/build/` and Flask will serve them automatically.

### Run Production Server
```bash
python -m backend.app
```

For production, consider using:
- **Gunicorn** for Flask
- **Nginx** as reverse proxy
- **AWS EC2** or similar for hosting

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

See LICENSE file for details.

## Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ using Flask and React
>>>>>>> copilot-scaffold
