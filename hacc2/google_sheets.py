from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime  # ✅ Import datetime

# Define Google Sheets API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Load credentials from the service account JSON file
json_path = r"service-account1.json"
creds = Credentials.from_service_account_file(json_path, scopes=SCOPES)

# Authorize client
client = gspread.authorize(creds)

# Google Sheets details
GOOGLE_SHEET_ID = "1ZvWDI_dlPPzIulMIiuJqC2GwwQFNwUu7nzfFAyMq_d8"
spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
worksheet = spreadsheet.sheet1  

# Fetch data from Google Sheets
data = worksheet.get_all_values()

if not data or len(data) < 2:
    print("No data found in the sheet.")
    exit()

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')

# Extract headers and customer data
headers = data[0]  
customer_data = data[1:]

# Ensure required columns exist
try:
    due_date_index = headers.index("Due-Date")
    status_index = headers.index("Call Status")
    response_index = headers.index("Customer Response")
except ValueError as e:
    print(f"Error: Missing column in the sheet: {e}")
    exit()

# Filter customers whose loan is due today
due_today = [row for row in customer_data if len(row) > due_date_index and row[due_date_index] == today_date]

# Function to update call status
def update_call_status(row_number, status):
    worksheet.update_cell(row_number + 1, status_index + 1, status)
    print(f"Updated row {row_number} with status: {status}")

# Function to update customer response
def update_customer_response(row_number, response):
    worksheet.update_cell(row_number + 1, response_index + 1, response)
    print(f"Updated row {row_number} with response: {response}")

# Print customers with due payments today
if due_today:
    print(f"{len(due_today)} customers have due payments today.")
else:
    print("No customers with due payments today.")