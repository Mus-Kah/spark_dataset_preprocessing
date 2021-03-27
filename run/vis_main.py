"""
Descripttion:
Author: Moustafa Sadek Kahil
Date: 13/11/2020
"""


file = "../data/BCHI.csv"
from utils.utils import read_dataset, spark, sorted_dict, sorted_cols, sorted_values, build_discrete_filters, \
    discrete_columns, cols_for_clustering
from utils.utils import  data_dict, dict_values, dict_cols, save_data_hdfs, sorted_data, add_filter, column_to_list
from vis.visualization import visualize_combinations, visualize_columns, hierarchical_visualization, \
    visualize_cols_stats
from clustering.kmeans import kmeans_list

if __name__ == '__main__':
    spark = spark()
    data = read_dataset(file=file, spark=spark, delimiter=",")

    dict = data_dict(data)

    sorted_dict = sorted_dict(data)

    #print(sorted_cols(sorted_dict))

    visualize_columns(dict_cols(dict), dict_values(dict), "Columns before sorting")

    visualize_columns(sorted_cols(sorted_dict), sorted_values(sorted_dict), "Columns After sorting")

    visualize_combinations(sorted_cols(sorted_dict), sorted_values(sorted_dict), "Columns Combinations")

    #visualize_cols_stats(data)

    filters_set=build_discrete_filters(data)

    #filters_set=add_filter(filters_set, "Value", kmeans_list(column_to_list(data, "Value")))
    for col in cols_for_clustering(data):
        #print(col)
        filters_set = add_filter(filters_set, col, kmeans_list(column_to_list(data, col)))

    hierarchical_visualization(data,sorted_cols(sorted_dict), 20)

    #hier_test()

    save_data_hdfs(sorted_data(data, sorted_cols(sorted_dict)), hdfs_path='../processed_data')
