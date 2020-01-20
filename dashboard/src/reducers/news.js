import actionConstants from '../constants/actionConstants';
import {getBiasPieData, filterNewsNumberArticles, filterNewsStackedSentimentArticles} from '../util/news';

const initialState = {
  allNews: [],
  news: [],
  candidateData: [],
  partyClicked: '',
  allBiasPie: [],
  biasPie: [],
  biasPieLabels: [],
  allNewsBarCandidate: {},
  newsBarCandidate: [],
  newsBarLabels: [],
  allStackedData: [],
  stackedData: [],
  labels: ['CPC', 'LPC', 'NDP'],
  biasClicked: '',
  allNewsWordCloud: {},
  newsWordCloud: []
};

export default (state=initialState, action = {}) => {
  switch(action.type) {
    case actionConstants.CLEAR_DATA:
      return {...state, ...initialState};
    case actionConstants.NEWS_DATA_FETCH:
      return {...state, ...{allNews: action.payload, news: action.payload['all']}};
    case actionConstants.NEWS_CANDIDATE_FETCH:
      return {...state, ...{candidateData: action.payload}};
    case actionConstants.CANDIDATE_CLICKED_NEWS:
      const partyClicked = (action.payload === state.partyClicked) ? '' : action.payload;
      return {
        ...state, 
        ...{
          partyClicked,
          biasPie: getBiasPieData(state.allBiasPie, (partyClicked) ? partyClicked : 'all'),
          newsBarCandidate: filterNewsNumberArticles(state.allNewsBarCandidate, partyClicked, state.biasClicked),
          newsWordCloud: (partyClicked) ? state.allNewsWordCloud[partyClicked] : state.allNewsWordCloud['all']
        }
      }
    case actionConstants.NEWS_CHANGE:
      return {
        ...state,
        ...{
          news: state.allNews[action.payload]
        }
      };
    case actionConstants.BIAS_PIE_FETCHED:
      return {
        ...state, 
        ...{
          allBiasPie: action.payload.data,
          biasPie: action.payload.pieChartData,
          biasPieLabels: action.payload.labels
        }
      };
    case actionConstants.NEWS_CANDIDATES_BAR_FETCH:
      return {
        ...state,
        ...{
          allNewsBarCandidate: action.payload.allNews,
          newsBarCandidate: action.payload.data,
          newsBarLabels: action.payload.labels
        }
      };
    case actionConstants.NEWS_CANDIDATES_STACKED_BAR_FETCH:
      return {
        ...state,
        ...{
          allStackedData: action.payload.allStackedData,
          stackedData: action.payload.stackedData
        }
      };
    case actionConstants.BIAS_CLICKED:
      const biasClicked = (action.payload === state.biasClicked) ? '' : action.payload
      return {
        ...state,
        ...{
          biasClicked: (action.payload === state.biasClicked) ? '' : action.payload,
          newsBarCandidate: filterNewsNumberArticles(state.allNewsBarCandidate, state.partyClicked, biasClicked),
          stackedData: filterNewsStackedSentimentArticles(state.allStackedData, biasClicked)
        }
      };
    case actionConstants.NEWS_WORD_CLOUD:
      return {
        ...state,
        ...{
          allNewsWordCloud: action.payload.allData,
          newsWordCloud: action.payload.data
        }
      };
    default:
      return state;
  }
}