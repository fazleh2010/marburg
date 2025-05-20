import csv

# Data to visualize
story_events = [
    {"date": "2020-01-01", "headline": "Start of Project", "text": "The research begins."},
    {"date": "2020-06-01", "headline": "First Results", "text": "Initial findings released."},
    {"date": "2021-01-01", "headline": "Public Launch", "text": "Project is made public."},
]

# Create a StorylineJS-compatible CSV
with open("storyline_data.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["date", "headline", "text"])
    writer.writeheader()
    for event in story_events:
        writer.writerow(event)

print("CSV written. You can import it into StorylineJS.")
