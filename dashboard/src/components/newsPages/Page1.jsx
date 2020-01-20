import React, { Component } from 'react';
import WordCloud from '../wordcloud/WordCloud';

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

  fontSizeMapper = word => word.value / 100;
  fontSizeMapper1 = word => word.value / 50;
  
  render() {
    return (
      <div className={`${this.props.styles['pane-container']} ${this.props.styles['variable-pane-container']}`}>
          {/* <div className={this.props.styles['pane']}>
            Bias + Candidate Interactive Chart
          </div> */}
          <div className={`${this.props.styles['word-cloud']} ${this.props.styles['pane']}`}>
            <p className="heading">Trending Words</p>
            <div ref={this.myRef}>
              <WordCloud 
                data={this.props.news.newsWordCloud} 
                fontSizeMapper={(this.props.news.partyClicked) ? this.fontSizeMapper1 : this.fontSizeMapper}
                width={this.state.width}
                height={this.state.height}
              />
            </div>
          </div>
        </div>
    );
  }
}

export default Page1;
