import actionConstants from '../constants/actionConstants';
import {filterTweetData} from '../util/tweets';
const initialState = {
  allTweets: [],
  tweets: [],
  candidates: [],
  partyClicked: '',
  allWordCloudData: [],
  wordCloudData: [],
  allWordCloudHashtagsData: [],
  wordCloudHashtagsData: [],
  allTweetsSentimentDistribution: [],
  tweetsSentimentDistribution: [],
  tweetsSentimentLabels: [],
  allTweetsCountDistribution: [],
  tweetsCountDistribution: [],
  tweetsNumberLabels: [],
  title: 'Average Sentiment by Party (Weekly)',
  title2: 'Number of tweets by Party (Weekly)',
};

export default (state=initialState, action = {}) => {
  switch(action.type) {
    case actionConstants.CLEAR_DATA:
      return {...state, ...initialState};
    case actionConstants.TWEETS_DATA_FETCH:
      return {...state, ...{allTweets: action.payload, tweets: action.payload['all']}};
    case actionConstants.TWEETS_WORD_CLOUD_HASHTAGS_DATA:
      return {
        ...state, 
        ...{
          allWordCloudHashtagsData: action.payload, 
          wordCloudHashtagsData: action.payload['all']
        }
      };
    case actionConstants.TWEETS_CHANGE:
      return {
        ...state,
        ...{
          tweets: state.allTweets[action.payload]
        }
      };
    case actionConstants.TWEETS_CANDIDATE_FETCH:
      return {
        ...state,
        ...{
          candidates: action.payload
        }
      };
    case actionConstants.CANDIDATE_CLICKED_TWEETS:
      if (state.partyClicked === action.payload) {
        return {
          ...state,
          ...{
            partyClicked: '',
            wordCloudData: filterTweetData(state.allWordCloudData, ['LPC', 'CPC', 'NDP']),
            wordCloudHashtagsData: filterTweetData(state.allWordCloudHashtagsData, ['LPC', 'CPC', 'NDP'])
          }
        };
      }
      return {
        ...state,
        ...{
          partyClicked: action.payload,
          wordCloudData: filterTweetData(state.allWordCloudData, [action.payload]),
          wordCloudHashtagsData: filterTweetData(state.allWordCloudHashtagsData, [action.payload])
        }
      };
    case actionConstants.TWEETS_WORD_CLOUD_DATA:
      return {
        ...state, 
        ...{
          wordCloudData: action.payload['all'],
          allWordCloudData: action.payload
        }
      };
    case actionConstants.TWEETS_WORD_SENTIMENT_DISTRIBUTION:
      return {
        ...state,
        ...{
          allTweetsSentimentDistribution: action.payload.allData,
          tweetsSentimentDistribution: action.payload.data,
          tweetsSentimentLabels: action.payload.labels,
        }
      };
    case actionConstants.TWEETS_SENTIMENT_DISTRIBUTION_UPDATE:
      return {
        ...state,
        ...{
          tweetsSentimentDistribution: action.payload
        }
      };
    case actionConstants.TWEETS_NUMBER_DISTRIBUTION:
      return {
        ...state,
        ...{
          allTweetsCountDistribution: action.payload.allData,
          tweetsCountDistribution: action.payload.data,
          tweetsNumberLabels: action.payload.labels,
        }
      };
    case actionConstants.TWEETS_NUMBER_DISTRIBUTION_UPDATE:
      return {
        ...state,
        ...{
          tweetsCountDistribution: action.payload
        }
      };
    default:
      return state;
  }
}