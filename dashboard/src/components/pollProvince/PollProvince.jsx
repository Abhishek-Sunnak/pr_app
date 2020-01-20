import React, { Component } from 'react';
import Line from '../charts/line/Line';
import strings from '../../constants/strings';

class PollProvince extends Component {
  render() {
    return (
      <div className="width-90 height-100 margin-auto">
        <Line 
          labels={this.props.polls.provinceLineChartLabels}
          dataset={this.props.polls.provinceLineChart}
          title={this.props.polls.title2}
          yLabel={strings.PROVINCIAL_POLL_Y_AXIS}
          xLabel={strings.PROVINCIAL_POLL_X_AXIS}
        />
      </div>
    );
  }
}

export default PollProvince;
