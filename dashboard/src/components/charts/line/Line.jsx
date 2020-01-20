import React, { PureComponent } from 'react';
import {Line} from 'react-chartjs-2';
import {legendColor, chartTitleColor, gridColor, gridFontColor} from '../../../styles/d3Colors';

class LineChart extends PureComponent {
  render() {
    const data = {
      labels: this.props.labels,
      datasets: this.props.dataset
    };
    return (
      <Line 
        data={data} 
        redraw
        legend={{
          fontColor: legendColor,
          // onClick: (e) => e.stopPropagation()
        }}
        options={{ 
          maintainAspectRatio: false,
          responsive: true, 
          title: {
            display: true,
            text: this.props.title,
            fontColor: chartTitleColor,
            fontFamily: 'Lato',
            fontSize: 16
          },
          elements: {
            line: {
              tension: 0 // disables bezier curves
            }
          },
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: this.props.yLabel,
                fontColor: legendColor,
                fontFamily: 'Lato',
                fontSize: 14
              },
              gridLines: {
                color: gridColor,
                lineWidth: 1,
              },
              ticks: {
                fontFamily: 'Lato',
                fontSize: 12,
                fontColor: gridFontColor,
                beginAtZero: true
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: this.props.xLabel,
                fontColor: legendColor,
                fontFamily: 'Lato',
                fontSize: 14
              },
              gridLines: {
                color: gridColor,
                lineWidth: 1
              },
              ticks: {
                fontFamily: 'Lato',
                fontSize: 12,
                fontColor: gridFontColor
              },
            }],
          }
        }}
      /> 
    );
  }
}

export default LineChart;
