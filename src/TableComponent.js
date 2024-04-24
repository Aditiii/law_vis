import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import jsonData from './data.json';
import './tableStyles.css';

const TableComponent = () => {
    const tableData = Object.entries(jsonData).map(([law, states]) => {
        return {
            id: law,
            law,
            ...states
        };
    });

    const columns = [
        { field: 'law', headerName: 'Laws', width: 400, headerClassName: 'bold-header' },
        ...Object.keys(jsonData[tableData[0].law]).map(state => ({
            field: state,
            headerName: state,
            renderCell: (params) => {
                const value = params.value;
                return <div className={value === 1 ? 'green-cell' : ''}>{value}</div>;
            },
            width: 0.01
        }))
    ];

    const rowClassRules = {
        'bold-row': (params) => params.id === tableData[0].id
    };

    return (
        <div style={{ height: '50%', overflow: 'auto' }}> {/* Set the height and overflow properties */}
            <div style={{ height: '70%', width: '100%' }}>
                <DataGrid
                    rows={tableData}
                    columns={columns}
                    checkboxSelection
                    getRowClassName={(params) => 'no-padding-row'}
                    getCellClassName={(params) => 'no-padding-cell'}
                    rowClassRules={rowClassRules}
                />
            </div>
        </div>
    );
};


export default TableComponent;
