// import { AgGridReact } from 'ag-grid-react'; // React Grid Logic
// import "ag-grid-community/styles/ag-grid.css"; // Core CSS
// import 'ag-grid-community/styles/ag-theme-alpine.css';
// import { useEffect, useState } from 'react';
// import jsonData from './data.json';
// import jsonData1 from './onedataset.json';

// const DataGrid = () => {
//     const [colDefs, setColDefs] = useState([]);
//     const [rowData, setRowData] = useState([]);

//     useEffect(() => {
//         const keys = Object.keys(jsonData[0]).slice(3);       
//         jsonData.map(row => {
//             keys.map((key) => {
//                 if(row[key] === 1)
//                     row[key] = 'Yes';
//                 else
//                     row[key] = 'No';
//                 return key;
//             })
//             return row;
//             // rowDD_Law[row.Jurisdictions] = row.DD_Law === 1 ? 'Yes' : 'No';
//             // rowDD_Law2[row.Jurisdictions] = row.DD_Law2 === 1 ? 'Yes' : 'No';
//         });

//         // const rowData = [rowDD_Law, rowDD_Law2];
        
//         setRowData(jsonData);
//         // console.log(jsonData)
//     }, []);

//     useEffect(()=>{
//         const colDefs = [
//             { headerName: 'Laws', field: 'lawType' },
//             ...jsonData.map(row => ({ headerName: row.Jurisdictions, field: row.Jurisdictions }))
//         ];
//         setColDefs(colDefs);
//     },[rowData])

//     return (
//         <div>
//             <div className="ag-theme-alpine" style={{ height: '50vh', width: '100vw' }}>
//                 <AgGridReact
//                     columnDefs={colDefs}
//                     rowData={rowData}
//                     pagination={true}
//                     paginationPageSize={5}
//                 />
//             </div>
//         </div>
//     )
// }

// export default DataGrid;
import React from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const GridComponent = () => {
    const jsonData = {
        "Alabama": {
            "Effective Date": 1416441600000,
            "Valid Through Date": 1506816000000,
            "DD_Law": "Yes",
            "DD_Prestsupp": "No"
        },
        "Alaska": {
            "Effective Date": 1416441600000,
            "Valid Through Date": 1506816000000,
            "DD_Law": "No",
            "DD_Prestsupp": "No"
        }
        // Add more states here...
    };

    // Extract column names dynamically
    const columnNames = Object.keys(jsonData);
    const columnHeaderDefs = columnNames.map((columnName) => ({
    headerName: columnName,
    field: columnName,
    }));
    console.log(columnNames);

    // Extract row headers and data
    const rowHeaderNames = Object.keys(jsonData[columnNames[0]]);
    const rowData = rowHeaderNames.map((rowHeaderName) => {
    const rowDataObj = { jurisdiction: rowHeaderName };
    columnNames.forEach((columnName) => {
        rowDataObj[columnName] = jsonData[columnName][rowHeaderName];
    });
    return rowDataObj;
    });

    // Combine column headers with row headers
    const columnDefs = [
    { headerName: "Jurisdiction", field: "jurisdiction" },
    ...columnHeaderDefs,
    ];
    console.log(rowHeaderNames);
    return (
        <div className="ag-theme-alpine" style={{ height: 2000, width: 6000 }}>
            <AgGridReact
                columnDefs={columnDefs}
                rowData={rowData}
                rowSelection="multiple"
                animateRows={true}
                enableFilter={true}
                enableSorting={true}
                floatingFilter={true}
            />
        </div>
    );
};

export default GridComponent;