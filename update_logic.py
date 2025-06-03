import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import yfinance as yf
import os
import base64
import tempfile

def load_credentials():
    encoded = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not encoded:
        raise Exception("GOOGLE_CREDENTIALS_JSON not set in environment")

    decoded = base64.b64decode(encoded)
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".json") as f:
        f.write(decoded.decode())
        return f.name  # returns the temp file path
    
    
def get_stock_data():
    SHEET_NAME = "Shares_Tracker"
    CREDENTIALS_FILE = load_credentials()

    # print(len(CREDENTIALS_FILE))
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
    except Exception as e:
        return f"❌ Error during Google Sheets authorization: {e}"
    
    rows = sheet.get_all_values()
    headers = rows[0]
    data_rows = rows[2:]
    stocks = []
    for row in data_rows:
        stocks.append({
            "date": row[0],
            "name": row[1],
            "quantity": row[3],
            "buy_price": row[4],
            "current_price": row[5],
            "profit_loss": row[8],
            "profit_loss_percent": row[9],
        })
    return stocks


def update_stock_prices():
    SHEET_NAME = "Shares_Tracker"
    CREDENTIALS_FILE = load_credentials()

    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
    except Exception as e:
        return f"❌ Error during Google Sheets authorization: {e}"

    try:
        rows = sheet.get_all_values()
        headers = rows[0]
        data_rows = rows[1:]

        today = datetime.now().strftime("%-d %B")

        total_investment = 0
        total_current_value = 0
        total_profit_loss = 0
        total_quantity = 0

        batch_updates = []
        log_messages = []

        for i, row in enumerate(data_rows, start=2):
            symbol = row[2]
            try:
                qty = float(row[3])
                buy_price = float(row[4])
            except ValueError:
                log_messages.append(f"⚠️ Skipping row {i} due to invalid qty/buy price.")
                continue

            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d")
                if hist.empty:
                    log_messages.append(f"⚠️ No data for {symbol} at row {i}.")
                    continue
                live_price = hist["Close"].iloc[-1]
            except Exception as e:
                log_messages.append(f"⚠️ Could not fetch price for {symbol} at row {i}: {e}")
                continue

            investment = round(qty * buy_price, 2)
            current_value = round(qty * live_price, 2)
            profit_loss = round((live_price - buy_price) * qty, 2)
            try:
                profit_loss_percent = round(((live_price - buy_price) / buy_price) * 100, 2)
            except ZeroDivisionError:
                profit_loss_percent = 0.0

            total_investment += investment
            total_current_value += current_value
            total_profit_loss += profit_loss
            total_quantity += qty

            batch_updates.extend([
                {'range': f'F{i}', 'values': [[round(live_price, 2)]]},
                {'range': f'I{i}', 'values': [[profit_loss]]},
                {'range': f'J{i}', 'values': [[profit_loss_percent]]},
                {'range': f'A{i}', 'values': [[today]]}
            ])

        # Detect total row
        last_row = rows[-1]
        if len(last_row) > 1 and last_row[1].strip().lower() == "total":
            total_row_index = len(rows)  # existing total row to update
        else:
            total_row_index = len(rows) + 1  # append new total row
        batch_updates.extend([
            {'range': f'B{total_row_index}', 'values': [["Total"]]},
            {'range': f'D{total_row_index}', 'values': [[round(total_quantity, 2)]]},
            {'range': f'G{total_row_index}', 'values': [[round(total_investment, 2)]]},
            {'range': f'H{total_row_index}', 'values': [[round(total_current_value, 2)]]},
            {'range': f'I{total_row_index}', 'values': [[round(total_profit_loss, 2)]]},
            {'range': f'J{total_row_index}', 'values': [[round((total_profit_loss / total_investment) * 100, 2) if total_investment else 0.0]]}
        ])

        sheet.batch_update(batch_updates)

        log_messages.append(f"✅ Updated {len(data_rows)} rows with totals.")

        return " ".join(log_messages)

    except Exception as e:
        return f"❌ Error during update: {e}"
