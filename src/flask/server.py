from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralCoclustering
from sklearn.cluster import SpectralBiclustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import MDS
from scipy.spatial.distance import pdist, squareform
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
def rearrange_matrix_by_ones(matrix):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)  # Sum of 1's per row

    # Step 2: Sort rows based on the sum of 1's (descending order)
    sorted_row_idx_by_ones = np.argsort(-row_sums)  # Sort in descending order (more 1's first)

    # Step 3: Rearrange the matrix rows based on this sorting
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 4: Compute the sum of 1's in each column of the sorted matrix
    col_sums = np.sum(sorted_matrix, axis=0)  # Sum of 1's per column

    # Step 5: Sort columns based on the sum of 1's (descending order)
    sorted_col_idx_by_ones = np.argsort(-col_sums)  # Sort in descending order (more 1's first)

    # Step 6: Rearrange the sorted matrix columns based on this sorting
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]


    return sorted_matrix, sorted_row_idx_by_ones, sorted_col_idx_by_ones



def rearrange_matrix_by_ones_and_clustering(matrix, n_clusters=2):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)  # Sum of 1's per row

    # Step 2: Sort rows based on the sum of 1's (descending order)
    sorted_row_idx_by_ones = np.argsort(-row_sums)  # Sort in descending order (more 1's first)

    # Step 3: Rearrange the matrix rows based on this sorting
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 4: Compute the sum of 1's in each column of the sorted matrix
    col_sums = np.sum(sorted_matrix, axis=0)  # Sum of 1's per column

    # Step 5: Sort columns based on the sum of 1's (descending order)
    sorted_col_idx_by_ones = np.argsort(-col_sums)  # Sort in descending order (more 1's first)

    # Step 6: Rearrange the sorted matrix columns based on this sorting
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]

    # Step 7: Apply agglomerative clustering on the rows
    row_clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='jaccard', linkage='complete').fit(sorted_matrix)
    sorted_row_idx_by_clustering = np.argsort(row_clustering.labels_)
    clustered_matrix = sorted_matrix[sorted_row_idx_by_clustering, :]

    # Step 8: Apply agglomerative clustering on the columns (transpose to cluster columns as rows)
    col_clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='jaccard', linkage='complete').fit(clustered_matrix.T)
    sorted_col_idx_by_clustering = np.argsort(col_clustering.labels_)
    clustered_matrix = clustered_matrix[:, sorted_col_idx_by_clustering]

    return clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering




#rearrange_matrix_by_ones_and_clustering(sorted_data_kmeans, 6)




def rearrange_matrix_by_ones_and_kmeans(matrix, n_clusters=2):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)

    # Step 2: Sort rows based on the sum of 1's
    sorted_row_idx_by_ones = np.argsort(-row_sums)
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 3: Sort columns based on the sum of 1's
    col_sums = np.sum(sorted_matrix, axis=0)
    sorted_col_idx_by_ones = np.argsort(-col_sums)
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]

    # Step 4: Apply KMeans clustering on the rows (set n_init explicitly)
    row_clustering = KMeans(n_clusters=n_clusters, n_init=10).fit(sorted_matrix)
    sorted_row_idx_by_clustering = np.argsort(row_clustering.labels_)
    clustered_matrix = sorted_matrix[sorted_row_idx_by_clustering, :]

    # Step 5: Apply KMeans clustering on the columns (set n_init explicitly)
    col_clustering = KMeans(n_clusters=n_clusters, n_init=10).fit(clustered_matrix.T)
    sorted_col_idx_by_clustering = np.argsort(col_clustering.labels_)
    clustered_matrix = clustered_matrix[:, sorted_col_idx_by_clustering]
    return clustered_matrix,sorted_row_idx_by_clustering, sorted_col_idx_by_clustering



# Example usage
#rearrange_matrix_by_ones_and_kmeans(sorted_data_kmeans, 6)



def rearrange_matrix_by_spectral_co_clustering(matrix, n_clusters=2):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)
    sorted_row_idx_by_ones = np.argsort(-row_sums)
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 2: Sort columns based on the sum of 1's
    col_sums = np.sum(sorted_matrix, axis=0)
    sorted_col_idx_by_ones = np.argsort(-col_sums)
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]

    # Step 3: Apply Spectral Co-clustering
    co_clustering = SpectralCoclustering(n_clusters=n_clusters, random_state=0).fit(sorted_matrix)
    sorted_row_idx_by_clustering = np.argsort(co_clustering.row_labels_)
    clustered_matrix = sorted_matrix[sorted_row_idx_by_clustering, :]

    sorted_col_idx_by_clustering = np.argsort(co_clustering.column_labels_)
    clustered_matrix = clustered_matrix[:, sorted_col_idx_by_clustering]

    return clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering


# Example usage
#rearrange_matrix_by_spectral_co_clustering(sorted_data_kmeans, 6)



