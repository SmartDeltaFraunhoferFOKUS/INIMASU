import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def visualize(issues):
    labels = [issue.labels if issue.labels else 'No Label' for issue in issues]
    created_dates = [datetime.strptime(issue.created_at, '%Y-%m-%dT%H:%M:%SZ') if issue.created_at else None for issue in issues]
    closed_dates = [datetime.strptime(issue.closed_at, '%Y-%m-%dT%H:%M:%SZ') if issue.closed_at else None for issue in issues]
    updated_dates = [datetime.strptime(issue.updated_at, '%Y-%m-%dT%H:%M:%SZ') if issue.updated_at else None for issue in issues]
    bodies = [len(issue.body) if issue.body else 0 for issue in issues]
    # Plot: Body Length vs. Answer Time
    answer_times = [(closed - created).days if closed and created else None for created, closed in
                    zip(created_dates, closed_dates)]
    plt.figure(figsize=(20, 20))
    plt.scatter(bodies, answer_times)
    plt.xlabel('Body Length')
    plt.ylabel('Answer Time (in days)')
    plt.title('Body Length vs. Answer Time')
    plt.show()

    """
    # Plot: Label vs. Answer Time
    answer_times = [(closed - created).days if closed and created else None for created, closed in zip(created_dates, closed_dates)]
    plt.figure(figsize=(8, 6))
    plt.scatter(labels, answer_times)
    plt.xlabel('Label')
    plt.ylabel('Answer Time (in days)')
    plt.title('Label vs. Answer Time')
    plt.xticks(rotation=90)
    plt.show()

    # Plot: Body Length vs. Tags
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=labels, y=bodies)
    plt.xlabel('Label')
    plt.ylabel('Body Length')
    plt.title('Body Length vs. Tags')
    plt.xticks(rotation=90)
    plt.show()
 """