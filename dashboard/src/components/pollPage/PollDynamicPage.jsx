import React, { Component } from 'react';
import PollHistoryData from '../pollHistoryData/PollHistoryData';
import PollProvince from '../pollProvince/PollProvince';
import Tweet from '../tweets/Tweets';
import News from '../news/News';

class PollDynamicPage extends Component {
  render() {
    if(this.props.page === 0) {
      return (
        <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
          <div className={this.props.styles['pane']}><PollHistoryData {...this.props} /></div>
          <div className={this.props.styles['pane']}><PollProvince {...this.props} /></div>
        </div>
      );
    } else if (this.props.page === 1) {
      return (
        <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
          <div className={this.props.styles['full-pane']}><Tweet {...this.props} /></div>
        </div>
      );
    }
    return (
      <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
        <div className={this.props.styles['full-pane']}><News {...this.props} /></div>
      </div>
    );
  }
}

export default PollDynamicPage;
