import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import filedialog


# Function to save documents into CSV and JSON file
def save_dataframe(data_frame, csv_file_name, json_file_name):
    if data_frame is None or data_frame.empty:
        print(f"Warning: No data to save in {csv_file_name} and {json_file_name}."
              f"The dataframe is empty.")
        return False
    try:
        data_frame.to_csv(csv_file_name, index=False)
        data_frame.to_json(json_file_name, orient="records", indent=4)
        print(f"{csv_file_name} successfully saved as CSV.")
        print(f"{json_file_name} successfully saved as JSON.")
        return True
    except PermissionError:
        print("Error: Permission denied for file!")
        return False
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


# Window for file selection
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select your bank statement")
print(f"You selected: {file_path}")

# Read dataset
if file_path:
    try:
        df = pd.read_excel(file_path)
        # Check if the file is empty
        if df.empty:
            print("Error: The file is empty!")
            exit(1)
        print("Excel file successfully loaded!\n")
        print("First 5 rows:")
        print(df.head())
        # Check the required columns
        required_columns = {"Date", "Balance"}  # Set
        if not required_columns.issubset(df.columns):
            raise KeyError(f"Missing required columns: {required_columns - set(df.columns)}")

        # Data cleaning
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
        df = df.dropna(subset=["Date"])  # Delete NaN (Not a Number)
        df = df.sort_values("Date").reset_index(drop=True)
        df["Balance_cleaned"] = df["Balance"].str.replace(",", "").astype(float)
        df = df.dropna(subset=["Balance_cleaned"])  # Delete NaN

        # Create a Months column
        df["Months"] = df["Date"].dt.strftime("%Y-%m")

        # Select the last value of the month
        df_monthly = df.groupby("Months").last().reset_index()

        # Count monthly transactions
        df_monthly_sum = df.groupby("Months").size().reset_index(name="Transaction Count")

        # Save DataFrames into CSV and JSON file
        save_dataframe(df_monthly, "monthly_balance_trend.csv",
                       "monthly_balance_trend.json")
        save_dataframe(df_monthly_sum, "monthly_transaction_count.csv",
                       "monthly_transaction_count.json")


        # 1. Diagram: Area chart for Monthly Balance Trend
        fig1 = px.area(df_monthly, x="Months", y="Balance_cleaned",
                       title="Monthly Balance Trend",
                       color_discrete_sequence=["#02a0e8"],  # Neon blue color
                       labels={"Months": "Date (Year-Month)",
                               "Balance_cleaned": "Balance (HUF)"},
                       template="plotly_dark", line_shape="spline")
        # Customize the layout
        fig1.update_layout(font_size=18, plot_bgcolor="rgb(117, 120, 117)", )
        fig1.update_xaxes(gridcolor="rgb(117, 120, 117)")
        fig1.update_yaxes(gridcolor="rgb(117, 120, 117)")
        # Show first diagram
        fig1.show()
        # Save the first diagram into HTML file
        fig1.write_html("fig_1.html", auto_open=True)


        # 2. Diagram: Bar chart for Monthly Transaction Count
        fig2 = px.bar(df_monthly_sum, x="Months", y="Transaction Count",
                      title="Monthly Transaction Count",
                      color_discrete_sequence=["rgb(72, 93, 247)"],
                      labels={"Months": "Date (Year-Month)",
                              "Transaction Count": "Number of Transactions"},
                      template="plotly_dark")
        # Customize the layout
        fig2.update_layout(font_size=18,
                           plot_bgcolor="rgb(117, 120, 117)",
                           xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=True, gridwidth=1)
                           )
        # Add value labels to the bars
        fig2.update_traces(texttemplate='%{y:,.0f}', textposition='outside',
                           marker=dict(
                               line=dict(width=2, color="DarkSlateGrey")))
        # Show second diagram
        fig2.show()
        # Save the second diagram into HTML file
        fig2.write_html("fig2.html", auto_open=True)

    except FileNotFoundError:
        print(f"Error: File {file_path} not found!")
        exit(1)
    except KeyError:
        print("ERROR: Required columns are missing!")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
else:
    print("No file selected.")








