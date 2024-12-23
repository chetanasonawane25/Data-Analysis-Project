import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the Datasets
file_path = "C:\\Users\\niles\\Downloads\\Data Analyst Intern Assignment - Excel.xlsx"
excel_data = pd.ExcelFile(file_path)

# Load each sheet into DataFrames
user_details = excel_data.parse("UserDetails.csv")
cooking_sessions = excel_data.parse("CookingSessions.csv")
order_details = excel_data.parse("OrderDetails.csv")

# Step 2: Data Cleaning
# Check for missing values
print("Missing Values in User Details:")
print(user_details.isnull().sum())
print("\nMissing Values in Cooking Sessions:")
print(cooking_sessions.isnull().sum())
print("\nMissing Values in Order Details:")
print(order_details.isnull().sum())

# Handle missing values (example: drop rows with missing values)
user_details.dropna(inplace=True)
cooking_sessions.dropna(inplace=True)
order_details.dropna(inplace=True)

user_details.columns = user_details.columns.str.replace(" ", "_")
cooking_sessions.columns = cooking_sessions.columns.str.replace(" ", "_")
order_details.columns = order_details.columns.str.replace(" ", "_")

# Step 3: Merge Datasets
merged_data = pd.merge(cooking_sessions, order_details, on=["User_ID", "Session_ID"], how="inner")
merged_data = pd.merge(merged_data, user_details, on="User_ID", how="inner")

# Validate merged data
print("\nMerged Data Sample:")
print(merged_data)

# Step 4a: Analyze Relationship Between Cooking Sessions and Orders
user_activity = merged_data.groupby("User_ID").agg({
    "Session_ID": "count",
    "Order_ID": "count"
}).rename(columns={"Session_ID": "total_sessions", "Order_ID": "total_orders"})

# Plot the relationship
sns.scatterplot(x="total_sessions", y="total_orders", data=user_activity)
plt.title("Relationship Between Cooking Sessions and Orders")
plt.xlabel("Total Cooking Sessions")
plt.ylabel("Total Orders")
plt.savefig("visualizations/relationship_sessions_orders.png")
plt.show()

# Step 4b: Identify Popular Dishes
popular_dishes = merged_data["Dish_Name_x"].value_counts()

# Plot popular dishes
popular_dishes.head(3).plot(kind="bar", title="Top 3 Dishes")
plt.xlabel("Dish Name")
plt.ylabel("Frequency")
plt.savefig("visualizations/popular_dishes.png")
plt.show()

# Step 4c: Explore Demographics
demographic_analysis = merged_data.groupby("Location").agg({
    "Session_ID": "count",
    "Order_ID": "count"
}).rename(columns={"Session_ID": "total_sessions", "Order_ID": "total_orders"})

print("\nDemographic Analysis:")
print(demographic_analysis)

# Plot demographic trends
demographic_analysis.plot(kind="bar", figsize=(10, 6), title="Demographics Analysis")
plt.xlabel("Region")
plt.ylabel("Count")
plt.savefig("visualizations/demographics_analysis.png")

