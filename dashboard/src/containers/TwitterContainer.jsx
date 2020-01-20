import React, {Component} from 'react';
import {connect} from 'react-redux';
import App from '../components/app/App';
import TwitterStatic from '../components/twitterPages/TwitterStatic';
import TwitterDynamic from '../components/twitterPages/TwitterDynamic';
import {
  getCanadaMapData, 
  getTweetsMentionsMapData, 
  regionClicked, 
  regionHovered, 
  getTweetsSentimentMapData, 
  regionExitHover
} from '../actions/mapActions';
import {
  getTweetsCandidateProfile, 
  tweetCandidateClick, 
  getTweetWordCloudData,
  getTweetData,
  changeTweets,
  getTweetWordCloudHashtagsData,
  getTweetSentimentDistributionData,
  changeTwitterSentimentDetails,
  getTweetNumberDistributionData,
  changeTwitterNumberDetails
} from '../actions/tweetsAction';
import {pageClick, clearData} from '../actions/appActions';

class TwitterContainer extends Component {
  componentDidMount() {
    this.props.clearData();
    this.props.pageClicked('Tweets');
    this.props.getTweetsCandidateProfile();
    this.props.getCanadaMapData();
    this.props.getTweetsMentionsData();
    this.props.getTweetWordCloudData();
    this.props.tweetDataFetch();
    this.props.getTweetWordCloudHashtagsData();
    this.props.getTweetSentimentDistributionData();
    this.props.getTweetNumberDistributionData();
  }

  render() {
    return (
      <App {...this.props} static={TwitterStatic} dynamic={TwitterDynamic}/>
    );
  }
}

const mapStateToProps = (state) => state;

const mapDispatchToProps = (dispatch) => ({
  pageClicked: (page) => {
    dispatch(pageClick(page));
  },
  getTweetsCandidateProfile: () => {
    dispatch(getTweetsCandidateProfile());
  },
  getCanadaMapData: () => {
    dispatch(getCanadaMapData());
  },
  regionHovered: (region) => {
    dispatch(regionHovered(region));
  },
  regionExitHover: (region) => {
    dispatch(regionExitHover(region));
  },
  getTweetsMentionsData: () => {
    dispatch(getTweetsMentionsMapData());
  },
  getTweetsSentimentData: () => {
    dispatch(getTweetsSentimentMapData());
  },
  candidateClicked: (party, oldPartyClicked) => {
    dispatch(tweetCandidateClick(party));
    dispatch(changeTweets(party, oldPartyClicked));
    dispatch(changeTwitterSentimentDetails());
    dispatch(changeTwitterNumberDetails());
  },
  regionClick: (region) => {
    dispatch(regionClicked(region));
    dispatch(changeTwitterSentimentDetails());
    dispatch(changeTwitterNumberDetails());
  },
  clearData: () => {
    dispatch(clearData());
  },
  getTweetWordCloudData: () => {
    dispatch(getTweetWordCloudData());
  },
  tweetDataFetch: () => {
    dispatch(getTweetData());
  },
  getTweetWordCloudHashtagsData: () => {
    dispatch(getTweetWordCloudHashtagsData());
  },
  getTweetSentimentDistributionData: () => {
    dispatch(getTweetSentimentDistributionData());
  },
  getTweetNumberDistributionData: () => {
    dispatch(getTweetNumberDistributionData());
  }
});
export default connect(
  mapStateToProps, mapDispatchToProps
)(TwitterContainer);
