import urls from '../constants/urls';
import actionConstants from '../constants/actionConstants';
import candidateProfile from '../constants/candidateProfile';
import {filterTweetsSentimentData, getLabelsSentimentData, filterTweetsSentimentDataOnSentiment,  filterTweetsNumberData} from '../util/tweets';

export const getTweetData = () => (dispatch) => (
  fetch(urls.tweetsJSON).then((response) => response.json())
  .then((response) => {
    dispatch(tweetsDataFetch(response));
  }).catch((err) => {
    console.log(err);
  })
);

export const getTweetWordCloudData = () => (dispatch) => (
  fetch(urls.wordCloudTweetsJSON).then((response) => response.json())
  .then((response) => {
    dispatch(tweetsDataWordCloudFetch(response));
  }).catch((err) => {
    console.log(err);
  })
);

export const getTweetWordCloudHashtagsData = () => (dispatch) => (
  fetch(urls.wordCloudHashtagsTweetsJSON).then((response) => response.json())
  .then((response) => {
    dispatch(tweetsDataWordCloudHashtagsFetch(response));
  }).catch((err) => {
    console.log(err);
  })
);

export const getTweetSentimentDistributionData = () => (dispatch) => (
  fetch(urls.tweetsSentimentDistributionJSON).then((response) => response.json())
  .then((response) => {
    const data = filterTweetsSentimentData(response);
    const labels = getLabelsSentimentData(response);
    dispatch(tweetsDistributionSentimentFetch(response, data, labels));
  }).catch((err) => {
    console.log(err);
  })
);

export const changeTwitterSentimentDetails = () => (dispatch, getState) => {
  const state = getState();
  const regionClicked = (state.polls.regionClicked) ? state.polls.regionClicked : 'National';
  const partyClicked = (state.tweets.partyClicked) ? [state.tweets.partyClicked] : ['NDP', 'CPC', 'LPC'];
  let newData;
  if(partyClicked.length === 3) {
    newData = filterTweetsSentimentData(state.tweets.allTweetsSentimentDistribution, regionClicked, partyClicked);
  } else {
    newData = filterTweetsSentimentData(state.tweets.allTweetsSentimentDistribution, regionClicked, [state.tweets.partyClicked]);
  }
  dispatch(tweetsDistributionSentimentUpdate(newData));
}

export const tweetsDistributionSentimentFetch = (allData, data, labels) => ({
  type: actionConstants.TWEETS_WORD_SENTIMENT_DISTRIBUTION,
  payload: {allData, data, labels}
});

export const tweetsDistributionSentimentUpdate = (payload) => ({
  type: actionConstants.TWEETS_SENTIMENT_DISTRIBUTION_UPDATE,
  payload
});

export const getTweetNumberDistributionData = () => (dispatch) => (
  fetch(urls.tweetsNumberDistributionJSON).then((response) => response.json())
  .then((response) => {
    const data = filterTweetsNumberData(response);
    const labels = getLabelsSentimentData(response);
    dispatch(tweetsDistributionNumberFetch(response, data, labels));
  }).catch((err) => {
    console.log(err);
  })
);

export const changeTwitterNumberDetails = () => (dispatch, getState) => {
  const state = getState();
  const regionClicked = (state.polls.regionClicked) ? state.polls.regionClicked : 'National';
  const partyClicked = (state.tweets.partyClicked) ? [state.tweets.partyClicked] : ['NDP', 'CPC', 'LPC'];
  const newData = filterTweetsNumberData(state.tweets.allTweetsCountDistribution, regionClicked, partyClicked);
  dispatch(tweetsDistributionNumberUpdate(newData));
}

export const tweetsDistributionNumberFetch = (allData, data, labels) => ({
  type: actionConstants.TWEETS_NUMBER_DISTRIBUTION,
  payload: {allData, data, labels}
});

export const tweetsDistributionNumberUpdate = (payload) => ({
  type: actionConstants.TWEETS_NUMBER_DISTRIBUTION_UPDATE,
  payload
});

export const tweetsDataFetch = (payload) => ({
  type: actionConstants.TWEETS_DATA_FETCH,
  payload
});

export const tweetsDataWordCloudFetch = (payload) => ({
  type: actionConstants.TWEETS_WORD_CLOUD_DATA,
  payload
});

export const tweetsDataWordCloudHashtagsFetch = (payload) => ({
  type: actionConstants.TWEETS_WORD_CLOUD_HASHTAGS_DATA,
  payload
});

export const changeTweets = (party, oldPartyClicked) => {
  let partyClicked = 'all';
  if(party !== oldPartyClicked) {
    partyClicked = party;
  }
  return {
    type: actionConstants.TWEETS_CHANGE,
    payload: partyClicked
  };
}

export const getTweetsCandidateProfile = () => (dispatch) => (
  fetch(urls.cadidateTweetsJSON).then(response => response.json())
    .then((response) => {
      const cpc = candidateProfile.CPC;
      cpc.positive = response.cpcPositive;
      cpc.negative = response.cpcNegative;
      cpc.neutral = response.cpcNeutral;

      const lpc = candidateProfile.LPC;
      lpc.positive = response.lpcPositive;
      lpc.negative = response.lpcNegative;
      lpc.neutral = response.lpcNeutral;

      const ndp = candidateProfile.NDP;
      ndp.positive = response.ndpPositive;
      ndp.negative = response.ndpNegative;
      ndp.neutral = response.ndpNeutral;

      dispatch(tweetCandidateFetch([cpc, lpc, ndp]));
    }).catch((err) => {
    console.log(err);
  })
)

const tweetCandidateFetch = (payload) => ({
  type: actionConstants.TWEETS_CANDIDATE_FETCH,
  payload
});

export const tweetCandidateClick = (payload) => ({
  type: actionConstants.CANDIDATE_CLICKED_TWEETS,
  payload
});