# MEDAI-Lite User Guide

**Version**: 1.0  
**Last Updated**: November 30, 2025
**For**: MEDAI-Lite Health Risk Assessment Platform

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Login](#login)
4. [Risk Calculator](#risk-calculator)
5. [Apple Watch Integration](#apple-watch-integration)
6. [Understanding Your Results](#understanding-your-results)
7. [Assessment History](#assessment-history)
8. [Statistics Dashboard](#statistics-dashboard)
9. [Admin Dashboard](#admin-dashboard)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#frequently-asked-questions)

---

## Introduction

### What is MEDAI-Lite?

MEDAI-Lite is a comprehensive health risk assessment platform that uses a multi-agent artificial intelligence system to evaluate your health across three key domains:

- **🫀 Cardiovascular Health** (35% weight) - Blood pressure, cholesterol, smoking impact
- **⚖️ Metabolic Health** (35% weight) - BMI, metabolic syndrome, weight management
- **🧠 Neurological Health** (30% weight) - Stroke risk, cognitive aging, brain health

### Key Features

✅ **Multi-Agent Assessment** - Three specialized AI agents working together  
✅ **Apple Watch Integration** - Import health data directly from your device  
✅ **Visual Analytics** - Radar charts, agent cards, risk breakdowns  
✅ **Historical Tracking** - View past assessments and trends  
✅ **Admin Monitoring** - System health and audit log access  
✅ **Fast & Accurate** - <100ms response time with comprehensive analysis

### Who Should Use This?

- Individuals wanting to understand their health risks
- Healthcare professionals for preliminary screening
- Researchers studying health risk patterns
- Students learning about health informatics
- Anyone interested in preventive health care

**⚠️ Important Disclaimer**: MEDAI-Lite is an educational demonstration tool. Always consult qualified healthcare professionals for medical advice. This tool does not replace professional medical assessment.

---

## Getting Started

### System Requirements

**Browser Requirements**:
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- JavaScript enabled
- Minimum screen resolution: 1024x768 (responsive down to 768px)

**Network Requirements**:
- Internet connection for backend API access
- Recommended: 5 Mbps or faster

### Accessing the Application

1. Open your web browser
2. Navigate to: `http://localhost:3000` (development) or your deployed URL
3. You'll see the MEDAI-Lite login screen

---

## Login

### Simple Authentication

MEDAI-Lite uses a simplified authentication system for demonstration purposes.

**Step-by-Step**:

1. **Enter a Username**
   - Type any username in the "Username" field
   - Examples: "john_doe", "test_user", "demo"
   - Username is used to track your assessment history

2. **Click "Continue as Guest"**
   - No password required
   - Creates a session for tracking assessments
   - Username stored in browser local storage

3. **You're In!**
   - Redirected to the main Dashboard
   - Your username appears in the top-right corner
   - Green "API Connected" indicator confirms backend connection

**Screenshot Guide**: *[Login screen with username field and "Continue as Guest" button highlighted]*

### Session Management

- **Session Duration**: Remains active until you click "Logout"
- **Multiple Tabs**: Username persists across browser tabs
- **Logout**: Click "Logout" button in top-right to clear session
- **Re-login**: Use same username to access your assessment history

---

## Risk Calculator

### Overview

The Risk Calculator is the heart of MEDAI-Lite. It collects your health information and provides a comprehensive risk assessment using three specialized AI agents.

### Navigation

From the Dashboard, click the **📊 Risk Calculator** tab (active by default).

### Manual Data Entry

**Required Information** (8 fields):

1. **Age (years)** - Your current age (1-150 range)
2. **Weight (kg)** - Your weight in kilograms
3. **Height (cm)** - Your height in centimeters
4. **Systolic BP (mmHg)** - Top blood pressure number (50-250 range)
5. **Diastolic BP (mmHg)** - Bottom blood pressure number (30-150 range)
6. **Total Cholesterol (mg/dL)** - Cholesterol level (100-400 range)
7. **Exercise Days/Week** - How many days per week you exercise (0-7 dropdown)
8. **I am a smoker** - Checkbox (check if you currently smoke)

**Step-by-Step Entry**:

1. Click into the "Age (years)" field
2. Type your age (e.g., "45")
3. Press Tab or click to move to next field
4. Continue entering all required information
5. For "Exercise Days/Week", click the dropdown and select
6. Check "I am a smoker" box if applicable

**Input Validation**:
- Red border appears if value is out of range
- Form cannot be submitted until all fields are valid
- Helpful hints show valid ranges

**Screenshot Guide**: *[Empty risk calculator form with all 8 fields visible]*

### Submitting Assessment

1. **Review Your Data** - Double-check all entered values
2. **Click "Calculate Risk"** - Large purple button at bottom
3. **Loading State** - Button shows "Calculating..." with spinner
4. **Results Appear** - Scroll down to see comprehensive results (typical: <1 second)

---

## Apple Watch Integration

### Overview

Quickly populate the risk calculator form with health data from your Apple Watch (simulated in this demo version).

**Screenshot Guide**: *[Connect Apple Watch button highlighted above the form]*

### Connecting Your Watch

**Step 1: Initiate Connection**
1. Look for the purple "📱 Connect Apple Watch" button
2. Button appears above the form when no results are displayed
3. Click the button to start connection

**Step 2: Connection Process**
- Loading spinner appears on button
- Button text changes to "Connecting..."
- Typical connection time: 1-2 seconds

**Step 3: Connection Established**
- Green status indicator appears: "✓ Connected: Apple Watch Series 9"
- Button changes to "🔌 Disconnect Watch"
- New button appears: "View Data"

**Screenshot Guide**: *[Connected state showing green status indicator and View Data button]*

### Viewing Watch Data

1. **Click "View Data"** button
2. **Preview Modal Opens** showing all health metrics:
   - Age and physical stats (weight, height)
   - Vital signs (blood pressure, heart rate)
   - Activity metrics (exercise frequency)
   - Health status (smoking)
3. **Review the Data** - Ensure it looks reasonable

**Screenshot Guide**: *[Data preview modal with sample health metrics in grid layout]*

### Importing to Form

1. **In the preview modal**, click **"Import to Form"** button
2. **Modal Closes** automatically
3. **Green Success Toast** appears top-right: "✓ Apple Watch data imported successfully!"
4. **All Form Fields Populated** - Check that all 8 fields now have values
5. **Ready to Calculate** - Click "Calculate Risk" to proceed

**Data Imported**:
- Age: 45-65 range (moderate risk demonstration)
- Weight: 70-95 kg
- Height: 165-185 cm
- Blood Pressure: 110-135/65-85 mmHg
- Cholesterol: 150-220 mg/dL
- Exercise: 2-5 days per week
- Smoking: Random (varies per connection)

**Screenshot Guide**: *[Form with all fields populated from Apple Watch data]*

### Disconnecting Watch

1. Click **"🔌 Disconnect Watch"** button
2. Status indicator disappears
3. Button returns to "📱 Connect Apple Watch"
4. Form data remains (not cleared)
5. Can reconnect anytime for new data

---

## Understanding Your Results

### Overview

After clicking "Calculate Risk", you'll see a comprehensive multi-panel results display with visualizations and recommendations.

**Screenshot Guide**: *[Full results page showing all sections]*

### Overall Health Index

**Location**: Top of results, large doughnut chart

**What It Shows**:
- Your overall health score (0-100 scale)
- Color-coded risk level:
  - 🟢 **Green (0-30)**: Low Risk - Healthy status
  - 🟠 **Orange (30-60)**: Moderate Risk - Needs attention
  - 🔴 **Red (60-100)**: High Risk - Urgent concerns

**How It's Calculated**:
- Weighted average of three agent scores
- CardioAgent: 35% weight
- MetabolicAgent: 35% weight
- NeuroAgent: 30% weight

**Example**: 
- CardioAgent score: 15.5
- MetabolicAgent score: 14.5  
- NeuroAgent score: 13.5
- Overall: (15.5×0.35 + 14.5×0.35 + 13.5×0.30) = 14.55
- Risk Level: "Low"

**Screenshot Guide**: *[Doughnut chart with score 14.55 and "Low Risk" label]*

### BMI Display

**Location**: Next to overall health index

**What It Shows**:
- Your Body Mass Index calculated from height/weight
- BMI classification:
  - Underweight (BMI < 18.5)
  - Normal (18.5-24.9)
  - Overweight (25-29.9)
  - Obese Class I (30-34.9)
  - Obese Class II (35-39.9)
  - Obese Class III (≥40)

**Screenshot Guide**: *[BMI value 22.86 with "Normal" classification]*

### Agent Assessment Cards

**Location**: Three cards below overall index (side by side)

#### 🫀 Cardiovascular Agent (Pink Gradient)

**What It Analyzes**:
- Blood pressure classification
- Cholesterol levels
- Smoking impact on heart health
- Age-related cardiovascular risks
- Exercise cardio benefits

**Risk Score**: 0-100 (lower is better)

**Risk Factors Breakdown**:
- Age factor (0-100%)
- Blood pressure factor (0-100%)
- Cholesterol factor (0-100%)
- Smoking factor (0-100%)
- Exercise benefit (-40% max reduction)

**Color Coding**:
- 🟢 Green bar: ≤30% (low risk)
- 🟠 Orange bar: 31-50% (moderate)
- 🔴 Red bar: >50% (high risk)

**Recommendations Example**:
- "Your blood pressure is optimal. Keep up the good work!"
- "Your cholesterol level is desirable (163 mg/dL). Maintain healthy diet."
- "Non-smoker status significantly reduces cardiovascular disease risk"

**Screenshot Guide**: *[CardioAgent card with pink gradient, score 15.5, and risk factor bars]*

#### ⚖️ Metabolic Agent (Blue Gradient)

**What It Analyzes**:
- BMI calculation and classification
- Metabolic syndrome indicators
- Weight management status
- Lipid profile evaluation
- Exercise metabolic benefits

**Risk Score**: 0-100 (lower is better)

**Risk Factors Breakdown**:
- Age factor (0-100%)
- BMI factor (0-100%)
- Cholesterol factor (0-100%)
- Exercise benefit (-30% max reduction)

**BMI Thresholds**:
- <18.5: Underweight (moderate risk)
- 18.5-24.9: Normal (low risk)
- 25-29.9: Overweight (moderate risk)
- 30+: Obese (high risk, scaled by class)

**Recommendations Example**:
- "Your BMI of 22.86 is in the normal range (18.5-24.9)"
- "Maintain current weight through balanced diet and regular exercise"
- "Continue exercising 3 days/week for metabolic health"

**Screenshot Guide**: *[MetabolicAgent card with blue gradient, score 14.5, BMI 22.86]*

#### 🧠 Neurological Agent (Purple Gradient)

**What It Analyzes**:
- Stroke risk assessment
- Cognitive aging factors
- Vascular brain health
- Blood pressure impact on brain
- Neuroprotective lifestyle factors

**Risk Score**: 0-100 (lower is better)

**Risk Factors Breakdown**:
- Age factor (0-100%)
- Blood pressure factor (0-100%)
- Cholesterol factor (0-100%)
- Exercise benefit (-25% max reduction)

**Key Considerations**:
- Optimal BP (<120/80) is best for brain health
- Age is primary non-modifiable risk factor
- Exercise provides significant neuroprotection
- Cholesterol management supports vascular brain health

**Recommendations Example**:
- "Your blood pressure is optimal for brain health"
- "Age-related cognitive decline risk is minimal at your age"
- "Continue regular exercise for neuroprotection"

**Screenshot Guide**: *[NeuroAgent card with purple gradient, score 13.5]*

### Radar Chart (Multi-Agent Comparison)

**Location**: Large chart below agent cards

**What It Shows**:
- All three agent scores on same chart
- Visual comparison of health domains
- 0-100 scale with 20-point increments
- Colored lines for each agent

**How to Read**:
- **Larger area** = Higher risk scores (worse health)
- **Smaller area** = Lower risk scores (better health)
- **Balanced shape** = Similar risk across domains
- **Lopsided shape** = One domain significantly worse

**Example Interpretation**:
- All three scores between 10-20: Excellent overall health
- CardioAgent at 60, others at 20: Focus on heart health
- NeuroAgent at 80, others at 30: Prioritize brain health interventions

**Screenshot Guide**: *[Radar chart with three colored areas representing agent scores]*

### Agent Comparison Bar Chart

**Location**: Below radar chart

**What It Shows**:
- Side-by-side bar comparison of agent scores
- Horizontal bars, color-coded by agent
- Numerical score displayed on each bar

**Screenshot Guide**: *[Horizontal bar chart showing CardioAgent: 15.5, MetabolicAgent: 14.5, NeuroAgent: 13.5]*

### Integrated Recommendations

**Location**: Bottom section of results

**What It Shows**:
- Combined recommendations from all three agents
- Prioritized action items
- Lifestyle modifications
- Areas to monitor

**Categories**:
1. **Immediate Actions** (if any high-risk factors)
2. **Lifestyle Modifications** (diet, exercise, stress)
3. **Monitoring** (what to track over time)
4. **Positive Reinforcement** (what you're doing well)

**Example Recommendations**:
- "Continue maintaining healthy blood pressure through current lifestyle"
- "Your exercise routine (3 days/week) provides significant protective benefits"
- "Consider increasing exercise to 4-5 days/week for optimal benefits"
- "Non-smoker status is excellent - continue avoiding tobacco"
- "Monitor blood pressure annually as you age"

**Screenshot Guide**: *[Recommendations list with bullet points and icons]*

### Viewing Another Assessment

**Option 1: Reset Form**
1. Scroll to bottom of results
2. Click **"Calculate Another Risk"** button
3. Form clears and returns to top

**Option 2: Modify Current Data**
1. Scroll up to form (above results)
2. Change any field values
3. Click **"Calculate Risk"** again
4. New results replace old results

---

## Assessment History

### Overview

View all your past risk assessments in one place, organized chronologically.

### Accessing History

1. From Dashboard, click **📋 History** tab
2. Page loads with your assessment history
3. Most recent assessments appear first

**Screenshot Guide**: *[History tab showing list of past assessments]*

### Understanding History Cards

Each assessment displays:

**Card Layout**:
```
┌─────────────────────────────────────┐
│ 📅 November 30, 2025 at 10:45 PM   │
│                                     │
│ Overall Risk: 14.55                 │
│ Risk Level: Low                     │
│ BMI: 22.86 (Normal)                 │
│                                     │
│ Agent Scores:                       │
│ • Cardiovascular: 15.5              │
│ • Metabolic: 14.5                   │
│ • Neurological: 13.5                │
│                                     │
│ [View Details] [Delete]             │
└─────────────────────────────────────┘
```

**Color Coding**:
- 🟢 Green border: Low risk assessments
- 🟠 Orange border: Moderate risk
- 🔴 Red border: High risk

**Screenshot Guide**: *[Sample assessment card with all information visible]*

### Viewing Assessment Details

1. Click **"View Details"** on any card
2. Full assessment results appear (same as after calculation)
3. Shows all visualizations and recommendations
4. Click **"Back to History"** to return

### Deleting Assessments

1. Click **"Delete"** button on any card
2. Confirmation dialog appears: "Are you sure?"
3. Click **"Yes, Delete"** to confirm
4. Assessment removed from history (permanent)

**⚠️ Warning**: Deletion is permanent and cannot be undone.

### Empty History

If you haven't completed any assessments:
- Message appears: "No assessment history found"
- Instructions: "Complete a risk assessment to see your history here"
- Click **"📊 Risk Calculator"** tab to get started

**Screenshot Guide**: *[Empty history state with helpful message]*

---

## Statistics Dashboard

### Overview

Aggregate statistics and visualizations across all your assessments.

### Accessing Statistics

1. From Dashboard, click **📈 Statistics** tab
2. Statistics load automatically
3. Updates in real-time as you complete assessments

**Screenshot Guide**: *[Statistics tab with metrics and charts]*

### Metric Cards

**Three Key Metrics Displayed**:

1. **Total Assessments**
   - Count of all assessments you've completed
   - Includes deleted assessments in historical count
   - Icon: 📊

2. **Average Risk Score**
   - Mean of all your overall health index scores
   - Helps track improvement over time
   - Icon: ⚡

3. **Average BMI**
   - Mean BMI across all assessments
   - Weight management trend indicator
   - Icon: ⚖️

**Screenshot Guide**: *[Three metric cards showing example values]*

### Risk Distribution Pie Chart

**What It Shows**:
- Breakdown of your assessments by risk level
- Color-coded segments:
  - 🟢 Green: Low risk assessments
  - 🟠 Orange: Moderate risk assessments
  - 🔴 Red: High risk assessments

**How to Read**:
- Larger green segment = Consistently low risk (good!)
- Larger orange/red segments = Areas needing attention
- Hover over segments for exact counts

**Example**:
- Low: 5 assessments (50%)
- Moderate: 3 assessments (30%)
- High: 2 assessments (20%)

**Screenshot Guide**: *[Pie chart with three colored segments and legend]*

### Risk Level Breakdown

**What It Shows**:
- Horizontal bars for each risk level
- Percentage of total assessments
- Actual count displayed

**Example Display**:
```
Low Risk:      ████████████████░░░░ 8 (80%)
Moderate Risk: ██░░░░░░░░░░░░░░░░░░ 2 (20%)
High Risk:     ░░░░░░░░░░░░░░░░░░░░ 0 (0%)
```

**Screenshot Guide**: *[Risk level breakdown with horizontal bars]*

### Using Statistics

**Track Progress**:
- Complete regular assessments (weekly/monthly)
- Watch average risk score decrease over time
- Monitor BMI trending toward healthy range

**Identify Patterns**:
- See which risk level is most common for you
- Notice seasonal variations (exercise patterns)
- Understand impact of lifestyle changes

**Set Goals**:
- Target: Move assessments from Moderate to Low
- Aim for average risk score below 30
- Maintain BMI in normal range (18.5-24.9)

---

## Admin Dashboard

### Overview

System monitoring, performance metrics, and audit log access for administrators.

**⚠️ Note**: In the demo version, admin features are accessible to all users. In production, this would require admin authentication.

### Accessing Admin Dashboard

1. From Dashboard, click **🔧 Admin** tab
2. Dashboard loads with system metrics
3. All data fetched from backend in real-time

**Screenshot Guide**: *[Admin dashboard showing all sections]*

### System Status

**Location**: Top card with green gradient

**Health Indicator**:
- ✅ **Healthy**: All systems operational
- ⚠️ **Degraded**: Some issues detected  
- 🛑 **Error**: Critical system failure

**Status Details**:
- Current system health
- Backend connectivity
- Database status
- Performance status

**Screenshot Guide**: *[System status card showing "Healthy" with checkmark]*

### System Metrics

**Four Key Metrics**:

1. **📊 Total Assessments**
   - Count across all users
   - System-wide statistic
   - Tracks platform usage

2. **⚡ Average Risk Score**
   - Mean risk score across all assessments
   - Population-level health indicator
   - Helps identify trends

3. **⚖️ Average BMI**
   - Mean BMI across all users
   - Population health metric
   - Obesity tracking

4. **🚀 Avg Response Time**
   - API performance metric
   - Typically: <100ms
   - Target: <3000ms
   - Status: "optimal" when <1000ms

**Screenshot Guide**: *[Four metric cards in grid layout]*

### Risk Distribution

**Location**: Middle section with horizontal bars

**What It Shows**:
- Percentage breakdown of all assessments
- Low / Moderate / High risk distribution
- Color-coded bars:
  - 🟢 Green: Low risk
  - 🟠 Orange: Moderate risk
  - 🔴 Red: High risk

**Example**:
```
Low Risk (0-30):      ████████████░░░░░░░░ 12 (60%)
Moderate Risk (30-60): ████████░░░░░░░░░░░ 8 (40%)
High Risk (60-100):    ░░░░░░░░░░░░░░░░░░░ 0 (0%)
```

**What It Means**:
- High percentage of low-risk = Healthy user population
- High percentage of high-risk = Need intervention programs
- Balanced distribution = Diverse user base

**Screenshot Guide**: *[Risk distribution with three horizontal bars]*

### Recent Activity (Audit Logs)

**Location**: Bottom section, scrollable table

**Table Columns**:
1. **Timestamp** - When action occurred (YYYY-MM-DD HH:MM:SS)
2. **Action** - Type of action (CREATE, READ, UPDATE, DELETE, EXPORT)
3. **Resource** - What was affected (assessment, user, system)
4. **Status** - Success or Failure
5. **User ID** - Who performed the action

**Action Badges**:
- 🟦 **CREATE** - Blue badge - New assessment created
- 🟩 **READ** - Green badge - Data viewed
- 🟨 **UPDATE** - Yellow badge - Data modified
- 🟥 **DELETE** - Red badge - Data deleted
- 🟪 **EXPORT** - Purple badge - Data exported

**Status Indicators**:
- ✅ **Success** - Green badge - Action completed
- ❌ **Failure** - Red badge - Action failed

**Example Log Entry**:
```
2024-11-30 22:45:32 | CREATE | assessment | Success | test_user
2024-11-30 22:44:18 | READ   | history    | Success | john_doe
2024-11-30 22:40:05 | EXPORT | watch_data | Success | test_user
```

**Screenshot Guide**: *[Audit logs table with sample entries]*

### Refreshing Data

1. Click **"🔄 Refresh"** button (top-right)
2. Button shows loading spinner
3. All metrics reload simultaneously
4. Takes 1-2 seconds typically

**When to Refresh**:
- After new assessments completed
- To check real-time system status
- When monitoring active usage
- After system changes

### Empty State

If no audit logs exist:
- Message: "No audit logs available"
- Reason: New system or logs cleared
- Logs will appear as users interact with system

**Screenshot Guide**: *[Empty audit logs state with message]*

---

## Troubleshooting

### Common Issues

#### Issue: "API Error" in header

**Symptoms**:
- Red dot next to username
- "API Error" instead of "API Connected"
- Features don't work

**Causes**:
- Backend server not running
- Wrong backend URL
- Network connectivity issue

**Solutions**:
1. Check if backend is running: `http://localhost:5000/api/health`
2. Restart backend server
3. Check browser console for error messages
4. Verify CORS settings if using custom domain

#### Issue: "Please enter a username" on login

**Symptoms**:
- Pink error message on login screen
- Cannot proceed past login

**Cause**:
- Username field empty

**Solution**:
- Type any username in the field (even a single character)
- Click "Continue as Guest"

#### Issue: Apple Watch button not appearing

**Symptoms**:
- No "Connect Apple Watch" button visible
- Only form fields shown

**Cause**:
- Results already displayed on page

**Solution**:
- Scroll to bottom and click "Calculate Another Risk"
- Form clears and watch button reappears
- OR refresh the page

#### Issue: Apple Watch connection fails

**Symptoms**:
- Button stuck on "Connecting..."
- Error message appears
- Status never shows connected

**Causes**:
- Backend watch API not responding
- Network timeout

**Solutions**:
1. Wait 5 seconds and try again
2. Refresh the page
3. Check backend logs for errors
4. Manually enter data instead

#### Issue: Charts not displaying

**Symptoms**:
- White spaces where charts should be
- "Loading..." forever
- Console errors about Chart.js

**Causes**:
- Chart.js library failed to load
- Browser compatibility issue
- JavaScript error

**Solutions**:
1. Refresh the page (Ctrl+R / Cmd+R)
2. Clear browser cache
3. Try different browser (Chrome, Firefox)
4. Check browser console for errors

#### Issue: Form submission button disabled

**Symptoms**:
- "Calculate Risk" button grayed out
- Cannot click button
- No response when clicking

**Causes**:
- Form validation errors
- Missing required fields
- Values out of allowed range

**Solutions**:
1. Check all 8 fields are filled
2. Look for red borders on fields (invalid values)
3. Ensure:
   - Age: 1-150
   - Weight: 20-500 kg
   - Height: 50-300 cm
   - Systolic BP: 50-250 mmHg
   - Diastolic BP: 30-150 mmHg
   - Cholesterol: 100-400 mg/dL
   - Exercise: Selected from dropdown
4. Fix invalid values and try again

#### Issue: History not loading

**Symptoms**:
- "No assessment history found" message
- But you've completed assessments
- Recent assessment missing

**Causes**:
- Different username used
- Browser local storage cleared
- Database connection issue

**Solutions**:
1. Verify you're using same username as when you did assessment
2. Check if using same browser/device
3. Try refreshing the page
4. Check backend logs for database errors

#### Issue: Statistics showing 0

**Symptoms**:
- All metric cards show 0
- No pie chart displayed
- Empty statistics page

**Cause**:
- No assessments completed under this username

**Solution**:
- Complete at least one risk assessment
- Statistics will populate automatically
- Refresh statistics tab after completing assessment

### Performance Issues

#### Slow page loading

**Solutions**:
- Close unnecessary browser tabs
- Clear browser cache
- Check network speed
- Restart browser

#### Slow calculation

**Solutions**:
- Wait a few more seconds (should be <3s)
- Check backend server performance
- Look for backend error messages
- Restart backend server

### Browser Compatibility

**Recommended Browsers**:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Not Supported**:
- ❌ Internet Explorer (any version)
- ❌ Older browser versions
- ❌ Browsers with JavaScript disabled

### Mobile Issues

**Current Status**: 
- Designed for desktop/tablet (1024px+ width)
- Mobile responsive down to 768px
- Some features may not work optimally on small screens

**Recommendations**:
- Use tablet (landscape mode) or desktop
- Minimum 768px screen width
- Portrait mode on tablets may have layout issues

---

## Frequently Asked Questions

### General Questions

**Q: Is MEDAI-Lite a real medical diagnosis tool?**  
A: No. MEDAI-Lite is an educational demonstration of AI-assisted health risk assessment. Always consult qualified healthcare professionals for medical advice. This tool does not diagnose, treat, or prevent any disease.

**Q: How accurate are the risk assessments?**  
A: The assessments use evidence-based algorithms similar to those in clinical practice, but they are simplified for educational purposes. They provide general risk estimates, not definitive medical diagnoses.

**Q: Can I use this for multiple people?**  
A: Yes! Each person should use a different username to keep their assessment history separate. The system tracks assessments by username.

**Q: Is my health data secure?**  
A: In this demo version, data is stored locally in your browser and in the backend database. For production use, additional security measures (encryption, authentication) would be implemented.

**Q: Can I export my assessment data?**  
A: Currently, you can view and take screenshots of your results. A PDF export feature is planned for future versions.

### Technical Questions

**Q: What technology does MEDAI-Lite use?**  
A: 
- **Frontend**: React.js with Chart.js for visualizations
- **Backend**: Flask (Python) with SQLite database
- **Architecture**: Multi-agent system (CardioAgent, MetabolicAgent, NeuroAgent)

**Q: Why do I need to enter health data manually?**  
A: The Apple Watch integration is a simulation for demonstration. Real device integration would require:
- Actual HealthKit API access
- iOS device with paired Apple Watch
- User authorization for health data access
- Production-level security and privacy compliance

**Q: How fast should the assessment be?**  
A: Target response time is under 3 seconds. Current implementation typically responds in under 100 milliseconds (0.1 seconds).

**Q: Can I run this on my own server?**  
A: Yes! MEDAI-Lite is designed to be deployable to your own infrastructure. See the README.md for installation and deployment instructions.

### Assessment Questions

**Q: What do the risk scores mean?**  
A:
- **Low Risk (0-30)**: Minimal health concerns in this domain
- **Moderate Risk (30-60)**: Some areas needing attention
- **High Risk (60-100)**: Significant concerns, professional consultation recommended

**Q: Why are there three agents?**  
A: Different aspects of health are interconnected but distinct. The multi-agent approach provides:
- Specialized assessment in each domain
- More comprehensive overall evaluation
- Identification of specific areas needing attention

**Q: How is the overall score calculated?**  
A: Weighted average of three agent scores:
- CardioAgent: 35% weight
- MetabolicAgent: 35% weight
- NeuroAgent: 30% weight

Example: (15.5×0.35) + (14.5×0.35) + (13.5×0.30) = 14.55

**Q: Should I try to get a score of 0?**  
A: No. A score of exactly 0 is not realistic or necessary. Scores under 30 indicate low risk and good health. Focus on maintaining low-risk status and following recommendations.

**Q: How often should I complete assessments?**  
A: For general monitoring: monthly or quarterly. If making lifestyle changes: weekly or bi-weekly to track progress. During stable health: annual assessments may suffice.

### Apple Watch Questions

**Q: Why is the Apple Watch integration simulated?**  
A: This is a demonstration/educational version. Real Apple Watch integration requires:
- Apple Developer account and HealthKit entitlements
- iOS app (cannot be done from web)
- User authorization and privacy compliance
- Production infrastructure

**Q: What data does the simulated watch provide?**  
A: Realistic health metrics including:
- Age (45-65 range)
- Physical stats (height, weight)
- Blood pressure (realistic ranges)
- Cholesterol levels
- Exercise frequency
- Smoking status

**Q: Can I connect a real Apple Watch?**  
A: Not in this demo version. The "Connect Apple Watch" feature simulates the connection and generates realistic sample data for demonstration purposes.

**Q: Will my imported watch data be saved?**  
A: Once you click "Import to Form", the data populates the form fields. When you click "Calculate Risk", the assessment is saved to your history like any manual entry.

### Admin Questions

**Q: Who can access the Admin Dashboard?**  
A: In this demo, all users can access admin features. In production, this would require admin-level authentication and authorization.

**Q: What are audit logs used for?**  
A: Audit logs track system activity for:
- Security monitoring
- Compliance requirements
- Troubleshooting issues
- Usage analytics
- Understanding user behavior

**Q: Can I delete audit logs?**  
A: Yes, via the cleanup API endpoint (requires direct API call). Manual cleanup retains logs for minimum 30 days. Automatic cleanup runs with 90-day retention policy.

**Q: What does "optimal" response time mean?**  
A: Response times under 1000ms (1 second) are considered optimal. The system typically responds in <100ms, which is excellent performance.

---

## Getting Help

### Support Resources

1. **Documentation**
   - README.md - Quick start and installation
   - ARCHITECTURE.md - Technical system design
   - IMPLEMENTATION_STATUS.md - Development progress
   - This guide (USER_GUIDE.md)

2. **In-App Help**
   - Hover tooltips on form fields
   - Error messages with guidance
   - Status indicators for system health

3. **Troubleshooting**
   - Check [Troubleshooting section](#troubleshooting) above
   - Review browser console for errors (F12 → Console)
   - Check backend logs for server errors

### Reporting Issues

When reporting issues, please include:

1. **What you were trying to do**
2. **What actually happened**
3. **Browser and version** (Chrome 96, Firefox 95, etc.)
4. **Screenshots** (if applicable)
5. **Error messages** (from browser console if any)
6. **Steps to reproduce** (so we can fix it)

**Example Issue Report**:
```
Issue: Cannot connect Apple Watch

What I tried: Clicked "Connect Apple Watch" button
What happened: Button stuck on "Connecting..." for 30 seconds
Browser: Chrome 96.0.4664.110
Screenshot: [attached]
Console error: "Failed to fetch watch/connect - 500 Internal Server Error"
Steps to reproduce:
1. Go to Risk Calculator tab
2. Click "Connect Apple Watch"
3. Wait - button never completes connection
```

---

## Appendix

### Glossary of Terms

**Assessment**: A single health risk calculation based on your input data

**Agent**: Specialized AI component focusing on one health domain (Cardio, Metabolic, Neuro)

**Aggregator**: System that combines results from all agents into overall health index

**Risk Score**: Numerical value (0-100) representing health risk level

**Risk Level**: Category (Low/Moderate/High) based on risk score

**BMI**: Body Mass Index - weight (kg) / height (m)²

**Systolic BP**: Top blood pressure number (pressure during heartbeat)

**Diastolic BP**: Bottom blood pressure number (pressure between heartbeats)

**Audit Log**: Record of system activity for security and compliance

**Session**: Your active login period from login to logout

### Health Metrics Reference

**Blood Pressure Categories** (Systolic/Diastolic):
- Optimal: <120 / <80
- Normal: 120-129 / 80-84
- High Normal: 130-139 / 85-89
- Grade 1 Hypertension: 140-159 / 90-99
- Grade 2 Hypertension: 160-179 / 100-109
- Grade 3 Hypertension: ≥180 / ≥110

**Cholesterol Levels** (Total):
- Desirable: <200 mg/dL
- Borderline High: 200-239 mg/dL
- High: ≥240 mg/dL

**BMI Categories**:
- Underweight: <18.5
- Normal: 18.5-24.9
- Overweight: 25-29.9
- Obese Class I: 30-34.9
- Obese Class II: 35-39.9
- Obese Class III: ≥40

**Exercise Recommendations**:
- Minimum: 3 days/week (150 min moderate activity)
- Optimal: 5+ days/week (300 min moderate activity)

### Keyboard Shortcuts

**Navigation**:
- Tab - Move to next form field
- Shift+Tab - Move to previous field
- Enter - Submit form (when all fields valid)
- Esc - Close modals

**Browser**:
- Ctrl/Cmd+R - Refresh page
- F12 - Open developer tools
- Ctrl/Cmd+Shift+Delete - Clear cache

---

**Document End**

For technical details, see ARCHITECTURE.md  
For development status, see IMPLEMENTATION_STATUS.md  
For installation instructions, see README.md

**Version**: 1.0  
**Last Updated**: November 30, 2025 
**Next Update**: As features are added

---

## Quick Reference Card

### Risk Calculator Quick Steps
1. Login with any username
2. Click "📊 Risk Calculator" tab
3. Option A: Click "Connect Apple Watch" → "View Data" → "Import to Form"
4. Option B: Manually enter 8 health metrics
5. Click "Calculate Risk"
6. Review results (overall index, 3 agents, recommendations)
7. Check History and Statistics tabs

### Risk Score Interpretation
- 0-30: 🟢 Low Risk (Good health)
- 30-60: 🟠 Moderate Risk (Needs attention)
- 60-100: 🔴 High Risk (Consult professional)

### Support Checklist
- □ Checked troubleshooting section
- □ Reviewed browser console
- □ Tried different browser
- □ Refreshed the page
- □ Restarted backend server
- □ Still need help? Gather error details and report issue