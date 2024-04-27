from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin
from sklearn.cluster import SpectralBiclustering

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
        result = {}
        for item in data:
            result[item["id"]] = {key: value for key, value in item.items() if key != "id"}
        print(result)
        result = {}
        for item in data:
            result[item["id"]] = {key: value for key, value in item.items() if key != "id"}

        print(result)

        # Assuming the first element in each row array is the row label
        row_labels = [row[0] for row in data['rows']]
        data_only = [row[1:] for row in data['rows']]

        # Create DataFrame using data and excluding the row label from columns
        df = pd.DataFrame(data_only, index=row_labels, columns=data['columns'][1:])

        # Sorting DataFrame by row and column labels
        df.sort_index(inplace=True)  # Sort by row labels
        df = df.reindex(sorted(df.columns), axis=1)  # Sort by column labels

        # Get sorted indices (order of labels in the sorted DataFrame)
        sorted_row_indices = list(df.index)
        sorted_column_indices = list(df.columns)
        sorted_df_json = df.to_json(orient='split')

        return jsonify({'sorted_row_indices': sorted_row_indices, 'sorted_column_indices': sorted_column_indices,  'sorted_dataframe': sorted_df_json})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)