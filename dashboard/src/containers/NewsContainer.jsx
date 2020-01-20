import React, {Component} from 'react';
import {connect} from 'react-redux';
import App from '../components/app/App';
import NewsStatic from '../components/newsPages/NewsStatic';
import NewsDynamic from '../components/newsPages/NewsDynamic';
import  {
  getNewsData, 
  getNewsCandidateData, 
  newsCandidateClick, 
  changeNews,
  biasPie,
  newsPerCandidate,
  newsPerCandidateStacked,
  biasClicked,
  fetchNewsWordCloud
} from '../actions/newsActions';
import {pageClick, clearData} from '../actions/appActions';

class NewsContainer extends Component {
  componentDidMount() {
    this.props.clearData();
    this.props.pageClicked('News');
    this.props.newsDataFetch();
    this.props.newsDataCandidateFetch();
    this.props.biasPie();
    this.props.newsPerCandidate();
    this.props.newsPerCandidateStacked();
    this.props.fetchNewsWordCloud();
  }

  render() {
    return (
      <App 
        {...this.props} 
        static={NewsStatic}
        dynamic={NewsDynamic}
      />
    );
  }
}

const mapStateToProps = (state) => state;

const mapDispatchToProps = (dispatch) => ({
  pageClicked: (page) => {
    dispatch(pageClick(page));
  },
  clearData: () => {
    dispatch(clearData());
  },
  newsDataFetch: () => {
    dispatch(getNewsData());
  },
  newsDataCandidateFetch: () => {
    dispatch(getNewsCandidateData());
  },
  candidateClicked(party, oldParty) {
    dispatch(newsCandidateClick(party));
    dispatch(changeNews(party, oldParty));
  },
  biasPie: () => {
    dispatch(biasPie());
  },
  newsPerCandidate: () => {
    dispatch(newsPerCandidate());
  },
  newsPerCandidateStacked: () => {
    dispatch(newsPerCandidateStacked());
  },
  biasClicked: (bias) => {
    dispatch(biasClicked(bias));
  },
  fetchNewsWordCloud: () => {
    dispatch(fetchNewsWordCloud());
  }
});
export default connect(
  mapStateToProps, mapDispatchToProps
)(NewsContainer);
