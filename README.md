# Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm
# Mini-Project in Unsupervised Learning

**Instructed by:** Oren Freifeld

### Our Project

The aim of this project is to modify the (P)DC-DP-means algorithm to effectively handle streaming data, considering support for concept drift over time and the potential variability in the number of clusters.

In this report, we present our project on modifying the (P)DC-DP-means algorithm to handle streaming data effectively, considering concept drift and varying numbers of clusters. Our infrastructure comprises a server-client setup, where the adapted algorithm is executed on the client side. We conducted experiments using two-dimensional datasets to examine the algorithm's performance under varying data patterns and assess its adaptability to evolving clusters.

---

### Clustering Algorithms

In the opening assignment, we were introduced to K-means and DP-means algorithms:

- **K-means algorithm**: A widely used clustering algorithm that aims to partition a dataset into a predefined number of K distinct clusters. It iteratively assigns data points to clusters based on their proximity to cluster centroids and updates the centroids until convergence or reaching a limitation on the iteration number.
  
- **DP-means algorithm**: An extension of the K-means algorithm that determines the optimal number of clusters instead of requiring it to be predefined. The algorithm initializes with a single centroid and dynamically creates new clusters when the distance between a data point and existing centroids exceeds a predefined threshold.

DP-means algorithm faces challenges such as limited utilization of BLAS’ optimizations due to dynamic cluster creation, sensitivity to observation visitation order, and the risk of over-clustering when naively splitting the data.

- **The solution - (P)DC-DP-means**, addresses the challenges of the previous algorithm by delaying cluster creation, incrementing K by 1 per iteration. These changes enable K-means-like optimizations, increase stability, eliminate sensitivity to ordering, and improve processing speed.

---

### Concept Drift

Concept drift refers to the phenomenon where the statistical properties of data change over time, causing models to become less accurate or outdated. It occurs due to environmental shifts or evolving patterns. Detecting and adapting to concept drift is vital for maintaining model effectiveness in dynamic environments.

To handle concept drift in clustering algorithms, we implemented a solution by setting a minimum threshold for the number of data points within a cluster. If a cluster had fewer points than the threshold, we excluded it from further analysis. This approach allowed us to adapt to changing patterns by focusing on clusters that maintained a meaningful representation of the data. By disregarding clusters with few points, we mitigated the impact of potential noise or outliers, resulting in improved clustering accuracy in the presence of concept drift.

---

### Methodology

#### Seamless Data Streaming: Server-Client Architecture

We implemented a server-client architecture for real-time video transmission. To achieve a continuous stream of video data, we made modifications to the code. Specifically, we adapted the server-client code to capture frames from a webcam as the video source in real-time. By incorporating this modification, the server component obtained frames directly from the webcam and transmitted them to the client seamlessly. This enhancement enabled a smooth and efficient real-time video streaming experience, ensuring a continuous flow of data throughout the transmission process.

#### Self-Implementation Endeavor

First, we followed the provided pseudo-code to implement the (P)DC-DP-means algorithm. To accommodate evolving data patterns, we introduced a formula that assigned a decaying weight to each frame as we progressed forward in time. However, we encountered challenges with computational efficiency, prompting us to explore alternative approaches to enhance the algorithm's speed. We decided to adapt Or Dinari's algorithm specifically for streaming data. This adaptation allowed us to achieve better efficiency while effectively managing concept drift and addressing the variability in the number of clusters encountered in streaming scenarios.

#### Or Dinari’s Algorithm Adaptation

In our adaptation of Or Dinari's Algorithm for streaming data, we implemented a strategy to handle the inclusion of previous frames. Specifically, we saved two frames backward at each iteration and assigned weights to them accordingly. The frame preceding the previous one was given a weight of 1/7, the previous frame received a weight of 2/7, and the current frame was assigned a weight of 4/7. This weighting scheme allowed us to effectively consider the influence of previous frames while placing more emphasis on the most recent data.

