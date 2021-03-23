def spark():
    import findspark
    findspark.init()
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName('BCHI preprocessing') \
        .config("spark.sql.broadcastTimeout", "3600000") \
        .getOrCreate()
    return spark


def read_dataset(file, spark, delimiter):
    data = spark.read.format("com.databricks.spark.csv") \
        .options(header='true', inferschema='true') \
        .option("delimiter", delimiter) \
        .load(file, header=True)

    data = data.fillna(0)

    return data


def sorted_data(data, sorted_cols):
    data = data.select(sorted_cols)
    return data


def data_dict(data):
    from pyspark.sql.functions import count, col, when
    df = data.select([count(when(col(c).isNotNull(), c)).alias(c) for c in data.columns])
    dict = list(map(lambda row: row.asDict(), df.collect()))[0]
    return dict


def sorted_dict(data):
    dict = data_dict(data)
    sorted_dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}

    return sorted_dict


def dict_cols(dict):
    cols = [c for c in dict.keys()]
    return cols


def dict_values(dict):
    values = [v for v in dict.values()]
    return values


def sorted_cols(dict):
    sorted_cols = dict_cols(dict)
    sorted_cols.reverse()
    return sorted_cols


def sorted_values(dict):
    sorted_values = dict_values(dict)
    sorted_values.reverse()
    return sorted_values


def column_to_list(data, col_name):
    l = list(set(data.select(col_name).rdd.flatMap(lambda x: x).collect()))

    return l


def add_filter(filters_list, column_index, column):
    from clustering import kmeans
    filters_list.append((column_index, kmeans(column)))
    return filters_list


def save_criteria(criteria_list, path):
    from pandas import DataFrame
    df = {'Criteria': criteria_list}
    df = DataFrame(df, columns=['Criteria'])
    df.to_csv(path + "criteria.csv")


def save_data_hdfs(data, hdfs_path):
    data = rename_cols(data)
    data.write.save(hdfs_path, format='parquet', mode='append')


def rename_cols(data):
    spark()
    cols = ["col" + str(i) for i in range(len(data.columns))]
    data = data.toDF(*cols)
    return data


def discrete_columns(data):
    cols = []
    for e in data.dtypes:
        if e[1] != 'double':
            cols.append(e[0])
    return cols


def build_discrete_filters(data):
    spark()
    filters = {}
    cols = discrete_columns(data)
    for col in cols:
        l = list(set(data.select(col).rdd.flatMap(lambda x: x).collect()))
        filters[col] = l
    return filters


def cols_for_clustering(data):
    cols = []
    for e in data.dtypes:
        if e[1] == 'double':
            cols.append(e[0])
    return cols


def add_filter(filters_set, key, values_list):
    filters_set[key] = values_list
    return filters_set


def get_list(df, col):
    ls = df.select(col).rdd.flatMap(lambda x: x).collect()
    return ls


def network_vis_array(data, cols):
    values_array = []
    for col in cols:
        values_array.append((get_list(data, col)))
    return values_array
