import React, { Component } from 'react';
import styles from './legend.module.scss';

class Legend extends Component {
  render() {
    return (
      <div className={`width-100 height-100 ${styles['legend-container']}`}>
        {
          this.props.labels.map((label, index) => (
            <div key={index} className={styles['legend-component']}>
              <div 
                className={styles['legend']} 
                style={{backgroundColor: this.props.colors[index], opacity: this.props.opacity}}
              >
              </div>
              <p>{label}</p>
            </div>
          ))
        }
      </div>
      
    );
  }
}

export default Legend;
