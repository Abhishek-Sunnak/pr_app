import urls from "../constants/urls";
import actionConstants from "../constants/actionConstants";
import { 
  getPartyDetails, 
  getLabels, 
  getData, 
  getProvinceData, 
  getProvinceDataLabels 
} from "../util/poll";

export const getPollData = () => (dispatch) => {
  return fetch(urls.pollJSON)
  .then((response) => response.json())
  .then((response) => {
    const partyDetails = getPartyDetails(response);
    const labels = getLabels(response);
    const data = getData(response);
    dispatch(pollDataFetch(response, partyDetails, labels, data))
  }).catch((err) => {
    console.log(err);
  })
}

export const getProvinceWisePollData = () => (dispatch) => (
  fetch(urls.provinceWiseDataJSON)
    .then((response) => response.json())
    .then((response)=> {
      const chartData = getProvinceData(response);
      const provinceLabels = getProvinceDataLabels(response);
      dispatch(provinceDataFetch(response, chartData, provinceLabels));
    }).catch((err) => {
      console.log(err);
    })
);

export const provinceDataFetch = (provinceWiseData, provinceLineChart, provinceLineChartLabels) => ({
  type: actionConstants.ADD_PROVINCE_DATA_DETAILS,
  payload: {provinceWiseData, provinceLineChart, provinceLineChartLabels}
});

export const pollDataFetch = (data, partyDetails, labels, dataset) => ({
  type: actionConstants.ADD_POLL_DATA,
  payload: {
    data, partyDetails, labels, dataset
  },
});

export const candidateClicked = (payload) => ({
  type: actionConstants.CANDIDATE_CLICKED,
  payload
})