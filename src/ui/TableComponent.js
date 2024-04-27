import React, { useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import jsonData from './data.json';
import './tableStyles.css';

let cd7 = {"goodsam-law": "Does the jurisdiction have a drug overdose Good Samaritan Law?",
  "goodsam-cs_Arrest": "What protection, if any, does the law provide from controlled substance possession laws? Arrest.",
  "goodsam-cs_Charge": "What protection, if any, does the law provide from controlled substance possession laws? Charge.",
  "goodsam-cs_Prosecution": "What protection, if any, does the law provide from controlled substance possession laws? Prosecution.",
  "goodsam-cs_Law provides an affirmative defense": "What protection, if any, does the law provide from controlled substance possession laws? Law provides an affirmative defense.",
  "goodsam-cs_Law provides other procedural protections": "What protection, if any, does the law provide from controlled substance possession laws? Law provides other procedural protections.",
  "goodsam-cs_None": "What protection, if any, does the law provide from controlled substance possession laws? None.",
  "goodsam-paraphernalia_Arrest": "What protection, if any, does the law provide from drug paraphernalia laws? Arrest.",
  "goodsam-paraphernalia_Charge": "What protection, if any, does the law provide from drug paraphernalia laws? Charge.",
  "goodsam-paraphernalia_Prosecution": "What protection, if any, does the law provide from drug paraphernalia laws? Prosecution.",
  "goodsam-paraphernalia_Law provides an affirmative defense": "What protection, if any, does the law provide from drug paraphernalia laws? Law provides an affirmative defense.",
  "goodsam-paraphernalia_Law provides other procedural protections": "What protection, if any, does the law provide from drug paraphernalia laws? Law provides other procedural protections.",
  "goodsam-paraphernalia_None": "What protection, if any, does the law provide from drug paraphernalia laws? None.",
  "goodsam-paroleyn": "Does the law provide protection from probation or parole violations?",
  "goodsam-parole_Protection from arrest": "What protection does the law provide from probation or parole violations? Protection from arrest.",
  "goodsam-parole_Protection from charge": "What protection does the law provide from probation or parole violations? Protection from charge.",
  "goodsam-parole_Protection from prosecution": "What protection does the law provide from probation or parole violations? Protection from prosecution.",
  "goodsam-parole_Protection from revocation of probation and/or parole": "What protection does the law provide from probation or parole violations? Protection from revocation of probation and/or parole.",
  "goodsam-parole_General protection from sanctions for violation of probation and/or parole": "What protection does the law provide from probation or parole violations? General protection from sanctions for violation of probation and/or parole.",
  "goodsam-mitigation": "Is reporting an overdose considered a mitigating factor in sentencing?",
  "goodsam-mit-type_Controlled substances offenses": "For what types of crimes is mitigation permitted? Controlled substances offenses.",
  "goodsam-mit-type_Alcohol-related offenses": "For what types of crimes is mitigation permitted? Alcohol-related offenses.",
  "goodsam-mit-type_Other offenses beyond controlled substances and alcohol-related violations": "For what types of crimes is mitigation permitted? Other offenses beyond controlled substances and alcohol-related violations."
}

const TableComponent = () => {
    let selectedRows = [];
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
            width: '300vw', 
            cellStyle: {textAlign: 'left', marginLeft: 18},
            pinned: 'left',
            filter: true,
            tooltipShowDelay: 0,
            tooltipValueGetter: (params) => {
                const lawKey = params.value;
                return cd7[lawKey] || 'Law description not found';
            }
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
            width: 47,
            headerClass: 'Hello'
        }))
    ];

    // const rowClassRules = {
       
    // };

    const handleCluster = () => {
        // Add clustering logic here
        console.log('Cluster button clicked');
        const url = 'http://localhost:8000/process-grid';
        if (selectedRows.length !== 0) {
            const requestBody = { selectedRows };
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            })
            .then(response => response.json())
            .then(data => {
                console.log('POST request successful');
                console.log(data);
            })
            .catch(error => {
                console.error('Error making POST request:', error);
            });
        }

    };

    const onSelectionChanged = (event) => {
        selectedRows = event.api.getSelectedRows();
        console.log(selectedRows);
    };

    return (
        <div>
            <div className="row justify-content-center">
                <div style={{ textAlign: 'center', margin: '1vh' }}>
                    <button type="button" className="btn btn-dark" onClick={handleCluster}>Cluster</button>
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="ag-theme-alpine" style={{ height: '92vh', width: '97%'}}>
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
        </div>
    );
};

export default TableComponent;
