import React, { PureComponent } from 'react';
import NewsTab from './newstab/NewsTab';

class News extends PureComponent {

  renderNewsTab = () => (
    this.props.news.news.map((newsArticle, index) => 
      <NewsTab 
        key={index}
        newsArticle={newsArticle} 
        {...this.props} 
      />
  ))
  
  render() {
    return (
      <div>
        <p className="heading">Top News</p>
        {this.renderNewsTab()}
      </div>
    );
  }
}

export default News;
