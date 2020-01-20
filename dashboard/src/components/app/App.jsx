import React, { Component } from 'react';
import classnames from 'classnames';
import Header from '../header/Header';
import styles from './app.module.scss';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      page: 0
    };
  }

  onPageDown = () => {
    this.setState({
      page: this.state.page + 1
    });
  }

  onPageUp = () => {
    this.setState({
      page: this.state.page - 1
    });
  }

  render() {
    const Static = this.props.static;
    const Dynamic = this.props.dynamic;
    const upStyleName = classnames({
      [styles['arrow-up']]: true,
      [styles['disabled']]: this.state.page === 0
    });

    const downStyleName = classnames({
      [styles['arrow-down']]: true,
      [styles['disabled']]: this.state.page === 2
    });
    return (
      <div className={styles['app']}>
        <div className={styles['header']}><Header {...this.props} /></div>
        <div className={styles['app-body']}>
          <div className={`width-50 height-100 ${styles['static']}`}>
            <Static {...this.props} styles={styles} />
          </div>
          <div className="width-50 height-100 relative">
            <div className={styles['arrow-container']}>
              <div onClick={this.onPageUp} className={upStyleName}></div>
            </div>
            <div className={styles['dynamic-container']}>
              <Dynamic {...this.props} styles={styles} page={this.state.page} />
            </div>
            <div className={styles['arrow-container']}>
              <div onClick={this.onPageDown} className={downStyleName}></div>
            </div>
          </div>
        </div>
        
      </div>
      
    );
  }
}

export default App;
