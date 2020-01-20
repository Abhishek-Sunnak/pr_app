import React, { Component } from 'react';

class Arc extends Component {
  constructor(props) {
    super(props);
    this.state = {isHovered: false};
  }

  onMouseOut = () => {
    this.setState({isHovered: false});
  }

  onMouseOver = () => {
    this.setState({isHovered: true});
  }


  onClick = () => {
    this.props.biasClicked(this.props.label);
  }

  render() {
    let isHighlight = false;
    if(this.props.bias === this.props.label) {
      isHighlight = true;
    }
    let outerRadius = this.props.outerRadius;
    if(this.state.isHovered || isHighlight) {
      outerRadius *= 1.05;
    }
    const arc = this.props.createArc(this.props.innerRadius, outerRadius);
    let filter = '';
    if (this.state.isHovered || isHighlight) {
      filter = 'url(#f3)';
    }
    return (
      <g className="arc" onMouseOut={this.onMouseOut} onMouseOver={this.onMouseOver} onClick={this.onClick}>
        <path 
          className="arc"
          d={arc(this.props.data)} 
          fill={this.props.colors} 
          filter={filter}
        />
        <text transform={`translate(${arc.centroid(this.props.data)})`}
          dy=".35em"
          textAnchor="middle"
          fill="white"
        >
          {this.props.data.value}%
        </text>
      </g>
    );
  }
}

export default Arc;