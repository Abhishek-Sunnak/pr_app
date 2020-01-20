import React, { Component } from 'react'; 
import BarChart from '../charts/bar/Bar';
import strings from '../../constants/strings';

class Page0 extends Component {
  render() {
    return (
      <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
          <div className={this.props.styles['pane']}>
            <BarChart 
              stacked={false}
              title={strings.BAR_CHART_1_TITLE}
              labels={this.props.news.newsBarLabels}
              data={this.props.news.newsBarCandidate}
              xLabel={strings.PUBLICATIONS}
              yLabel={strings.NUMBER_OF_ARTICLES}
              barPercentage={(!this.props.news.partyClicked) ? 1 : 0.3 }
            />
          </div>
          <div className={this.props.styles['pane']}>
            <BarChart 
              labels={this.props.news.labels}
              data={this.props.news.stackedData}
              stacked={true}
              title={strings.BAR_CHART_2_TITLE}
              barPercentage={0.3}
              xLabel={strings.PARTIES}
              yLabel={strings.PERECENTAGE_OF_ARTICLES}
            />
          </div>
        </div>
    );
  }
}

export default Page0;
