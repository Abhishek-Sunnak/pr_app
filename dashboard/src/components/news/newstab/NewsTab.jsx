import React, { PureComponent } from 'react';
import classnames from 'classnames';
import styles from './newstab.module.scss';

class NewsTab extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      more: false
    };
  }

  onClick = () => {
    this.setState({
      more: !this.state.more
    });
  }

  render() {
    const summary = (this.state.more) ? this.props.newsArticle.Summary : this.props.newsArticle.Description;

    const readMore = (!this.state.more) ? 
      <span onClick={this.onClick}>more</span> 
      : <span onClick={this.onClick}> less</span>;
    
    const clickHere = (this.state.more) ? <a className={styles['link']} href={this.props.newsArticle.URL} target="blank">Source</a> : null;
    
    const divClassnames = classnames({
      [styles['news-container']]: true,
      [styles['positive']]: (this.props.newsArticle.sentiment > 0),
      [styles['negative']]: (this.props.newsArticle.sentiment < 0),
      [styles['neutral']]: (this.props.newsArticle.sentiment === 0)
    });
    return (
      <div className={divClassnames}>
        <p className={styles['headline']}>{this.props.newsArticle.Headline}</p>
        <p className={styles['summary']}>{summary}{readMore}</p>
        {clickHere}
      </div>
    );
  }
}

export default NewsTab;
