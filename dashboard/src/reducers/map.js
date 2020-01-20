import actionConstants from '../constants/actionConstants';
const initialState = {
  canadamap: [],
  mapData: {},
  regionClicked: '',
  regionHovered: '',
  min: 0,
  max: 100
};

export default (state=initialState, action = {}) => {
  switch(action.type) {
    case actionConstants.CLEAR_DATA:
      return {...state, ...initialState};
    case actionConstants.ADD_MAP_DATA:
      return {...state, ...{canadamap: action.payload}};
    case actionConstants.ADD_MAP_DETAILS:
      return {
        ...state, 
        ...{
          mapData: action.payload.hash,
          min: action.payload.min,
          max: action.payload.max
        }
      };
    case actionConstants.REGION_HOVERED:
      return {...state, ...{regionHovered: action.payload}};
    case actionConstants.REGION_EXIT_HOVERED:
      return {...state, ...{regionHovered: ''}};
    default:
      return state;
  }
}