import React, { Component } from 'react';
import {Doughnut} from 'react-chartjs-2';
import {hoverBorderColor} from '../../../styles/d3Colors';

class Donut extends Component {
    
  render() {
    const data = {
      labels: this.props.labels,
      datasets: [{
        data: this.props.data,
        backgroundColor: this.props.colors,
        hoverBackgroundColor: this.props.colors,
        hoverBorderColor: hoverBorderColor
      }]
    };
    return (
      <Doughnut data={data} legend={{display: false}} 
      options={{
        cutoutPercentage: 80,
        tooltips: {
          callbacks: {
            label: (tooltipItem, data) => this.props.labels[tooltipItem.index] + ': ' + this.props.data[tooltipItem.index] + '%'
          }
        }
      }} />
    );
  }
}

export default Donut;
