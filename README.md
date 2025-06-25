# 📊 Shares Tracker (Live Stock Portfolio Viewer)

A clean and minimal **stock portfolio tracker** web app that shows real-time updates from a connected Google Sheet. Perfect for personal use or as a portfolio project.

---

## 🚀 Features

- 📈 Tracks investments with current stock prices
- 🔄 Manual "Update Now" button with loader animation
- 🧠 Auto calculates:
  - Profit / Loss
  - Profit / Loss Percentage
- 🌐 Pulls data live from a Google Sheet via Python + Flask
- 📅 Periodic refresh every 5 minutes

---

## 🖼️ Preview

> <img width="1196" alt="Screenshot 2025-06-25 at 12 10 19 PM" src="https://github.com/user-attachments/assets/69fad20c-bfe1-4acf-8eac-be4867220e46" />

---

## 🛠️ Tech Stack

| Layer     | Tech              |
|-----------|-------------------|
| Frontend  | HTML + CSS + JS   |
| Backend   | Python (Flask)    |
| Data      | Google Sheets API |
| Hosting   | Run locally or on Render/Railway |

---

## 📁 Project Structure

```bash
Shares_Tracker/
├── app.py                   # Flask app
├── templates/
│   └── index.html           # Frontend UI
├── static/
│   └── style.css (optional)
├── creds.json               # Google Sheets credentials
├── requirements.txt
└── README.md
```


# 🔧 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Pahatsahil/Shares_Tracker.git
cd Shares_Tracker
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google Sheets API

✅ You’ll need to set up Google Sheets API and a service account to fetch data.

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a **new project**
- Enable **Google Sheets API**
- Create **Service Account Credentials**
- Download the `credentials.json` file
- Rename it to `creds.json`
- Share your Google Sheet with the **service account email**


### 4. Run the Flask App

```bash
python app.py
```

### Visit in browser: http://127.0.0.1:5000

# ✨ Upcoming Features

- 📱 Mobile responsive design
- 📊 Chart.js or D3.js for visualizing performance
- 🔔 Email alerts for price thresholds
