"""
clustering.py
-------------
Performs log clustering to group similar log messages together.

Current approach:
- Text vectorization using TF-IDF
- Clustering using K-Means

This module is a lightweight placeholder and can be
replaced by LogAI semantic clustering models.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster_logs(logs, num_clusters=5):
    """
    Cluster log messages into groups based on textual similarity.

    Args:
        logs (list): List of log dictionaries with key 'message'
        num_clusters (int): Number of clusters to form

    Returns:
        dict: {
            cluster_id: [log1, log2, ...]
        }
    """

    if not logs:
        return {}

    # Extract log messages
    messages = [log["message"] for log in logs if "message" in log]

    if len(messages) < num_clusters:
        num_clusters = max(1, len(messages))

    # Convert text to TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500
    )
    X = vectorizer.fit_transform(messages)

    # Apply K-Means clustering
    kmeans = KMeans(
        n_clusters=num_clusters,
        random_state=42,
        n_init=10
    )
    labels = kmeans.fit_predict(X)

    # Group logs by cluster label
    clustered_logs = {}
    for label, log in zip(labels, logs):
        clustered_logs.setdefault(int(label), []).append(log)

    return clustered_logs
