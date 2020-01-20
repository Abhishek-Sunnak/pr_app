import React, { Component } from 'react';
import Poll from '../poll/Poll';
import strings from '../../constants/strings';
import TwitterMap from '../twitterMap/TwitterMap';

class TwitterStatic extends Component {
  render() {
    return (
      <div className={this.props.styles['pane-container']}>
        <div className={this.props.styles['static-pane']}>
          <Poll 
            {...this.props}
            labels={[
              strings.POSITIVE, strings.NEGATIVE, strings.NEUTRAL
            ]}
            candidates={this.props.tweets.candidates}
            partyClicked={this.props.tweets.partyClicked}
            title="Sentiment for each Candidate"
          />
        </div>
        <div className={this.props.styles['line']}></div>
        <div className={this.props.styles['static-pane']}>
          <TwitterMap {...this.props} title="Leading Party Across Canadian Provinces" description={strings.POLL_MAP_DESC}/>
        </div>
      </div>
    );
  }
}

export default TwitterStatic;
