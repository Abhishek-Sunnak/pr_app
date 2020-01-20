import actionConstants from '../constants/actionConstants';
import {getData, getPartyData, getProvinceData} from '../util/poll';
import strings from '../constants/strings';

const initialState = {
  data: [],
  partyDetails: [],
  labels: [],
  dataset: [],
  provinceWiseData: [],
  provinceLineChart: [],
  provinceLineChartLabels: [],
  partyClicked: '',
  title: strings.HISTORICAL_POLL_DATA_TITLE,
  regionClicked: '',
  title2: strings.PROVINCIAL_POLL_DATA_TITLE,
}

export default (state=initialState, action = {}) => {

  let province;
  let parties;
  let title2;
  switch(action.type) {
    case actionConstants.CLEAR_DATA:
      return {...state, ...initialState};
    case actionConstants.ADD_POLL_DATA:
      return {...state, ...action.payload};
    case actionConstants.ADD_PROVINCE_DATA_DETAILS:
      return {...state, ...action.payload};
    case actionConstants.CANDIDATE_CLICKED:
      province = (state.regionClicked) ? state.regionClicked : 'National';
      if (state.partyClicked === action.payload) {
        if (province === 'National') {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE;
        } else {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE_REGION_SET.replace('REGION_NAME', province);
        }
        parties = ['NDP', 'CPC', 'LPC'];
        return {
          ...state, 
          ...{
            partyClicked: '', 
            dataset: getData(state.data),
            title: strings.HISTORICAL_POLL_DATA_TITLE,
            provinceLineChart: getProvinceData(state.provinceWiseData, province, parties),
            title2
          }
        };
      }
      if (province === 'National') {
        title2 = strings.PROVINCIAL_POLL_DATA_TITLE_CANDIDATE_SET.replace('PARTY_NAME', action.payload);
      } else {
        title2 = strings.PROVINCIAL_POLL_DATA_TITLE_CANDIDATE_AND_REGION_SET.replace('REGION_NAME', province).replace('PARTY_NAME', action.payload);
      }
      parties = (action.payload) ? [action.payload] : ['NDP', 'CPC', 'LPC'];
      return {
        ...state, 
        ...{
          partyClicked: action.payload, 
          dataset: getPartyData(state.data, action.payload),
          title: strings.HISTORICAL_POLL_DATA_TITLE_PARTY.replace('PARTY_NAME', action.payload),
          provinceLineChart: getProvinceData(state.provinceWiseData, province, parties),
          title2
        }
      };
    case actionConstants.REGION_CLICKED:
      province = (action.payload) ? action.payload : 'National';
      parties = (state.partyClicked) ? [state.partyClicked] : ['NDP', 'CPC', 'LPC'];
      if (province === 'National') {
        if(state.partyClicked === '') {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE;
        } else {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE_CANDIDATE_SET.replace('PARTY_NAME', state.partyClicked);
        }
      } else {
        if(state.partyClicked === '') {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE_REGION_SET.replace('REGION_NAME',action.payload);
        } else {
          title2 = strings.PROVINCIAL_POLL_DATA_TITLE_CANDIDATE_AND_REGION_SET.replace('PARTY_NAME', state.partyClicked).replace('REGION_NAME',action.payload);
        }
      }
      return {
        ...state,
        ...{
          provinceLineChart: getProvinceData(state.provinceWiseData, province, parties),
          regionClicked: action.payload,
          title2
        }
      };
    default:
      return state;
  }
}