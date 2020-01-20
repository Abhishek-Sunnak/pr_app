import React, { PureComponent } from 'react';
import {Tweet} from 'react-twitter-widgets';
import classnames from 'classnames';
import styles from './tweet.module.scss';

class Tweets extends PureComponent {
  render() {
    return (
      <div className={`margin-auto ${styles['tweets-container']}`}>
        <p className="heading">Top Tweets</p>
        {
          this.props.tweets.tweets.map((tweet, index) => {
            const styleName = classnames({
              [styles['neutral']]: +tweet.sentiment === 0,
              [styles['negative']]: +tweet.sentiment < 0,
              [styles['positive']]: +tweet.sentiment > 0
            });
            return (
              <div key={index} className={styleName}><Tweet tweetId={String(tweet.id)} /></div>
            );
          }
          )
        }
        
      </div>
    );
  }
}

export default Tweets;
