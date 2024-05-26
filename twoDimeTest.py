import numpy as np
from sklearn.datasets import make_blobs
from pdc_dp_means import DPMeans
import matplotlib.pyplot as plt

fig, axes_tuple = plt.subplots(2, 5, figsize=(10, 5), subplot_kw={'aspect': 'equal'}, sharex=True, sharey=True)
dpmeans = DPMeans(n_clusters=1, n_init=10, delta=30)  # n_init and delta parameters

n_samples = 300
X, y_true = make_blobs(n_samples=n_samples, centers=4, cluster_std=0.60, random_state=1)

# data movement vector
movement_direction = (1, 1)
movement_scale = 0.1

temp = np.copy(X)
temp_colours = y_true

for i in range(5):
    if (i == 1):
        X, y_true = make_blobs(n_samples=300, centers=2, cluster_std=0.60, random_state=2)
    else:
        X = temp
        y_true = temp_colours

    movement = np.array(movement_direction) * 0.1
    X += movement

    # Apply DPMeans clustering
    dpmeans.fit(X)
    dpmeans.update_clusters_for_streaming(X)
    # Predict the cluster for each data point
    y_dpmeans = dpmeans.predict(X)

    # Plotting generated clusters
    axes_tuple[((i // 5) * 2)][i % 5].scatter(X[:, 0], X[:, 1], c=y_true, s=20, alpha=0.5, cmap='viridis')
    axes_tuple[((i // 5) * 2)][i % 5].set_title(f'Generated {i}')

    # Plotting clustered labeling
    axes_tuple[((i // 5) * 2) + 1][i % 5].scatter(X[:, 0], X[:, 1], c=y_dpmeans, s=50, cmap='viridis')
    axes_tuple[((i // 5) * 2) + 1][i % 5].set_title(f'PDCDPMEANS {i}')

    # Plotting centroids
    centers = dpmeans.cluster_centers_
    axes_tuple[((i // 5) * 2) + 1][i % 5].scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

plt.tight_layout()
plt.show()
