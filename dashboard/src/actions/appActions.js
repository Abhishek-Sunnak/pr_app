import actionConstants from '../constants/actionConstants';
export const pageClick  = (payload) => ({
  type: actionConstants.PAGE_CHANGE,
  payload
});

export const clearData = () => ({
  type: actionConstants.CLEAR_DATA
});