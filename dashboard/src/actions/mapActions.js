import urls from "../constants/urls";
import actionConstants from '../constants/actionConstants';
import {createHash} from '../util/util';

export const getCanadaMapData = () => dispatch => (
  fetch(urls.mapJSON).then(
    (response) => response.json()
  ).then((response) => {
    dispatch(dispatchMapDetails(response));
  }).catch((err) => console.log(err))
);

export const getMapData = () => dispatch => (
  fetch(urls.mapDataJSON)
    .then((response) => response.json())
    .then((response) => {
      const hash = createHash(response, 'Province');
      dispatch(dispatchMapData(hash));
    }).catch((err) => {
    console.log(err);
  })
);

export const getTweetsSentimentMapData = () => dispatch => (
  fetch(urls.mapTweetsSentimentJSON)
    .then((response) => response.json())
    .then((response) => {
      const hash = createHash(response, 'Province');
      let min = 10000;
      let max = -1;
      const parties = ['Conservative', 'Liberal', 'NDP'];
      response.forEach((item) => {
        parties.forEach((party) => {
          if (item[party] < min) {
            min = item[party];
          }
          if(item[party] > max) {
            max = item[party];
          }
        });
      })
      dispatch(dispatchMapData(hash, min, max));
    }).catch((err) => {
    console.log(err);
  })
);

export const getTweetsMentionsMapData = () => dispatch => (
  fetch(urls.mapTweetsMentionsJSON)
    .then((response) => response.json())
    .then((response) => {
      const hash = createHash(response, 'Province');
      let min = 10000;
      let max = -1;
      const parties = ['Conservative', 'Liberal', 'NDP'];
      response.forEach((item) => {
        parties.forEach((party) => {
          if (item[party] < min) {
            min = item[party];
          }
          if(item[party] > max) {
            max = item[party];
          }
        });
      })
      dispatch(dispatchMapData(hash, min, max));
    }).catch((err) => {
    console.log(err);
  })
);

export const dispatchMapDetails = (payload) => ({
  type: actionConstants.ADD_MAP_DATA,
  payload
});

export const dispatchMapData = (hash, min, max) => ({
  type: actionConstants.ADD_MAP_DETAILS,
  payload: {hash, min, max}
});

export const regionClicked = (payload) => ({
  type: actionConstants.REGION_CLICKED,
  payload
});

export const regionHovered = (payload) => ({
  type: actionConstants.REGION_HOVERED,
  payload
})

export const regionExitHover = (payload) => ({
  type: actionConstants.REGION_EXIT_HOVERED,
  payload
})