def rearrange_matrix_by_spectral_bi_clustering(matrix, n_clusters=2):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)
    sorted_row_idx_by_ones = np.argsort(-row_sums)
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 2: Sort columns based on the sum of 1's
    col_sums = np.sum(sorted_matrix, axis=0)
    sorted_col_idx_by_ones = np.argsort(-col_sums)
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]

    # Step 3: Apply Spectral Bi-clustering
    bi_clustering = SpectralBiclustering(n_clusters=n_clusters, random_state=0).fit(sorted_matrix)
    sorted_row_idx_by_clustering = np.argsort(bi_clustering.row_labels_)
    clustered_matrix = sorted_matrix[sorted_row_idx_by_clustering, :]

    sorted_col_idx_by_clustering = np.argsort(bi_clustering.column_labels_)
    clustered_matrix = clustered_matrix[:, sorted_col_idx_by_clustering]

    return clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering


def rearrange_matrix_by_spectral_bi_clustering(matrix, n_clusters=2):

    # Step 1: Compute the sum of 1's in each row
    row_sums = np.sum(matrix, axis=1)
    sorted_row_idx_by_ones = np.argsort(-row_sums)
    sorted_matrix = matrix[sorted_row_idx_by_ones, :]

    # Step 2: Sort columns based on the sum of 1's
    col_sums = np.sum(sorted_matrix, axis=0)
    sorted_col_idx_by_ones = np.argsort(-col_sums)
    sorted_matrix = sorted_matrix[:, sorted_col_idx_by_ones]

    # Step 3: Apply Spectral Bi-clustering
    bi_clustering = SpectralBiclustering(n_clusters=n_clusters, random_state=0).fit(sorted_matrix)
    sorted_row_idx_by_clustering = np.argsort(bi_clustering.row_labels_)
    clustered_matrix = sorted_matrix[sorted_row_idx_by_clustering, :]

    sorted_col_idx_by_clustering = np.argsort(bi_clustering.column_labels_)
    clustered_matrix = clustered_matrix[:, sorted_col_idx_by_clustering]

    return clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering

