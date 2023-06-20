import matplotlib.pyplot as plt
import datetime
import seaborn as sns
from matplotlib.gridspec import GridSpec

def visualizeDates(created_dates, closed_dates):
    # Create a dictionary to store the counts and average times per month
    months_data = {}

    # Calculate the counts and average times per month
    for created_date, closed_date in zip(created_dates, closed_dates):
        created_month_year = created_date.strftime("%Y-%m")
        if created_month_year not in months_data:
            months_data[created_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0, "average_time": 0}
        months_data[created_month_year]["created_count"] += 1

        if closed_date:  # Check if closed_date exists
            closed_month_year = closed_date.strftime("%Y-%m")
            if closed_month_year not in months_data:
                months_data[closed_month_year] = {"created_count": 0, "closed_count": 0, "total_time": 0, "average_time": 0}
            months_data[closed_month_year]["closed_count"] += 1
            answer_time = (closed_date - created_date).days
            months_data[closed_month_year]["total_time"] += answer_time

    # Extract the month-year values and sort them
    month_years = sorted(months_data.keys())

    # Extract the counts and average times per month
    created_counts = [months_data[month_year]["created_count"] for month_year in month_years]
    closed_counts = [months_data[month_year]["closed_count"] for month_year in month_years]
    average_times = [months_data[month_year]["total_time"] / months_data[month_year]["closed_count"] if months_data[month_year]["closed_count"] != 0 else 0 for month_year in month_years]
    difference_counts = [created - closed for created, closed in zip(created_counts, closed_counts)]

    # Generate the x-axis labels in the format "YYYY-MM"
    x_labels = [datetime.datetime.strptime(month_year, "%Y-%m").strftime("%Y-%m") for month_year in month_years]

    # Set seaborn style
    sns.set()

    # Create GridSpec for flexible subplots arrangement
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 1, figure=fig)

    # Plotting the created, closed, and difference issues per month
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x_labels, created_counts, label="Created Issues", color="blue")
    ax1.plot(x_labels, closed_counts, label="Closed Issues", color="orange")
    ax1.plot(x_labels, difference_counts, label="Difference", color="green")
    ax1.set_xlabel("Month-Year")
    ax1.set_ylabel("Number of Issues")
    ax1.set_title("Number of Created, Closed, and Difference Issues per Month")
    ax1.legend()
    ax1.set_xticklabels(x_labels, rotation=45)

    # Plotting the average time to close issues per month
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x_labels, average_times, marker="o", color="green")
    ax2.set_xlabel("Month-Year")
    ax2.set_ylabel("Average Time to Close (days)")
    ax2.set_title("Average Time to Close Issues per Month")
    ax2.set_xticklabels(x_labels, rotation=45)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the plot
    plt.show()
