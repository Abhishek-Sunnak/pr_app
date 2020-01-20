import React, { Component } from 'react';
import {createPie, createArc} from '../../../util/d3';
import {biasColors} from '../../../styles/d3Colors';
import Legend from '../../poll/legend/Legend';
import Arc from './arc/Arc';

class PieChart extends Component {
  
  renderArc = (newData) => (
    newData.map((d, index) => (
      <Arc
        key={index}
        data={d}
        createArc={createArc}
        outerRadius={120}
        innerRadius={0}
        colors={biasColors[index]}
        label={this.props.labels[index]}
        biasClicked={this.props.biasClicked}
        bias={this.props.bias}
      />
    ))
  )
  render() {
    const newData = createPie(this.props.data);
    
    return (
      <div className="width-100 height-100">
        <p className="heading">{this.props.title}</p>
        <div className="width-100 height-10">
          <Legend 
            labels={this.props.labels}
            colors={biasColors} 
          />
        </div>
        <svg width="100%" height="90%">
          <defs>
          <filter id="f3" x="0" y="0" width="200%" height="200%">
            <feOffset result="offOut" in="SourceAlpha" dx="20" dy="20" />
            <feGaussianBlur result="blurOut" in="offOut" stdDeviation="10" />
            <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
          </filter>
          </defs>
          <g transform="translate(350 130)">
            {this.renderArc(newData)}
          </g>
        </svg>
      </div>
      
    );
  }
}

export default PieChart;
