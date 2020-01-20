import React, { Component } from 'react';
import Line from '../charts/line/Line';

class Page0 extends Component {

  render() {
    return (
      <div className={this.props.styles['pane-container']} >
        <div className={this.props.styles['pane']} ref={this.myRef}>
          <Line
            labels={this.props.tweets.tweetsSentimentLabels}
            dataset={this.props.tweets.tweetsSentimentDistribution}
            title={this.props.tweets.title}
            yLabel="Avg Sentiment"
            xLabel="Time"
          />
        </div>
        {/* <div className={this.props.styles['line']}></div> */}
        <div className={this.props.styles['pane']}>
          <Line
            labels={this.props.tweets.tweetsNumberLabels}
            dataset={this.props.tweets.tweetsCountDistribution}
            title={this.props.tweets.title2}
            yLabel="Number of Tweets"
            xLabel="Time"
          />
        </div>
      </div>
    );
  }
}

export default Page0;
