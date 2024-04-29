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
        sorted_df_json = fit_data.to_json(orient='index')
        return jsonify({'sorted_dataframe': sorted_df_json})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)