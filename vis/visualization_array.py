import numpy as np
def visualization_array(cols, vals):
    vis_array=np.zeros((len(cols), len(cols)), int)
    for i in range(1, len(vis_array)):
        vis_array[0][i] = vals[i]
        vis_array[i][0] = vals[i]

    for i in range(1, len(vis_array)):
        for j in range(1, len(vis_array)):
            if i != j:
                vis_array[i][j] = vis_array[i - 1][j]

    for i in range(len(vis_array) - 1, 1, -1):
        for j in range(1, len(vis_array)):
            if i != j:
                vis_array[i][j] = vis_array[j][i]

    return vis_array