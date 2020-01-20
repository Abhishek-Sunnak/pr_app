import React, { Component } from 'react';
import Tweet from '../tweets/Tweets';

class Page2 extends Component {
  render() {
    return (
      <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
        <div className={this.props.styles['full-pane']}><Tweet {...this.props} /></div>
      </div>
    );
  }
}

export default Page2;
