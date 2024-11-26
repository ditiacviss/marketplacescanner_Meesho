import json
import matplotlib.pyplot as plt
import io

def result_plot(input_json):

    details_data = json.loads(input_json)
    uids = []
    scores = []

    for uid, details in details_data.items():
        uids.append(uid)
        scores.append(details.get('Acviss_Score', 0))  # Default to 0 if Acviss_Score is missing

    # Set colors based on the score thresholds
    colors = ['green' if score > 80 else 'yellow' if 60 <= score <= 80 else 'red' for score in scores]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(uids, scores, color=colors)
    plt.xlabel('UID')
    plt.ylabel('Acviss Score')
    plt.title('Acviss Score corresponding to UID')
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='PNG')
    buffer.seek(0)
    return buffer
