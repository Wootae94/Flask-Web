from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt 
import os
from flask import current_app
def clustering(df_csv,k_number):       
        # 전처리 - 정규화
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_csv.iloc[:, :-1])

        # 차원 축소(PCA)
        pca = PCA(n_components=2)
        pca_array = pca.fit_transform(X_scaled)
        df = pd.DataFrame(pca_array, columns=['pca_x', 'pca_y'])
        df['target'] = df_csv.iloc[:, -1].values

        # K-Means Clustering
        kmeans = KMeans(n_clusters=k_number, init='k-means++', max_iter=300, random_state=2021)
        kmeans.fit(X_scaled)
        df['cluster'] = kmeans.labels_

        # 시각화
        markers = ['s', 'o', '^', 'P', 'D', 'H', 'x']
        plt.figure()
        for i in df.target.unique():
            marker = markers[i]
            x_axis_data = df[df.target == i]['pca_x']
            y_axis_data = df[df.target == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.title('Original Data Visualization by 2 PCA Components')
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster0.png')
        plt.savefig(img_file)

        plt.figure()
        for i in range(k_number):
            marker = markers[i]
            x_axis_data = df[df.cluster == i]['pca_x']
            y_axis_data = df[df.cluster == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.title(f'{k_number} Clusters Visualization by 2 PCA Components')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster1.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        return mtime