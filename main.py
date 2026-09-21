import csv
import os

FILENAME = "expenses.csv"

# Function to save an expense directly to a CSV file
def save_expense_to_file(amount, category, description):
    file_exists = os.path.exists(FILENAME)
    
    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write headers if the file is being created for the first time
        if not file_exists:
            writer.writerow(["Amount (ILS)", "Category", "Description"])
        
        writer.writerow([amount, category, description])

print("=== Personal Expense Analyzer ===")

while True:
    print("\n--- Add New Expense ---")
    
    category = input("Enter category (or type 'quit' to finish): ")
    if category.lower() == 'quit':
        break
        
    amount = float(input("Enter amount (₪): "))
    description = input("Enter description: ")

    # Save to CSV file automatically
    save_expense_to_file(amount, category, description)
    print(f"✓ Saved ₪{amount:.2f} under '{category}' to {FILENAME}!")

# Display current stored expenses
print("\n==================================")
print("     ALL STORED EXPENSES (CSV)    ")
print("==================================")

total = 0.0
if os.path.exists(FILENAME):
    with open(FILENAME, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            amt = float(row["Amount (ILS)"])
            print(f"• {row['Category'].title()}: ₪{amt:.2f} ({row['Description']})")
            total += amt

print(f"\nTotal Spent So Far: ₪{total:.2f}")