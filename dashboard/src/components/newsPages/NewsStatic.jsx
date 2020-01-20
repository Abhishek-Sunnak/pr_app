import React, { Component } from 'react';
import Poll from '../poll/Poll';
import PieChart from '../charts/pie/Pie';
import strings from '../../constants/strings';

class NewsStatic extends Component {
  render() {
    return (
      <div className={this.props.styles['pane-container']}>
        <div className={this.props.styles['static-pane']}>
          <Poll 
              {...this.props}
              labels={[
                strings.POSITIVE, strings.NEGATIVE, strings.NEUTRAL
              ]}
              candidates={this.props.news.candidateData}
              partyClicked={this.props.news.partyClicked}
              title={strings['CANDIDATE_NEWS_TITLE']}
            />
        </div>
        <div className={this.props.styles['static-pane']}>
          <PieChart
            title={strings['BIAS_PIE_TITLE']}
            labels={this.props.news.biasPieLabels}
            data={this.props.news.biasPie}
            biasClicked={this.props.biasClicked}
            bias={this.props.news.biasClicked}
          />
        </div>
      </div>
    );
  }
}

export default NewsStatic;
