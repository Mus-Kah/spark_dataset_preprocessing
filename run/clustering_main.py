file = "../data/BCHI.csv"
from utils.utils import read_dataset, spark
from clustering.kmeans import kmeans_list
from utils.utils import column_to_list, cols_for_clustering

if __name__ == '__main__':
    spark = spark()
    data = read_dataset(file=file, spark=spark, delimiter=",")
    cols_for_clustering = cols_for_clustering(data)
    if cols_for_clustering:
        for col in cols_for_clustering:
            print(kmeans_list(column_to_list(data, col)))