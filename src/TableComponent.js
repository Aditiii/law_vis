import React, { useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import jsonData from './data.json';
import './tableStyles.css';

const TableComponent = () => {
    const gridApiRef = useRef(null);
    const tableData = Object.entries(jsonData).map(([law, states]) => {
        return {
            id: law,
            law,
            ...states
        };
    });

    const columnDefs = [
        {
            headerName: '',
            field: 'checkbox',
            checkboxSelection: true,
            headerCheckboxSelection: true,
            width: 35,
            cellStyle: {marginLeft: 17},
            pinned: 'left'
        },
        { 
            headerName: 'Laws', 
            field: 'law',
            width: 300, 
            cellStyle: {textAlign: 'left', marginLeft: 18},
            pinned: 'left',
            filter: true
        },
            ...Object.keys(jsonData[tableData[0].law]).map(state => ({
            headerName: state,
            field: state,
            // cellClass: params => {
            //     return params.value === 1 ? 'green-cell' : '';
            // },
            cellRenderer: params => {
                return params.value === 1 ? <div className="green-cell" style={{width: '100%', height: '100%'}}></div> : '';
            },
            filter: true,
            width: 75
        }))
    ];

    // const rowClassRules = {
       
    // };

    const handleCluster = () => {
        // Add clustering logic here
        console.log('Cluster button clicked');
    };

    const onSelectionChanged = (event) => {
    
        const selectedRows = event.api.getSelectedRows();
        console.log("Selected Rows:", selectedRows);
        console.log('Selection changed');
    };

    return (
        <div>
            <div style={{ textAlign: 'center', margin: '20px 0' }}>
                <button type="button" className="btn btn-dark" onClick={handleCluster}>Cluster</button>
            </div>
            <div className="ag-theme-alpine" style={{ height: '650px', width: '97%',paddingLeft: '3%' }}>
                <AgGridReact
                    rowData={tableData}
                    columnDefs={columnDefs}
                    enableFilter={true}
                    rowSelection='multiple'
                    rowMultiSelectWithClick = {true}
                    onSelectionChanged={onSelectionChanged}
                    onGridReady={(params) => {
                        gridApiRef.current = params.api;
                    }}
                />
            </div>
        </div>
    );
};

export default TableComponent;
