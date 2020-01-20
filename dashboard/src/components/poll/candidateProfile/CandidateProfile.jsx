import React, { Component } from 'react';
import classnames from 'classnames';
import Donut from '../../charts/donut/Donut';
import styles from './candidateProfile.module.scss';
import partyConstants from '../../../constants/partyConstants';

class CandidateProfile extends Component {
  handleClick = () => {
    this.props.candidateClicked(partyConstants[this.props.candidate], this.props.partyClicked);
  }
  renderLabels = () => {
    return this.props.data.map((item, index) => {
      return (
        <p className={styles['candidate-poll-ratings']} key={index}>
          <span>{this.props.labels[index]}: </span>
          {Math.round(item)}%
        </p>
      )
    });
  }
  render() {
    const candidateStyles = classnames({
      'width-100': true,
      'height-100': true,
      [styles['candidate-container']]: true,
      [styles['clicked']]: this.props.partyClicked === partyConstants[this.props.candidate],
      [styles['unclicked']]: this.props.partyClicked !== partyConstants[this.props.candidate]
    });
    return (
      <div 
        className={candidateStyles}
        onClick={this.handleClick}
      >
        <Donut
          data={this.props.data}
          colors={this.props.colors}
          labels={this.props.labels}
        />
        <img 
          src={this.props.image}
          className={styles['candidate-image']}
          alt={this.props.candidate}
        />
        <p className={styles['candidate-name']}>{this.props.candidate}</p>
        <p className={styles['candidate-party']}>({this.props.party})</p>
        {this.renderLabels()}
      </div>
    );
  }
}

export default CandidateProfile;
