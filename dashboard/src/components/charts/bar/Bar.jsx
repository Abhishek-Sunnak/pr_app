import React, { Component } from 'react';
import {Bar} from 'react-chartjs-2';
import {legendColor, chartTitleColor, gridColor, gridFontColor} from '../../../styles/d3Colors';

class BarChart extends Component {
    
  render() {
    const options = {
      maintainAspectRatio: false,
      responsive: true, 
      title: {
        display: true,
        text: this.props.title,
        fontColor: chartTitleColor,
        fontFamily: 'Lato',
        fontSize: 16
      },
      // scales: {
      //   yAxes: [{
      //     ticks: {
      //       beginAtZero: true,
      //     },
      //     stacked: this.props.stacked
      //   }],
      //   xAxes: [{
      //     stacked: this.props.stacked
      //   }]
      // }
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
            fontColor: gridFontColor
          },
          stacked: this.props.stacked
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: this.props.xLabel,
            fontColor: legendColor,
            fontFamily: 'Lato',
            fontSize: 14
          },
          stacked: this.props.stacked,
          gridLines: {
            color: gridColor,
            lineWidth: 1
          },
          barPercentage: this.props.barPercentage,
          ticks: {
            fontFamily: 'Lato',
            fontSize: 12,
            fontColor: gridFontColor
          },
        }]
      }
    };

    const data = {
      labels: this.props.labels,
      datasets: this.props.data
    };

    return (
      <Bar data={data} options={options} />
    );
  }
}

export default BarChart;
