import React, { Component } from 'react';
import CandidateProfile from './candidateProfile/CandidateProfile';
import styles from './poll.module.scss';
import {colorsDonutChart} from '../../styles/d3Colors';
import {getDonutData} from '../../util/poll';
import Legend from './legend/Legend';

class Poll extends Component {

  renderPollIcon = () => {
    return this.props.candidates.map((party, index) => {
      const data = getDonutData(
        party.positive, 
        party.negative, 
        party.neutral
      );
      return (
        <CandidateProfile
          data={data}
          colors={colorsDonutChart}
          labels={this.props.labels}
          candidate={party.candidate}
          party={party.party}
          image={party.image}
          key={index}
          candidateClicked={this.props.candidateClicked}
          partyClicked={this.props.partyClicked}
        />
      );
    })
  }

  render() {
    return (
      <div className="width-100 height-100">
        <p className="heading">{this.props.title}</p>
        <div className={styles['legends']}>
          <Legend 
            labels={this.props.labels} 
            colors={colorsDonutChart}
            opacity={1}
          />
        </div>
        <div className={styles['candidates']}>{this.renderPollIcon()}</div>
        
      </div>
      
    );
  }
}

export default Poll;
