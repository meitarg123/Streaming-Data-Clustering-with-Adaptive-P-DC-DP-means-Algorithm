import socket, pickle, struct
import cv2
import numpy as np
import matplotlib.image as img
from pdc_dp_means import DPMeans

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.47'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")  # Q: unsigned long long integer(8 bytes)

def data_to_frame(centroids, cluster_labels, h, w, c):
    rgb_cols = [[0, 0, 0] for center in centroids]
    j = 0
    for center in centroids:
        for i in range(len(center)):
            rgb_cols[j][i] = (center[i] * 256).round(0).astype(int)
        j = j + 1
    numpy_rgb_cols = np.array([])
    numpy_rgb_cols = np.array([entity for entity in rgb_cols], np.uint8)
    numpy_cluster_labels = np.array(cluster_labels)
    img_quant = np.reshape(numpy_rgb_cols[numpy_cluster_labels], (h, w, c))  # assigning points to the clusters
    return img_quant

dpmeans = DPMeans(n_clusters=1, n_init=10, delta=0.1)  # n_init and delta parameters

# Business logic to receive data frames, and unpack it and de-serialize it and show video frame on client side
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
        if not packet: break
        data += packet  # append the data packet got from server into data variable
    packed_msg_size = data[:payload_size]  # will find the packed message size i.e. 8 byte, we packed on server side.
    data = data[payload_size:]  # Actual frame data
    msg_size = struct.unpack("Q", packed_msg_size)[0]  # meassage size
    # print(msg_size)

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)  # will receive all frame data from client socket
    frame_data = data[:msg_size]  # recover actual frame data
    data = data[msg_size:]
    frame = pickle.loads(frame_data)  # de-serialize bytes into actual frame type

    # frame as array
    # img.imsave("frame.png", frame)
    # img_arr = img.imread("frame.png")
    (h, w, c) = frame.shape
    img2D = frame.reshape(h * w, c)

    # create model

    img2D = img2D/256

    # run algo
    dpmeans.fit(img2D)
    cluster_labels = dpmeans.predict(img2D)
    centroids = dpmeans.cluster_centers_

    # reconstract new frame
    frame = data_to_frame(centroids, cluster_labels, h, w, c)

    cv2.imshow("RECEIVING VIDEO", frame)  # show video frame at client side
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # press q to exit video
        break
        client_socket.close()

# import socket, pickle, struct, cv2
# from pdc_dp_means import DPMeans
# import matplotlib.image as img
# import numpy as np
#
#
# def data_to_frame(centroids, cluster_labels, h, w, c):
#     print("data_to_frame | 10")
#     rgb_cols = [[0, 0, 0] for center in centroids]
#     j = 0
#     print(len(centroids))
#     print(len(rgb_cols))
#     print(centroids)
#     for center in centroids:
#         for i in range(len(center)):
#             rgb_cols[j][i] = (center[i] * 256).round(0).astype(int)
#         j = j + 1
#     numpy_rgb_cols = np.array([])
#     numpy_rgb_cols = np.array([entity for entity in rgb_cols], np.uint8)
#     numpy_cluster_labels = np.array(cluster_labels)
#     img_quant = np.reshape(numpy_rgb_cols[numpy_cluster_labels], (h, w, c))  # assigning points to the clusters
#     return img_quant
#
#
# # create socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '172.16.112.63'  # paste your server ip address here
# port = 9999
# client_socket.connect((host_ip, port))  # a tuple
# data = b""
# payload_size = struct.calcsize("Q")  # Q: unsigned long long integer(8 bytes)
#
# # create model
# dpmeans = DPMeans(n_clusters=1, n_init=10, delta=10)  # n_init and delta parameters
#
# # Business logic to receive data frames, and unpack it and de-serialize it and show video frame on client side
# while True:
#     while len(data) < payload_size:
#         packet = client_socket.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
#         if not packet: break
#         data += packet  # append the data packet got from server into data variable
#     packed_msg_size = data[:payload_size]  # will find the packed message size i.e. 8 byte, we packed on server side.
#     data = data[payload_size:]  # Actual frame data
#     msg_size = struct.unpack("Q", packed_msg_size)[0]  # meassage size
#     # print(msg_size)
#
#     while len(data) < msg_size:
#         data += client_socket.recv(4 * 1024)  # will receive all frame data from client socket
#     frame_data = data[:msg_size]  # recover actual frame data
#     data = data[msg_size:]
#     frame = pickle.loads(frame_data)  # de-serialize bytes into actual frame type
#
#     # # frame as array
#     # img.imsave("frame.png", frame)
#     # img_arr = img.imread("frame.png")
#     # (h, w, c) = img_arr.shape
#     # img2D = img_arr.reshape(h * w, c)
#     #
#     # # run algo
#     # dpmeans.fit(img2D)
#     # cluster_labels = dpmeans.predict(img2D)
#     # centroids = dpmeans.cluster_centers_
#
#     # # reconstract new frame
#     # frame = data_to_frame(centroids, cluster_labels, h, w, c)
#
#     cv2.imshow("RECEIVING VIDEO", frame)  # show video frame at client side
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):  # press q to exit video
#         break
#     client_socket.close()
#
# # frame0 to data
