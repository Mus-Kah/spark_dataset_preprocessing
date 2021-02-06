from pandas import DataFrame
from sklearn.cluster import KMeans
def kmeans_list(col):
    Data = {'x': col}

    df = DataFrame(Data, columns=['x'])

    kmeans = KMeans(n_clusters=20).fit(df)
    centroids = kmeans.cluster_centers_

    return centroids