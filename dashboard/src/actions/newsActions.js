import urls from '../constants/urls';
import actionConstants from '../constants/actionConstants';
import candidateProfile from '../constants/candidateProfile';
import {
  getBiasPieData, 
  getArticlesForCandidate, 
  getNewsArticlesForCandidateLabels, 
  formatDataForStackedBarChart,
  getBiasPieDataLabels
} from '../util/news';

export const getNewsData = () => (dispatch) => (
  fetch(urls.newsJSON).then((response) => response.json())
  .then((response) => {
    dispatch(newsDataFetch(response));
  }).catch((err) => {
    console.log(err);
  })
);

export const getNewsCandidateData = () => (dispatch) => (
  fetch(urls.newsCandidateJSON).then((response) => response.json())
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

    dispatch(newsDataCandidateFetch([cpc, lpc, ndp]));
  }).catch((err) => {
    console.log(err);
  })
);

export const newsDataFetch = (payload) => ({
  type: actionConstants.NEWS_DATA_FETCH,
  payload
});

export const newsDataCandidateFetch = (payload) => ({
  type: actionConstants.NEWS_CANDIDATE_FETCH,
  payload
});

export const newsCandidateClick = (payload) => ({
  type: actionConstants.CANDIDATE_CLICKED_NEWS,
  payload
})

export const changeNews = (party, oldPartyClicked) => {
  let partyClicked = 'all';
  if(party !== oldPartyClicked) {
    partyClicked = party;
  }
  return {
    type: actionConstants.NEWS_CHANGE,
    payload: partyClicked
  };
}

export const biasPie = () => dispatch => (
  fetch(urls.newsBiasPieJSON).then((response) => response.json())
    .then((response) => {
      const data = getBiasPieData(response);
      const labels = getBiasPieDataLabels(response, 'bias');
      dispatch(biasPieFetch(response, data, labels));
    }).catch((err) => {
      console.log(err);
    })
);

export const biasPieFetch = (data, pieChartData, labels) => ({
  type: actionConstants.BIAS_PIE_FETCHED,
  payload: {data, pieChartData, labels}
})

export const newsPerCandidate = () => (dispatch) => (
  fetch(urls.newsPerCandidateJSON).then(response => response.json())
  .then((response) => {
    const data = getArticlesForCandidate(response);
    const labels = getNewsArticlesForCandidateLabels(response);
    dispatch(newsPerCandidateFetch(response, data, labels));
  })
  .catch((err) => {
    console.log(err);
  })
);

export const newsPerCandidateStacked = () => (dispatch) => (
  fetch(urls.newsPerCandidateStackedJSON).then(response => response.json())
  .then((response) => {
    const data = formatDataForStackedBarChart(response['all']);
    dispatch(newsPerCandidateStackedFetch(response, data));
  }).catch((err) => {
    console.log(err);
  })
);

export const newsPerCandidateFetch = (allNews, data, labels) => ({
  type: actionConstants.NEWS_CANDIDATES_BAR_FETCH,
  payload: {allNews, data, labels}
});

export const newsPerCandidateStackedFetch = (allStackedData, stackedData) => ({
  type: actionConstants.NEWS_CANDIDATES_STACKED_BAR_FETCH,
  payload: {allStackedData, stackedData}
});

export const biasClicked = (payload) => ({
  type: actionConstants.BIAS_CLICKED,
  payload
});

export const fetchNewsWordCloud = () => dispatch => 
  fetch(urls.newsWordCloud).then(response => response.json()).then((response) => {
    dispatch(newsWordCloudFetch(response, response['all']));
  }).catch((err) => {
    console.log(err);
  });

export const newsWordCloudFetch = (allData, data) => ({
  type: actionConstants.NEWS_WORD_CLOUD,
  payload: {allData, data}
})