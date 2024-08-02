function createDoughnut(chartID, data) {
    chartElement = document.getElementById(chartID)
    let chart = echarts.init(chartElement);
    new ResizeObserver(() => chart.resize()).observe(chartElement);
    
    let option = {
        tooltip: {
            trigger: 'item',
            formatter: "<b>{a}</b> <ul><li>{b}</li><li>Worth: ${c}</li></ul>"
        },
        legend: {
            bottom: '0%',
            left: 'center'
        },
        series: [
            {
                name: 'Stock',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false,
                },
                data: data
            }
        ]
    };

    chart.setOption(option);
}


function createLinechart(chartID, data, title) {
    chartElement = document.getElementById(chartID)
    let chart = echarts.init(chartElement);
    new ResizeObserver(() => chart.resize()).observe(chartElement);
    
    let minValue = Math.round(Math.min(...data) - 75)
    let maxValue = Math.round(Math.max(...data) + 75)

    let date = Date.now();
    let oneDay = 24 * 3600 * 1000;
    let chartData = []

    for (let i = 0; i < data.length; i++) {
        chartData.push([date, data[i].toFixed(2)]);
        date += oneDay
    }

    option = {
        tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            },
        },
        title: {
            left: 'center',
            text: title
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'time',
            boundaryGap: false
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            min: minValue,
            max: maxValue
        },
        dataZoom: [
        {
            type: 'inside',
            start: 0,
            end: 100,
            filterMode: 'none'
        },
        {
            start: 0,
            end: 100
        }
        ],
        series: [
        {
            name: 'Price',
            type: 'line',
            smooth: false,
            symbol: 'none',
            areaStyle: {},
            data: chartData
        }
        ]
    };


    chart.setOption(option);
}