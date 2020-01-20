import { combineReducers } from 'redux';
import polls from './polls';
import map from './map';
import tweets from './tweets';
import news from './news';
import page from './page';

export default combineReducers({
  polls,
  map,
  tweets,
  news,
  page
});