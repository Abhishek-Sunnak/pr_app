import React, { Component } from 'react';
import classnames from 'classnames';
import CanadaMap from '../map/CanadaMap';
import strings from '../../constants/strings';
import styles from './twitterMap.module.scss';
import {ndpColor, cpcColor, lpcColor, disapprovalColor, approvalColor, dontknowColor} from '../../styles/d3Colors';

class TwitterMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tab: 'Mentions'
    }
  }

  fill = (value, baseColor) => {
    const slope = 0.5 / (this.props.map.max - this.props.map.min);
    const intercept = 0.8 - (slope * this.props.map.max);
    const opacity = (slope * value) + intercept;
    const rounded = Math.round( opacity * 10 ) / 10;
    const rgb = this.hexToRgb(baseColor)
    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${rounded})`;
  };

  getGradientsMentions = () => {
    const gradient1 = '#fff';
    let gradient2 = ndpColor;
    if (this.props.tweets.partyClicked === 'LPC') {
      gradient2 = lpcColor;
    } else if (this.props.tweets.partyClicked === 'CPC') {
      gradient2 = cpcColor;
    }

    return [gradient1, gradient2];
  }

  getGradientsTweets = () => {
    return [disapprovalColor, '#fff', approvalColor];
  }

  fillTweets = (value) => {
    let fill;
    if(value < 0) {
      const opacity = (value / this.props.map.min);
      const rounded = Math.round( opacity * 10 ) / 10;
      const rgb = this.hexToRgb(disapprovalColor);
      fill = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${rounded})`;
    } else if(value > 0) {
      const opacity = (value / this.props.map.max);
      const rounded = Math.round( opacity * 10 ) / 10;
      const rgb = this.hexToRgb(approvalColor)
      fill = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${rounded})`;
    } else {
      fill = dontknowColor;
    }
    return fill;
  }

  hexToRgb = (hex) => {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
  }

  getFill = (value, mapData) => {
    let fill;
  
    if(this.state.tab === 'Mentions') {
      if (this.props.tweets.partyClicked === 'LPC') {
        fill = this.fill(value, lpcColor);
      } else if (this.props.tweets.partyClicked === 'CPC') {
        fill = this.fill(value, cpcColor);
      } else if (this.props.tweets.partyClicked === 'NDP') {
        fill = this.fill(value, ndpColor);
      } else {
        fill = lpcColor;
        if(mapData.Max === 'Conservative') {
          fill = cpcColor;
        } else if (mapData.Max === 'NDP') {
          fill = ndpColor;
        }
      }
    } else {
      if (this.props.tweets.partyClicked) {
        fill = this.fillTweets(value);
      } else {
        fill = lpcColor;
        if(mapData.Max === 'Conservative') {
          fill = cpcColor;
        } else if (mapData.Max === 'NDP') {
          fill = ndpColor;
        }
      }
    }
    return fill;
  }

  onClickMentions = () => {
    if(this.state.tab !== 'Mentions') {
      this.setState({
        tab: 'Mentions'
      });
      this.props.getTweetsMentionsData();
    }
  }

  onClickSentiment = () => {
    if(this.state.tab !== 'Sentiment') {
      this.setState({
        tab: 'Sentiment'
      });
      this.props.getTweetsSentimentData();
    }
  }

  render() {
    const mentionsStyles = classnames({
      [styles['tabs']]: true,
      [styles['selected']]: this.state.tab === 'Mentions'
    });

    const sentimentStyles = classnames({
      [styles['tabs']]: true,
      [styles['selected']]: this.state.tab === 'Sentiment'
    });
    return (
      <div className="width-100 height-100">
        <div className={styles['twitter-map-container']}>
          <CanadaMap 
            {...this.props} 
            title="Leading Party Across Canadian Provinces" 
            description={strings.POLL_MAP_DESC}
            getFill={this.getFill}
            partyClicked={this.props.tweets.partyClicked}
            getGradients={(this.state.tab === 'Mentions') ? this.getGradientsMentions : this.getGradientsTweets}
            gradient1={(this.state.tab === 'Mentions') ? 'Low' : 'Negative'}
            gradient2={(this.state.tab === 'Mentions') ? 'High' : 'Positive'}
          />
        </div>
        <div className={styles['tabs-container']}>
          <div className={mentionsStyles} onClick={this.onClickMentions}>Mentions</div>
          <div className={sentimentStyles} onClick={this.onClickSentiment}>Sentiment</div>
        </div>
      </div>
    );
  }
}

export default TwitterMap;
