import React, { Component } from 'react';
import WordCloud from '../wordcloud/WordCloud';
import {colorsDonut5ScaleChart, colorsDonutChart} from '../../styles/d3Colors';

class Page1 extends Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();

    this.state = {
      width: 600,
      height: 300
    }
  }

  componentDidMount () {
    this.setState({
      width: this.myRef.current.offsetWidth,
      height: this.myRef.current.offsetHeight - 35
    });
  }

  fill1 = (index) => {
    console.log(index);
    if(this.props.tweets.wordCloudData[index]) {
      return colorsDonutChart[this.props.tweets.wordCloudData[index].sentiment + 1];
    } else {
      return '#000';
    }
  }

  fill2 = (index) => {
    if(this.props.tweets.wordCloudHashtagsData[index]) {
      return colorsDonut5ScaleChart[this.props.tweets.wordCloudHashtagsData[index].sentiment + 2];
    } else {
      return '#000';
    }
  }

  fontSizeMapper = word => word.value * 2
  fontSizeMapper3 = word => word.value * 3
  fontSizeMapper1 = word => word.value / 4
  fontSizeMapper2 = word => word.value / 3


  render() {
    return (
      <div className={this.props.styles['pane-container']} >
        <div className={this.props.styles['pane']} ref={this.myRef}>
          <p className="heading">Trending Words</p>
          <WordCloud 
            data={this.props.tweets.wordCloudData} 
            fontSizeMapper={(this.props.tweets.partyClicked) ? this.fontSizeMapper2 : this.fontSizeMapper1} 
            // fill={this.fill1} 
            width={this.state.width}
            height={this.state.height}
          />
        </div>
        {/* <div className={this.props.styles['line']}></div> */}
        <div className={this.props.styles['pane']}>
          <p className="heading">Trending Hashtags</p>
          <WordCloud 
            data={this.props.tweets.wordCloudHashtagsData} 
            fontSizeMapper={(this.props.tweets.partyClicked) ? this.fontSizeMapper3 : this.fontSizeMapper}
            // fill={this.fill2} 
            width={this.state.width}
            height={this.state.height}
          />
        </div>
      </div>
    );
  }
}

export default Page1;
