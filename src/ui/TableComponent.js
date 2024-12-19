import React, { useRef, useState, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import goodSam from './datasets/goodSam.json';
import dirDisp from './datasets/dirDisp.json';
import naloxoneOverdosePrev from './datasets/naloxoneOverdosePrev.json';
import sspUpdate2021 from './datasets/sspUpdate2021.json';
import stateJson from './datasets/states.json';
import './tableStyles.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import DateSlider from './DateSlider';

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
    const optionsData = [
        { id: 'goodSam', value: 'goodSam', label: 'Good Samaritan Overdose Prevention Laws' },
        { id: 'directDisp', value: 'directDisp', label: 'Direct Dispensing Stat' },
        { id: 'naloxoneOverdosePrev', value: 'naloxoneOverdosePrev', label: 'Naloxone Overdose Prevention Laws' },
        { id: 'sspUpdate2021', value: 'sspUpdate2021', label: 'SSP Update 2021' },
        // Add more options here
    ];

    const [combinedData, setCombinedData] = useState([]);

    const [selectedRows, setSelectedRows] = useState([]);
    const [displayData, setDisplayData] = useState([]);
    const [tableData, setTableData] = useState([]);
    const gridApiRef = useRef(null);
    const [columnDefs, setColumnDefs] = useState([]);
    const [remainingIds, setRemainingIds] = useState([]);
    const [showAlert, setShowAlert] = useState(false);
    const [selectedClusteringMethod, setSelectedClusteringMethod] = useState('');
    
    const [startCell, setStartCell] = useState(null); // Stores the starting cell for drag selection
    const [endCell, setEndCell] = useState(null); // Stores the ending cell for drag selection
    const [selectedCells, setSelectedCells] = useState([]); // Selected cells range

    // multiple db changes
    const [isPanelOpen, setIsPanelOpen] = React.useState(false);
    const [isFilterPanelOpen, setIsFilterPanelOpen] = React.useState(false);
    const [selectedOptions, setSelectedOptions] = React.useState(['goodSam']);

    //date slider
    const [selectedDate, setSelectedDate] = useState(new Date('2021-08-01').getTime());

    const processData = (jsonData, date, source) => {
        return Object.entries(jsonData).map(([law, states]) => {
          const processedStates = {};
          Object.entries(states).forEach(([state, data]) => {
            const applicableStatus = data.find(item => 
              new Date(item.from) <= date && (!item.to || new Date(item.to) > date)
            );
            processedStates[state] = applicableStatus ? applicableStatus.status : data[data.length - 1].status;
          });
          return { id: law, law, ...processedStates,  datasetSource: source };
        });
    };

    useEffect(() => {
        if(displayData && displayData.length > 0) {            
            let cols = [];
            const excludedKeys = ['selected', 'law', 'id']; // Array of keys to exclude

            cols = Object.keys(displayData[0]).filter(key => !excludedKeys.includes(key));

            const temp = [
                {
                    headerName: '',
                    field: 'checkbox',
                    checkboxSelection: true,
                    headerCheckboxSelection: true,
                    width: 50,
                    minWidth: 50,
                    maxWidth: 50,
                    pinned: 'left',
                    lockPosition: true,
                    suppressMovable: true,
                    cellStyle: { display: 'flex', justifyContent: 'center', alignItems: 'center' },
                    headerClass: 'ag-checkbox-header custom-checkbox-header'
                },
                { 
                    headerName: 'Laws', 
                    field: 'law',
                    width: '45vw', 
                    cellStyle: {textAlign: 'left', marginLeft: 10},
                    pinned: 'left',
                    filter: true,
                    tooltipValueGetter: (params) => {
                        const lawKey = params.value;
                        return cd7[lawKey];
                    },
                    headerClass: 'Laws'
                },
                { 
                    headerName: 'Source', 
                    field: 'datasetSource',
                    width: '45vw', 
                    cellStyle: {textAlign: 'left', marginLeft: 10},
                    pinned: 'left',
                    filter: true
                },
                    ...cols.map(state => ({
                    headerName: state,
                    field: state,
                    headerTooltip: stateJson[state],
                    cellStyle: params => {  
                        const isSelected = selectedCells.some(cell => 
                          cell.rowIndex === params.rowIndex && cell.colId === params.column.getColId()
                        );
                        // if (isSelected) {
                        //     console.log("true");
                        // }
                        if (isSelected) {
                            if (params.value === 1) {
                                return { backgroundColor: 'black' };
                            }
                            else{
                                return { backgroundColor: 'grey'};
                            }
                            // White cells remain white when selected
                            //return {};
                        }
                        if (params.value === 1) {
                            return { backgroundColor: `rgba(255, 0, 0, 0.5)` };
                          }
                        else{
                            return {backgroundColor:'white'};
                        }
                    },
                    cellRenderer: params => {
                        return params.value === 1 ? <div className="selected-cell" style={{width: '100%', height: '100%'}}></div> : '';
                    },
                    filter: true,
                    width:18,
                    headerClass: 'Hello',
                    // cellClass: getCellClass, // Add the cellClass here
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
    }, [displayData, selectedCells])

    useEffect(() => {
        if (combinedData && combinedData.length > 0) {
          let cols = [];
          const excludedKeys = ['selected', 'law', 'id'];
          cols = Object.keys(combinedData[0]).filter(key => !excludedKeys.includes(key));
          
          const temp = [
            // ... existing columns ...
            {
              headerName: 'Dataset Source',
              field: 'datasetSource',
              width: 150,
              filter: true,
              headerClass: 'DatasetSource'
            },
            // ... other columns ...
          ];
          
          setColumnDefs(temp);
        }
    }, [combinedData]);
    
    useEffect(() => {
        const initialDate = new Date('2025-01-01');
        // const initialData = Object.entries(goodSam).map(([law, states]) => ({
        //   ...states,
        //   id: law,
        //   law,
        //   datasetSource: 'Good Samaritan Overdose Prevention Laws'
        // }));
        const idata = processData(goodSam, initialDate, 'Good Samaritan Overdose Prevention Laws')
        setTableData(idata);
        setDisplayData(idata);
        setSelectedDate(initialDate.getTime());
      }, []);
    
      const getDataForOption = (option) => {
        switch(option) {
          case 'goodSam':
            return goodSam; // Assuming jsonData is your Good Samaritan data
          case 'directDisp':
            return dirDisp; // Other data sources
          case 'naloxoneOverdosePrev':
            return naloxoneOverdosePrev;
          case 'sspUpdate2021':
            return sspUpdate2021;
          default:
            return {};
        }
      };
      
    const handleOptionChange = (e) => {
        const value = e.target.value;
        setSelectedOptions(prev => {
          const newSelection = prev.includes(value) ? prev.filter(opt => opt !== value) : [...prev, value];
          if (!prev.includes(value)) {
            let newData;
            let source;
            switch (value) {
              case 'goodSam':
                source = 'Good Samaritan Overdose Prevention Laws';
                newData = processData(goodSam, selectedDate, source);
                break;
              case 'directDisp':
                source = 'Direct Dispensing Stat';
                newData = processData(dirDisp, selectedDate, source);
                break;
              case 'naloxoneOverdosePrev':
                source = 'Naloxone Overdose Prevention Laws';
                newData = processData(naloxoneOverdosePrev, selectedDate, source);
                break;
              case 'sspUpdate2021':
                source = 'SSP Update 2021';
                newData = processData(sspUpdate2021, selectedDate, source);
                break;
              default:
                break;
            }
            setDisplayData(prevData => [...prevData, ...newData]);
          } else {
            setDisplayData(prevData => prevData.filter(item => item.datasetSource !== optionsData.find(opt => opt.value === value).label));
          }
          return newSelection;
        });
    };

    const handleDateChange = (newDate) => {
        setSelectedDate(newDate);
        const updatedData = selectedOptions.flatMap(option => {
          const sourceData = getDataForOption(option);
          return processData(sourceData, newDate, option+' data');
        });
        
        setDisplayData(updatedData);
    };
    
    const handleCluster = () => {
        if (selectedRows.length < 2) {
            setShowAlert(true);
            setTimeout(() => {
                setShowAlert(false);
            }, 3000);}
        const url = 'http://localhost:8000/process-grid';
        if (selectedRows.length !== 0) {
            const requestBody = { 
                selectedRows,
                cluster: selectedClusteringMethod 
            };
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
        setSelectedRows([]);
        setSelectedCells([]);
        setSelectedOptions(['goodSam']);
        setSelectedClusteringMethod('');
        setSelectedDate([new Date('2021-08-01').getTime()])
        if (gridApiRef.current) {
            gridApiRef.current.setFilterModel(null);
            // gridApiRef.current.setSortModel([]);
            setDisplayData(tableData);
        }
    }

    const onSelectionChanged = (event) => {
        console.log('In onSelectionChanged');
        setSelectedRows(event.api.getSelectedRows());
        // Update selectedCells state based on your selection logic
        const newSelectedCells = [];
        selectedRows.forEach(row => {
            const rowIndex = row.rowIndex; // Assuming rowIndex is part of your data
            Object.keys(row).forEach(key => {
                newSelectedCells.push({ rowIndex, colId: key });
            });
        });
        setSelectedCells(newSelectedCells); // Update your selectedCells state

        // Refresh cells to apply new styles based on selection
        // if (gridApiRef.current) {
        //     const checkboxColumn = gridApiRef.current.getColumnDef('checkbox');
        //     if (checkboxColumn) {
        //       gridApiRef.current.refreshCells({
        //         columns: [checkboxColumn],
        //         force: true
        //       });
        //     }
        //   }
    };

    const handleCellClick = (params) => {
        const { rowIndex, colDef } = params;
        const colId = colDef.field;
        // console.log("handleCellClick");
        const isAlreadySelected = selectedCells.some(
            cell => cell.rowIndex === rowIndex && cell.colId === colId
          );
          if (isAlreadySelected) {
            // If the cell is already selected, remove it from the selection
            setSelectedCells(prevSelectedCells => 
              prevSelectedCells.filter(cell => !(cell.rowIndex === rowIndex && cell.colId === colId))
            );
          } else {
            // If the cell is not selected, start a new selection
            setStartCell({ rowIndex, colId });
            setEndCell(null);
            setSelectedCells([{ rowIndex, colId }]);
          }
          if (gridApiRef.current) {
            gridApiRef.current.refreshCells({ force: true });
          }
    };

    const handleCellMouseOver = (params) => {
        // console.log("handleCellMouseOver");
        if (!startCell) return; // Only drag-select if a starting cell has been clicked

        const { rowIndex, colDef } = params;
        const colId = colDef.field;

        // Set the end cell and select all cells within the rectangle
        setEndCell({ rowIndex, colId });
        const newSelectedCells = calculateSelectedCells(startCell, { rowIndex, colId });
        setSelectedCells(prevSelectedCells => {
            // Merge the new selection with existing selections
            return [...new Set([...prevSelectedCells, ...newSelectedCells])];
          });
        
          if (gridApiRef.current) {
            gridApiRef.current.refreshCells({ force: true });
          }
    };

    // Calculate the range of selected cells between startCell and endCell
    const calculateSelectedCells = (start, end) => {
        const rows = [start.rowIndex, end.rowIndex].sort((a, b) => a - b); // Min and max row
        const cols = [start.colId, end.colId]; // Get column names between start and end

        const colIndexes = columnDefs.map((col, index) => ({
            colId: col.field,
            index
        }));

        // Get start and end column indexes
        const startColIndex = colIndexes.findIndex(col => col.colId === start.colId);
        const endColIndex = colIndexes.findIndex(col => col.colId === end.colId);

        const colsInRange = colIndexes
            .slice(Math.min(startColIndex, endColIndex), Math.max(startColIndex, endColIndex) + 1)
            .map(col => col.colId);

        // Build selected cells range
        const selectedCells = [];
        for (let row = rows[0]; row <= rows[1]; row++) {
            colsInRange.forEach(col => {
                selectedCells.push({ rowIndex: row, colId: col });
            });
        }
        //console.log(selectedCells);
        return selectedCells;
    };

    // Handle mouse up to finish the selection
    const handleMouseUp = () => {
        setStartCell(null); // Reset start cell after selection is finished
        setEndCell(null);   // Reset end cell

        // Refresh the cells to apply new styles
        if (gridApiRef.current) {
            gridApiRef.current.refreshCells({ force: true });
        }
    };

    useEffect(() => {
        document.addEventListener('mouseup', handleMouseUp);
        return () => {
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, []);

    return (
<div className="container-fluid" style={{marginTop: '10px'}}>
  <div className="row align-items-center mb-3">
    <div className="col-auto">
      <button className="btn btn-light" type="button" onClick={() => setIsPanelOpen(!isPanelOpen)}>
        <i className="bi bi-list" style={{ fontSize: '1.5rem' }}></i>
      </button>
    </div>
    <div className="col">
      <select className="form-select" aria-label="Clustering Options" onChange={(e) => setSelectedClusteringMethod(e.target.value)} value={selectedClusteringMethod}>
        <option value="">Select Clustering Method</option>
        <option value="rearrangement">Rearrangement</option>
        <option value="agglomerative_clustering">Agglomerative Clustering</option>
        <option value="kmeans_clustering">KMeans Clustering</option>
        <option value="spectral_coclustering">Spectral Co-clustering</option>
        <option value="spectral_biclustering">Spectral Bi-clustering</option>
        <option value="mds">MDS + Rearrangement</option>
      </select>
    </div>
    <div className="col-auto">
      <button type="button" className="btn btn-dark me-2" onClick={handleCluster}>Cluster</button>
      <button type="button" className="btn btn-dark me-2" onClick={handleReset}>Reset</button>
      <button className="btn btn-light" type="button" onClick={() => setIsFilterPanelOpen(!isFilterPanelOpen)}>
        <i className="bi bi-funnel" style={{ fontSize: '1.5rem' }}></i>
      </button>
    </div>
  </div>
  
  <div className="row">
    {isPanelOpen && (
      <div className="col-auto border p-2" style={{ minWidth: '250px', maxWidth: '300px', marginLeft: '10px'}}>
        <h6>Datasets</h6>
        <div className="dataset-options">
          {optionsData.map((option) => (
            <div key={option.id} className="form-check mb-2">
              <input
                className="form-check-input"
                type="checkbox"
                value={option.value}
                id={option.id}
                onChange={handleOptionChange}
                checked={selectedOptions.includes(option.value)}
              />
              <label className="form-check-label" htmlFor={option.id}>
                {option.label}
              </label>
            </div>
          ))}
        </div>
      </div>
    )}
    
    <div className={`col ${isPanelOpen ? 'ps-3' : ''} ${isFilterPanelOpen ? 'pe-3' : ''}`}>
      {showAlert && <div className="alert alert-warning" role="alert">Please select at least 2 rows for clustering!</div>}
      <div className="ag-theme-alpine" style={{ height: '92vh', width: '100%' }}>
        <AgGridReact
          rowData={displayData}
          columnDefs={columnDefs}
          enableFilter={true}
          rowSelection="multiple"
          rowMultiSelectWithClick={true}
          suppressRowClickSelection={true}
          onSelectionChanged={onSelectionChanged}
          enableBrowserTooltips={true}
          onCellMouseDown={handleCellClick}
          onCellMouseOver={handleCellMouseOver}
          onMouseUp={handleMouseUp}
          onGridReady={(params) => {
            gridApiRef.current = params.api;
          }}
          isRowSelectable={(params) => !remainingIds.includes(params.data.id)}
        />
      </div>
    </div>

    {isFilterPanelOpen && (
      <div className="col-auto border p-2" style={{ minWidth: '250px', maxWidth: '300px', marginRight: '10px' }}>
        <h6>Date Filter</h6>
        <DateSlider 
            minDate={new Date('2000-01-01').getTime()}
            maxDate={new Date('2025-01-01').getTime()}
            onDateChange={handleDateChange}
            value={selectedDate}
        />
        {/* <div className="filter-options">
          {filterOptions.map((filter) => (
            <div key={filter.id} className="form-check mb-2">
              <input
                className="form-check-input"
                type="checkbox"
                value={filter.value}
                id={filter.id}
                // onChange={}
                // checked={selectedFilters.includes(filter.value)}
              />
              <label className="form-check-label" htmlFor={filter.id}>
                {filter.label}
              </label>
            </div>
          ))}
        </div> */}
      </div>
    )}
  </div>
</div>
  );
};

export default TableComponent;