def solve_tsp(dist_matrix):
    num_points = len(dist_matrix)
    
    # Create the routing index manager and model
    manager = pywrapcp.RoutingIndexManager(num_points, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    # Define the distance callback
    def distance_callback(from_index, to_index):
        return int(dist_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting up parameters for TSP
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30

    # Solve the TSP
    solution = routing.SolveWithParameters(search_parameters)

    # Retrieve the path
    if solution:
        path = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            path.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        return path
    else:
        return None

def mds_and_rearrangement(matrix):
    # Step 1: Compute row (law) correlation matrix and apply MDS
    row_correlation_matrix = matrix.T.corr()
    row_correlation_matrix = row_correlation_matrix.fillna(0)
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    row_mds_coords = mds.fit_transform(1 - row_correlation_matrix)  # Using (1 - correlation) as distance

    # Step 2: Solve TSP on rows based on MDS coordinates
    row_dist_matrix = squareform(pdist(row_mds_coords))
    row_order = solve_tsp(row_dist_matrix)
    if row_order:
        tsp_df = matrix.iloc[row_order]  # Reorder rows
    print(row_order)
    # Step 4: Compute the sum of 1's in each column of the sorted matrix
    col_sums = np.sum(tsp_df.values, axis=0)  # Sum of 1's per column

    # Step 5: Sort columns based on the sum of 1's (descending order)
    sorted_col_idx_by_ones = np.argsort(-col_sums)  # Sort in descending order (more 1's first)
    print(sorted_col_idx_by_ones)
    # Step 6: Rearrange the sorted matrix columns based on this sorting
    tsp_df = tsp_df.iloc[:, sorted_col_idx_by_ones]
    return tsp_df, row_order, sorted_col_idx_by_ones

@app.route('/process-grid', methods=['POST'])
@cross_origin()
def process_grid():
    data = request.get_json()
    print("In process grid")
    print(data)
    try:
        # Assuming the first element in each row array is the row label
        # row_labels = [row[0] for row in data['rows']]
        # data_only = [row[1:] for row in data['rows']]

        # Create DataFrame using data and excluding the row label from columns
        df = pd.DataFrame(data['selectedRows'])
        clustering_algo=data.get('cluster','rearrangement')
        dataset_source = df['datasetSource']

        # Set 'law' as the index
        df.set_index('law', inplace=True)
        # Remove the 'id' column as it is redundant with 'law'
        df.drop(columns=['id', 'datasetSource'], inplace=True)
        df=df.replace(0,0.01)
        matrix=df.values
        if clustering_algo=='rearrangement':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = rearrange_matrix_by_ones(matrix)
        elif clustering_algo=='agglomerative_clustering':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = rearrange_matrix_by_ones_and_clustering(matrix, 6)
        elif clustering_algo=='kmeans_clustering':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = rearrange_matrix_by_ones_and_kmeans(matrix, 6)
        elif clustering_algo=='spectral_coclustering':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = rearrange_matrix_by_spectral_co_clustering(matrix, 6)
        elif clustering_algo=='spectral_biclustering':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = rearrange_matrix_by_spectral_bi_clustering(matrix, 6) 
        elif clustering_algo=='mds':
            clustered_matrix, sorted_row_idx_by_clustering, sorted_col_idx_by_clustering = mds_and_rearrangement(df)
        # print(model.row_labels_)
        # print(model.column_labels_)
        # fit_data = df.iloc[np.argsort(model.row_labels_)]
        # fit_data = fit_data.iloc[:, np.argsort(model.column_labels_)]
        # row_labels_list = model.row_labels_.tolist()
        # column_labels_list = model.column_labels_.tolist()
        # response = {
        # 'row_labels': row_labels_list,
        # 'column_labels': column_labels_list
        # }

        # Sorting DataFrame by row and column labels
        #df.sort_index(inplace=True)  # Sort by row labels
        #df = df.reindex(sorted(df.columns), axis=1)  # Sort by column labels

        # # Get sorted indices (order of labels in the sorted DataFrame)
        # sorted_row_indices = list(df.index)
        # sorted_column_indices = list(df.columns)
        new_index = df.index[sorted_row_idx_by_clustering]
        new_columns = df.columns[sorted_col_idx_by_clustering]
        fit_data = pd.DataFrame(clustered_matrix, columns=new_columns, index=new_index)
        fit_data=fit_data.replace(0.01,0)
        # Add the datasetSource column back to the DataFrame
        fit_data['datasetSource'] = dataset_source[sorted_row_idx_by_clustering].values
        sorted_df_json = fit_data.to_json(orient='index')
        return jsonify({'sorted_dataframe': sorted_df_json})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

from collections import deque

def flood_fill_multiple_colors(matrix):
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    color = 5  # Start coloring with 1

    def bfs(start_x, start_y, new_color):
        queue = deque([(start_x, start_y)])
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            
            visited.add((x, y))
            matrix[x][y] = new_color

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if matrix[nx][ny] in {-2, -1} and (nx, ny) not in visited:
                        queue.append((nx, ny))

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] in {-2, -1} and (i, j) not in visited:
                bfs(i, j, color)
                color += 1  # Increment color for the next component

    return matrix

def flood_fill(matrix, x, y, new_color):
    rows = len(matrix)
    cols = len(matrix[0])
    current_color = matrix[x][y]

    # Create a queue for BFS
    queue = [(x, y)]
    
    while queue:
        cx, cy = queue.pop()
        
        # Continue if the current cell is already colored correctly
        if matrix[cx][cy] != current_color:
            continue
        
        # Color the current cell
        matrix[cx][cy] = new_color
        
        # Check and add the four adjacent cells if valid
        if cx > 0:  # Up
            queue.append((cx-1, cy))
        if cx < rows - 1:  # Down
            queue.append((cx+1, cy))
        if cy > 0:  # Left
            queue.append((cx, cy-1))
        if cy < cols - 1:  # Right
            queue.append((cx, cy+1))
     
def fill_all_components(matrix,start_number):
    rows = len(matrix)
    cols = len(matrix[0])
    color = start_number  # Start coloring from 10 to clearly differentiate colors in examples
    
    for x in range(rows):
        for y in range(cols):
            if matrix[x][y] == -2 or matrix[x][y] == -1:  # Assuming original colors are < 10
                flood_fill(matrix, x, y, color)
                color += 10  # Increment the color for the next component
    
@app.route('/flood-fill-route',methods=['POST'])
@cross_origin()
def flood_fill_route():
    data = request.get_json()
    print("In flood fill")
    #print(data)
    try:
        # Assuming the first element in each row array is the row label
        # row_labels = [row[0] for row in data['rows']]
        # data_only = [row[1:] for row in data['rows']]

        # Create DataFrame using data and excluding the row label from columns
        df = pd.DataFrame(data['selectedRows'])
        # Set 'law' as the index
        df.set_index('law', inplace=True)
        # Remove the 'id' column as it is redundant with 'law'
        df.drop(columns=['id'], inplace=True)
        df=df.replace(0,0.01)
        model = SpectralBiclustering(n_clusters=3, random_state=0)
        model.fit(df)
        print(model.row_labels_)
        print(model.column_labels_)

        fit_data = df.iloc[np.argsort(model.row_labels_)]
        fit_data = fit_data.iloc[:, np.argsort(model.column_labels_)]
        sorted_row_indices = np.argsort(model.row_labels_)  # model.row labels [2 0 2 2 2 1 2 0 0 0 2]
        sorted_col_indices = np.argsort(model.column_labels_)
        row_labels_list = model.row_labels_.tolist()
        column_labels_list = model.column_labels_.tolist()
        response = {
        'row_labels': row_labels_list,
        'column_labels': column_labels_list
        }
        fit_data=fit_data.replace(0.01,0)
        sorted_df_json1 = fit_data
        clustered_df = df.copy()
        print(model.row_labels_)
        print(model.column_labels_)
        clustered_df = clustered_df.iloc[np.argsort(model.row_labels_)]
        clustered_df = clustered_df.iloc[:, np.argsort(model.column_labels_)]
        matrix = clustered_df.values
                    
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                if model.row_labels_[i] == model.column_labels_[j]:
                        clustered_df.iloc[i, j] = model.row_labels_[i]
                elif model.row_labels_[i] != model.column_labels_[j]:
                        clustered_df.iloc[i,j] = -2
                else:
                        clustered_df.iloc[i,j] = -1

        # Apply the flood fill to color different componentsc
        max_list1 = max(model.row_labels_)
        max_list2 = max(model.column_labels_)

        # Compare the maximum values
        start_number = max(max_list1, max_list2) + 1
        flood_fill_multiple_colors(matrix)
        #fill_all_components(matrix,start_number)

        # Convert the matrix back to DataFrame with the original index and columns
        clustered_df[:] = matrix
        for i in range(sorted_df_json1.shape[0]):
             for j in range(sorted_df_json1.shape[1]):
                  if model.row_labels_[i] != model.column_labels_[j]:
                       sorted_df_json1.iloc[i,j] = clustered_df.iloc[i][j]
                  
        sorted_df_json2 = sorted_df_json1.to_json(orient='index')
        return jsonify({'sorted_dataframe': sorted_df_json2})
        # Sorting DataFrame by row and column labels
        #df.sort_index(inplace=True)  # Sort by row labels
        #df = df.reindex(sorted(df.columns), axis=1)  # Sort by column labels

        # # Get sorted indices (order of labels in the sorted DataFrame)
        # sorted_row_indices = list(df.index)
        # sorted_column_indices = list(df.columns)
        # fit_data=fit_data.replace(0.01,0)
        # sorted_df_json = fit_data.to_json(orient='index')
        # return jsonify({'sorted_dataframe': sorted_df_json})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# def flood_fill(matrix, x, y, new_color):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     current_color = matrix[x][y]

#     # Create a stack for DFS
#     stack = [(x, y)]
    
#     while stack:
#         cx, cy = stack.pop()
        
#         # Continue if the current cell is already colored correctly
#         if matrix[cx][cy] != current_color:
#             continue
        
#         # Color the current cell
#         matrix[cx][cy] = new_color
        
#         # Check and add the four adjacent cells if valid
#         if cx > 0:  # Up
#             stack.append((cx-1, cy))
#         if cx < rows - 1:  # Down
#             stack.append((cx+1, cy))
#         if cy > 0:  # Left
#             stack.append((cx, cy-1))
#         if cy < cols - 1:  # Right
#             stack.append((cx, cy+1))

# def fill_all_components(matrix,start_number):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     color = start_number  # Start coloring from 10 to clearly differentiate colors in examples
    
#     for x in range(rows):
#         for y in range(cols):
#             if matrix[x][y] == -2 or matrix[x][y] == -1:  # Assuming original colors are < 10
#                 flood_fill(matrix, x, y, color)
#                 color += 10  # Increment the color for the next component

# fill_all_components(matrix,10)

# for row in matrix:
#     print(row)

# def flood_fill(matrix, x, y, new_color):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     current_color = matrix[x][y]

#     # Create a stack for DFS
#     stack = [(x, y)]
    
#     while stack:
#         cx, cy = stack.pop()
        
#         # Continue if the current cell is already colored correctly
#         if matrix[cx][cy] != current_color:
#             continue
        
#         # Color the current cell
#         matrix[cx][cy] = new_color
        
#         # Check and add the four adjacent cells if valid
#         if cx > 0:  # Up
#             stack.append((cx-1, cy))
#         if cx < rows - 1:  # Down
#             stack.append((cx+1, cy))
#         if cy > 0:  # Left
#             stack.append((cx, cy-1))
#         if cy < cols - 1:  # Right
#             stack.append((cx, cy+1))

# def fill_all_components(matrix,start_number):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     color = start_number  # Start coloring from 10 to clearly differentiate colors in examples
    
#     for x in range(rows):
#         for y in range(cols):
#             if matrix[x][y] == -2 or matrix[x][y] == -1:  # Assuming original colors are < 10
#                 flood_fill(matrix, x, y, color)
#                 color += 10  # Increment the color for the next component

# fill_all_components(matrix,10)

# for row in matrix:
#     print(row)

if __name__ == '__main__':
    app.run(port=8000, debug=True)