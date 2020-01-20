import React, {Component} from 'react';
import {connect} from 'react-redux';
import App from '../components/app/App';
import PollStaticPage from '../components/pollPage/PollStaticPage';
import PollDynamicPage from '../components/pollPage/PollDynamicPage';
import {getPollData, getProvinceWisePollData, candidateClicked} from '../actions/pollActions';
import {getCanadaMapData, getMapData, regionClicked, regionHovered, regionExitHover} from '../actions/mapActions';
import {getTweetData, changeTweets} from '../actions/tweetsAction';
import  {getNewsData, changeNews} from '../actions/newsActions';
import {pageClick, clearData} from '../actions/appActions';

class PollContainer extends Component {
  componentDidMount() {
    this.props.clearData();
    this.props.getPollData();
    this.props.getCanadaMapData();
    this.props.getMapData();
    this.props.getProvinceWisePollData();
    this.props.tweetDataFetch();
    this.props.newsDataFetch();
  }

  render() {
    return (
      <App {...this.props} static={PollStaticPage} dynamic={PollDynamicPage}/>
    );
  }
}

const mapStateToProps = (state) => state;

const mapDispatchToProps = (dispatch) => ({
  getPollData: () => {
    dispatch(getPollData())
  }, 
  getCanadaMapData: () => {
    dispatch(getCanadaMapData());
  },
  getMapData: () => {
    dispatch(getMapData());
  },
  getProvinceWisePollData: () => {
    dispatch(getProvinceWisePollData());
  },
  candidateClicked: (party, oldPartyClicked) => {
    dispatch(candidateClicked(party));
    dispatch(changeTweets(party, oldPartyClicked));
    dispatch(changeNews(party, oldPartyClicked));
  },
  regionClick: (region) => {
    dispatch(regionClicked(region));
  },
  regionHovered: (region) => {
    dispatch(regionHovered(region));
  },
  regionExitHover: (region) => {
    dispatch(regionExitHover(region));
  },
  tweetDataFetch: () => {
    dispatch(getTweetData());
  },
  newsDataFetch: () => {
    dispatch(getNewsData());
  },
  pageClicked: (page) => {
    dispatch(pageClick(page));
  },
  clearData: () => {
    dispatch(clearData());
  }
});

export default connect(
  mapStateToProps, mapDispatchToProps
)(PollContainer);
