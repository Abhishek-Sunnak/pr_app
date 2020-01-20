import React, { Component } from 'react';
import Poll from '../poll/Poll';
import strings from '../../constants/strings';
import CanadaMap from '../map/CanadaMap';
import {ndpColor, cpcColor, lpcColor} from '../../styles/d3Colors';

class PollStaticPage extends Component {
  fill = (value, baseColor) => {
    const rounded = Math.round( value / 10 ) / 10;
    const rgb = this.hexToRgb(baseColor)
    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${rounded})`;
  };

  getGradients = () => {
    const gradient1 = '#fff';
    let gradient2 = ndpColor;
    if (this.props.polls.partyClicked === 'LPC') {
      gradient2 = lpcColor;
    } else if (this.props.polls.partyClicked === 'CPC') {
      gradient2 = cpcColor;
    }

    return [gradient1, gradient2];
  }

  getFill = (value, mapData) => {
    let fill;
    if (this.props.polls.partyClicked === 'LPC') {
      fill = this.fill(value, lpcColor);
    } else if (this.props.polls.partyClicked === 'CPC') {
      fill = this.fill(value, cpcColor);
    } else if (this.props.polls.partyClicked === 'NDP') {
      fill = this.fill(value, ndpColor);
    } else {
      fill = lpcColor;
      if(mapData.Max === 'Conservative') {
        fill = cpcColor;
      } else if (mapData.Max === 'NDP') {
        fill = ndpColor;
      }
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

  render() {
    return (
      <div className={this.props.styles['pane-container']}>
        <div className={this.props.styles['static-pane']}>
          <Poll 
            {...this.props}
            labels={[
              strings.APPROVAL, strings.DISAPPROVAL, strings.NOT_DECIDED
            ]}
            candidates={this.props.polls.partyDetails}
            partyClicked={this.props.polls.partyClicked}
          title="Approval Ratings for each Candidate"
          />
        </div>
        <div className={this.props.styles['static-pane']}>
          <CanadaMap 
            {...this.props} 
            title="Leading Party Across Canadian Provinces" 
            description={strings.POLL_MAP_DESC} 
            partyClicked={this.props.polls.partyClicked} 
            fill={this.fill}
            getFill={this.getFill}
            getGradients={this.getGradients}
            gradient1="Disapprove"
            gradient2="Approve"
          />
        </div>
      </div>
    );
  }
}

export default PollStaticPage;
