file = "../data/BCHI.csv"
from utils.utils import read_dataset, spark
from clustering.kmeans import kmeans_list
from utils.utils import column_to_list

if __name__ == '__main__':
    spark = spark()
    data = read_dataset(file=file, spark=spark, delimiter=",")
    print(kmeans_list(column_to_list(data, "Value")))