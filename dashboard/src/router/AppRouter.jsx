import React from 'react';
import {BrowserRouter, Route} from 'react-router-dom';
import PollContainer from '../containers/PollContainer'
import TwitterContainer from '../containers/TwitterContainer'
import NewsContainer from '../containers/NewsContainer';

/**
 * This component contains all the routing details.
 */
class AppRouter extends React.Component {
  /**
   * @return {ReactComponent}
   */
  render() {
    return (
      <BrowserRouter>
        <div>
          <Route exact path="/" component={PollContainer} />
          <Route exact path="/twitter" component={TwitterContainer} />
          <Route exact path="/news" component={NewsContainer} />
        </div>
      </BrowserRouter>
    );
  }
}

export default AppRouter;
