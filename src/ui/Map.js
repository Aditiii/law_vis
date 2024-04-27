import { ResponsiveHeatMap } from '@nivo/heatmap'
import jsonData from './data.json';
import { useEffect, useState } from 'react';
import Slider from 'rc-slider';

const Map = () => {
    const [convertedData,setConvertedData] = useState([]);
    useEffect(()=>{
        const outputData = [];
        const laws = Object.keys(jsonData[0]).slice(3);

        laws.forEach((law) => {
            const data = jsonData.map((item) => ({
                x: item.Jurisdictions,
                y: item[law]===1?item[law]:0,
                Effective_Date : item['Effective Date'],
                Valid_Through_Date : item['Valid Through Date']
            }));

            outputData.push({
                id: law,
                data: data
            });
        });

        setConvertedData(outputData);
    },[])
    

    return (
        <div style={{ width : '250vw',  overflow: 'scroll', height:'100vh'}}>
            <ResponsiveHeatMap
        data={convertedData}
        margin={{ top: 150, right: 100, bottom: 60, left: 500 }}
        valueFormat=">-.2s"
        label={(obj)=>{
            if(obj.data.y===0)
                return "NO"
            else
                return "YES"
        }}
        tooltip={(obj)=>{
            var str = 'YES'
            if(obj.cell.data.y===0)
                str = 'NO'
            return <h6>
                {obj.cell.id} : {str}
            </h6>
        }}
        axisTop={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: -90,
            legend: '',
            legendOffset: 46
        }}
        colors={{
            type: 'diverging',
            scheme: 'greens',
            divergeAt: 0.5,
            minValue: 0,
            maxValue: 3
        }}
        emptyColor="#ffffff"
        hoverTarget="cell"
        borderRadius={9}
        borderWidth={1}
        borderColor="black"
        isInteractive={false}
        // legends={[
        //     {
        //         anchor: 'bottom',
        //         translateX: 0,
        //         translateY: 30,
        //         length: 400,
        //         thickness: 8,
        //         direction: 'row',
        //         tickPosition: 'after',
        //         tickSize: 3,
        //         tickSpacing: 4,
        //         tickOverlap: false,
        //         tickFormat: '>-.2s',
        //         title: 'Value →',
        //         titleAlign: 'start',
        //         titleOffset: 4
        //     }
        // ]}
    />
        </div>
    )
}

export default Map;