Additionally, to address the challenge of varying cluster numbers encountered in streaming scenarios, we introduced a cluster removal mechanism. This mechanism is invoked after each "fit" call. We set a threshold for the minimum number of points assigned to a cluster and removed clusters that fell below this threshold. This approach enabled us to ensure that only meaningful clusters were retained.

#### Examining Two-Dimensional Dataset

We conducted an examination of the modified algorithm using two-dimensional data. This choice allowed us to visualize the results more easily and gain insights into the clustering performance. In the results section of our report, we include informative graphs and visualizations that depict the clustering outcomes, providing a clear representation of the algorithm's effectiveness in handling the given data.

---

### Results

In the following 2-dimensional results (figures 1-3) we examined our model with lambda value of 0.2:

- **Figure 1: Concept Drift**

  ![Figure 1: Concept Drift](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure1_concecptDrift.jpg)

  The concept drift is apparent as the algorithm fails to adapt, persistently perceiving multiple clusters instead of recognizing the concept of a single cluster despite the consistency of a batch of points in the subsequent frames.
  
- **Figure 2: Moving Clusters (data patterns)**

  ![Figure 2: Moving Clusters](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure2_movingClusters.jpg)

  The data points depicted in the figure exhibit movement, yet the clustering model successfully maintains a consistent number of clusters. This demonstrates the algorithm's robustness in capturing and grouping the data points effectively, ensuring stable and reliable clustering results despite the dynamic nature of the data.
  
- **Figure 3: Varying Number of Clusters**

  ![Figure 3: Varying Number of Clusters](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure3_VaryingBumberOfClusters.jpg)

  In Frame 0, there are four distinct clusters, while Frame 1 shows a reduced number of two clusters, consequently influencing Frames 2 and 3 as expected. However, in Frame 4, there is a recovery as the algorithm successfully detects and re-establishes the original four clusters, highlighting its adaptability to variations in the number of clusters within the data.
  
- **Figure 4: Endless Data Stream (webcam) - using delta value of 0.7**

  ![Figure 4: Endless Data Stream](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure4_endless_data_stream%20.jpg)
  
- **Figures 5,6: Video Recoloring using delta value of 0.2**

  ![Figure 5: Video Recoloring](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure5_videoRecoloring.jpg)
  
  ![Figure 6: Video Recoloring](https://github.com/meitarg123/Streaming-Data-Clustering-with-Adaptive-P-DC-DP-means-Algorithm/blob/main/Figure6_video_recoloring2.jpg)

---

### Conclusions

- In conclusion, our approach to handling concept drift by removing irrelevant clusters in response to new and different data frames has proven effective in addressing this challenge. Although the model requires a few frames (specifically, two frames) to fully adapt to the new situation, the removal of irrelevant clusters allows the algorithm to dynamically adjust and maintain accurate cluster assignments, as can be seen in Figure 1. This demonstrates the importance of incorporating adaptive mechanisms to effectively handle concept drift and ensure the model's responsiveness to changing data patterns.

- From an applicative point of view, the presence of multiple clusters in tasks such as video repainting does not affect the performance of the algorithm. This is because the objective is to modify colors rather than the clustering itself. Empty or insignificant clusters resulting from concept drift have no actual impact on the successful execution of recoloring.

- Adapting clustering algorithms to streaming data offers both advantages and disadvantages. Modeling each frame independently can potentially yield more accurate results per frame, as it allows for precise analysis of individual data points, overshadowing concept drifts and varying number of clusters. However, this approach fails to capture the underlying data patterns, such as the trends of specific centroids over an extended period.

- As a potential avenue for future research, it is suggested to incorporate the tracking and analysis of centroid trends and movements in the context of streaming data. This extension would serve to underscore the advantages of streaming data, showcasing the potential in analyzing continuous data streams - an analysis that can give deeper insights into the dynamics of evolving data patterns.

