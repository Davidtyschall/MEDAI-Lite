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

## API Endpoints

### Health Check
```bash
GET /api/health

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

GET /api/history?limit=10&user_id=1

GET /api/history/{assessment_id}

DELETE /api/history/{assessment_id}

pip install -r requirements.txt

python -m backend.app

cd frotnend 

npm install

npm start



