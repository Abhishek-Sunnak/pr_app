import React, { Component } from 'react';
import classnames from 'classnames';
import styles from './header.module.scss';

class Header extends Component {
  onClickHome = () => {
    this.props.history.push('/');
    this.props.pageClicked('Home');
  }

  onClickTweets = () => {
    this.props.history.push('/twitter');
    this.props.pageClicked('Tweets');
  }

  onClickNews = () => {
    this.props.history.push('/news');
    this.props.pageClicked('News');
  }

  render() {
    const homeStyle = classnames({
      [styles['tab']]: true,
      [styles['selected']]: this.props.page.page === 'Home'
    });

    const tweetsStyle = classnames({
      [styles['tab']]: true,
      [styles['selected']]: this.props.page.page === 'Tweets'
    });

    const newsStyle = classnames({
      [styles['tab']]: true,
      [styles['selected']]: this.props.page.page === 'News'
    });
    return (
      <header className={styles['header-container']}>
        <nav>
          <ul className={styles['tabs']}>
            <li className={homeStyle} onClick={this.onClickHome}>Home</li>
            <li className={tweetsStyle} onClick={this.onClickTweets}>Tweets</li>
            <li className={newsStyle} onClick={this.onClickNews}>News</li>
          </ul>
        </nav>
        <h1 className={styles['title']}>2019 Canada Election Analysis</h1>

      </header>
    );
  }
}

export default Header;
