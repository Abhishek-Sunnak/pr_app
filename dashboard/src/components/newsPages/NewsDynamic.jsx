import React, { Component } from 'react';
import Page0 from './Page0';
import Page1 from './Page1';
import Page2 from './Page2';

class NewsDynamic extends Component {
  render() {
    if(this.props.page === 0) {
      return (
        <Page0 {...this.props} />
      );
    } else if (this.props.page === 1) {
      return (
        <Page1 {...this.props} />
      );
    }
    return (
      <Page2 {...this.props} />
    );
  }
}

export default NewsDynamic;
