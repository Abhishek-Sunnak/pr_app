import React, { Component } from 'react';
import styles from './gradient.module.scss';

class Gradient extends Component {
  render() {
    const gradients = this.props.getGradients()
    const pStyle = {
      background: `linear-gradient(to right, ${gradients.toString()})`
    };
    return (
      <div className={styles['gradient-container']}>
        <span>{this.props.gradient1}</span>
        <div style={pStyle} className={styles['gradient-legend']}></div>
        <span>{this.props.gradient2}</span>
      </div>
      
      
    );
  }
}

export default Gradient;
