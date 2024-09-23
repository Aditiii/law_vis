from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin
from sklearn.cluster import SpectralBiclustering
import numpy as np
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
        # Set 'law' as the index
        df.set_index('law', inplace=True)
        # Remove the 'id' column as it is redundant with 'law'
        df.drop(columns=['id'], inplace=True)
        df=df.replace(0,0.01)
        model = SpectralBiclustering(n_clusters=2, random_state=0)
        model.fit(df)
        print(model.row_labels_)
        print(model.column_labels_)
        fit_data = df.iloc[np.argsort(model.row_labels_)]
        fit_data = fit_data.iloc[:, np.argsort(model.column_labels_)]
        row_labels_list = model.row_labels_.tolist()
        column_labels_list = model.column_labels_.tolist()
        response = {
        'row_labels': row_labels_list,
        'column_labels': column_labels_list
        }

        # Sorting DataFrame by row and column labels
        #df.sort_index(inplace=True)  # Sort by row labels
        #df = df.reindex(sorted(df.columns), axis=1)  # Sort by column labels

        # # Get sorted indices (order of labels in the sorted DataFrame)
        # sorted_row_indices = list(df.index)
        # sorted_column_indices = list(df.columns)
        fit_data=fit_data.replace(0.01,0)
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

if __name__ == '__main__':
    app.run(port=8000, debug=True)