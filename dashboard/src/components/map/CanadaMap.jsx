import React, { Component } from "react"
import MapPath from './mapPath/MapPath';
import styles from './canadaMap.module.scss';
import mapConstants from '../../constants/mapConstants';
import Legend from '../poll/legend/Legend';
import {colorsParty} from '../../styles/d3Colors';
import Gradient from "./gradient/Gradient";

class CanadaMap extends Component {

  renderMap = () => {
    return this.props.map.canadamap.map((path, index) => {
      const mapData = this.props.map.mapData[path.region]
      if(!mapData) {
        return null;
      }
      let value;
      if(this.props.partyClicked === 'LPC') {
        value = mapData.Liberals;
      } else if (this.props.partyClicked === 'CPC') {
        value = mapData.Conservative;
      } else if (this.props.partyClicked === 'NDP') {
        value = mapData.NDP;
      } else {
        value = mapData.Liberals;
        if(mapData.Max === 'Conservative') {
          value = mapData.Conservative;
        } else if (mapData.Max === 'NDP') {
          value = mapData.NDP;
        }
      }
      return (
        <MapPath 
          {...path} 
          key={index} 
          {...this.props.map.mapData[path.region]} 
          regionClicked={this.props.polls.regionClicked}
          regionHovered={this.props.map.regionHovered}
          fill={this.props.getFill(value, mapData)}
          value={value}
          partyClicked={this.props.partyClicked}
        />
      );
    });
  }

  handleClick = (ev) => {
    const region = (mapConstants[ev.target.id] === this.props.polls.regionClicked) ? '': mapConstants[ev.target.id];
    this.props.regionClick(region);
  }

  handleMouseOver = (ev) => {
    const region = mapConstants[ev.target.id];
    if(region) {
      this.props.regionHovered(region);
    }
  }

  handleMouseOut = (ev) => {
    this.props.regionExitHover(mapConstants[ev.target.id])
  }

  render() {
    const legend = (this.props.partyClicked) ? (
      <Gradient
        getGradients={this.props.getGradients}
        gradient1={this.props.gradient1}
        gradient2={this.props.gradient2}
      />
    ): (
      <Legend 
        labels={['CPC', 'LPC', 'NDP']}
        opacity={0.7} 
        colors={colorsParty}
      />
    );
    return (
      <div className="height-100 width-100">
        <div className="height-15 width-100">
          <p className={styles['map-title']}>{this.props.title}</p>
          {legend}
        </div>
        <svg 
          viewBox="0 885 1000 200" 
          width="100%" 
          height="85%" 
          onClick={this.handleClick} 
          onMouseOver={this.handleMouseOver}
          onMouseOut={this.handleMouseOut}
        >
          <defs>
            <filter id="f4" x="0" y="0" width="200%" height="200%">
              <feOffset result="offOut" in="SourceGraphic" dx="20" dy="20" />
              <feColorMatrix result="matrixOut" in="offOut" type="matrix"
              values="0.2 0 0 0 0 0 0.2 0 0 0 0 0 0.2 0 0 0 0 0 1 0" />
              <feGaussianBlur result="blurOut" in="matrixOut" stdDeviation="10" />
              <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
            </filter>
          </defs>
          <g transform="scale(0.9)">
            {this.renderMap()}
          </g>
        </svg>
      </div>
    );    
  }
}

export default CanadaMap;