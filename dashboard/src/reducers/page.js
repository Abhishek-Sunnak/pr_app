import actionConstants from '../constants/actionConstants';

const initialState = {
  page: 'Home'
};

export default (state=initialState, action = {}) => {
  switch(action.type) {
    case actionConstants.PAGE_CHANGE:
      return {...state, ...{page: action.payload}};
    default:
      return state;
  }
}