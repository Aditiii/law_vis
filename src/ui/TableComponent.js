import React, { useRef, useState, useEffect } from 'react';
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
    const [displayData, setDisplayData] = useState([]);
    const [tableData, setTableData] = useState([]);
    const gridApiRef = useRef(null);
    const [columnDefs, setColumnDefs] = useState([]);
    const [remainingIds, setRemainingIds] = useState([]);
    const [showAlert, setShowAlert] = useState(false);

    useEffect(()=> {
        const temp = Object.entries(jsonData).map(([law, states]) => {
            return {
                id: law,
                law,
                ...states
            };
        });
        setTableData(temp);
    }, []) 

    useEffect(()=> {
        if(tableData && tableData.length > 0) {
            setDisplayData(tableData);
        }
    }, [tableData]) 

    useEffect(() => {
        
        if(displayData && displayData.length > 0) {
            const cols = Object.keys(displayData[0]).slice(2,-1);
            const temp = [
                {
                    headerName: '',
                    field: 'checkbox',
                    checkboxSelection: true,
                    headerCheckboxSelection: true,
                    width: 35,
                    cellStyle: {marginLeft: 17},
                    pinned: 'left',
                    showDisabledCheckboxes: true
                },
                { 
                    headerName: 'Laws', 
                    field: 'law',
                    width: '300vw', 
                    cellStyle: {textAlign: 'left', marginLeft: 18},
                    pinned: 'left',
                    filter: true,
                    tooltipValueGetter: (params) => {
                        const lawKey = params.value;
                        return cd7[lawKey] || 'Law description not found';
                    }
                },
                    ...cols.map(state => ({
                    
                    headerName: state,
                    field: state,
                    // cellClass: params => {
                    //     return params.value === 1 ? 'green-cell' : '';
                    // },
                    // cellRenderer: params => {
                    //     return params.value === 1 ? <div className="green-cell" style={{width: '100%', height: '100%'}}></div> : '';
                    // },
                    filter: true,
                    width: 47,
                    headerClass: 'Hello'
                }))
            ];
            setColumnDefs(temp);
        
            gridApiRef.current.forEachNode(node => {
                if (node.data.selected) {
                    node.setSelected(true);
                } else {

                }
            });
        }
    }, [displayData])

    const handleCluster = () => {
        if (selectedRows.length < 2) {
            setShowAlert(true);
            setTimeout(() => {
                setShowAlert(false);
            }, 3000);}
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
                const sortedData = JSON.parse(data.sorted_dataframe);
                let rowData = Object.keys(sortedData).map(key => {
                    return {
                        id: key,
                        law: key,
                        ...sortedData[key]
                    };
                });

                rowData.forEach(row => {
                    row.selected = true;
                });

                const remainingRows = tableData.filter((e)=>{
                    return !Object.keys(sortedData).includes(e.id);
                })
                const temp = []
                remainingRows.forEach((entry) => {
                    temp.push(entry.id);
                });

                setRemainingIds(temp);
                rowData = [...rowData, ...remainingRows];
                setDisplayData(rowData);
            })
            .catch(error => {
                console.error('Error making POST request:', error);
            });
        }

    };
    const handleFlood = () => {
        if (selectedRows.length < 2) {
            setShowAlert(true);
            setTimeout(() => {
                setShowAlert(false);
            }, 3000);}
        const url = 'http://localhost:8000/flood-fill-route';
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
                const sortedData = JSON.parse(data.sorted_dataframe);
                let rowData = Object.keys(sortedData).map(key => {
                    return {
                        id: key,
                        law: key,
                        ...sortedData[key]
                    };
                });

                rowData.forEach(row => {
                    row.selected = true;
                });

                const remainingRows = tableData.filter((e)=>{
                    return !Object.keys(sortedData).includes(e.id);
                })
                const temp = []
                remainingRows.forEach((entry) => {
                    temp.push(entry.id);
                });

                setRemainingIds(temp);
                rowData = [...rowData, ...remainingRows];
                setDisplayData(rowData);
            })
            .catch(error => {
                console.error('Error making POST request:', error);
            });
        }

    };

    const handleReset = () => {
        setRemainingIds([]);
        selectedRows = [];
        if (gridApiRef.current) {
            gridApiRef.current.setFilterModel(null);
            // gridApiRef.current.setSortModel([]);
            setDisplayData(tableData);
        }
    }

    const onSelectionChanged = (event) => {
        selectedRows = event.api.getSelectedRows();
    };

    return (
        <div>
            {showAlert && <div className="alert alert-warning" role="alert" >
                {/* style={{marginLeft: '3vh', marginRight: '3vh'}}> */}
                Please select at least 2 rows for clustering!
            </div>}
            <div className="row justify-content-center">
                <div style={{ textAlign: 'center', margin: '1vh'}}>
                    <button type="button" className="btn btn-dark" onClick={handleCluster}>Cluster</button>
                    <button type="button" className="btn btn-dark" onClick={handleFlood}>Flood-fill</button>
                    <button type="button" className="btn btn-dark" onClick={handleReset} style={{ marginLeft: '1vh'}}>Reset</button>
                </div>
               
            </div>
            <div className="row justify-content-center">
                <div className="ag-theme-alpine" style={{ height: '92vh', width: '97%'}}>
                <AgGridReact
                    rowData={displayData}
                    columnDefs={columnDefs}
                    enableFilter={true}
                    rowSelection='multiple'
                    rowMultiSelectWithClick = {true}
                    onSelectionChanged={onSelectionChanged}
                    onGridReady={(params) => {
                        gridApiRef.current = params.api;
                    }}
                    isRowSelectable= {(params)=>{
                        if(remainingIds.includes(params.data.id)) {
                            return false
                        } else {
                            return true
                        }
                    }}
                />
                </div>
            </div>
        </div>
    );
};

export default TableComponent;
