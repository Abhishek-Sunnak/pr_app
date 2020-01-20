import React, { Component } from "react";
import styles from './mapPath.module.scss';
import mapConstants from '../../../constants/mapConstants';
import classnames from 'classnames';

class MapPath extends Component {

  render() {
    const isHighlight = (this.props.regionClicked === mapConstants[this.props.id]) || (this.props.regionHovered === mapConstants[this.props.id])
    const pathStyle = classnames({
      [styles['highlight']]: isHighlight,
      [styles['path']]: true,
      [styles['unclicked']]: this.props.regionClicked && this.props.regionClicked !== mapConstants[this.props.id],
      [styles['opacity']]: !this.props.partyClicked
    });

    let text = null;
    if (isHighlight) {
      text = (
        <text x={this.props.x} y={this.props.y} fill="#fff" fontSize = "30">
          {Math.round(this.props.value * 10) / 10}
        </text>
      );
    }
    let filter = '';
    if (isHighlight) {
      filter = 'url(#f4)';
    }
    return (
      <g>
        <path 
          d={this.props.d} 
          name={this.props.name} 
          id={this.props.id} 
          onClick={this.props.handleClick}
          fill={this.props.fill}
          stroke="#fff"
          className={pathStyle}
          filter={filter}
        />
        {text}      
      </g>
      
    );    
  }
}

export default MapPath;