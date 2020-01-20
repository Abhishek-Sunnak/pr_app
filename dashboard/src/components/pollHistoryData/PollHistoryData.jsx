import React, { Component } from 'react';
import styles from './pollHistoryData.module.scss';
import Line from '../charts/line/Line';
import strings from '../../constants/strings';

class PollHistoryData extends Component {
  render() {
    return (
      <div className={styles['poll-history-container']}>
        <Line 
          labels={this.props.polls.labels}
          dataset={this.props.polls.dataset}
          title={this.props.polls.title}
          yLabel={strings.HISTORICAL_POLL_Y_AXIS}
          xLabel={strings.HISTORICAL_POLL_X_AXIS}
        />
      </div>
    );
  }
}

export default PollHistoryData;
