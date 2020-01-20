import pollConstants from '../constants/pollConstants';
import { ndpColor, cpcColor, lpcColor, approvalColor, disapprovalColor, dontknowColor } from '../styles/d3Colors';
import partyConstants from '../constants/partyConstants';
import candidateProfile from '../constants/candidateProfile';
import strings from '../constants/strings';

export const getPartyDetails = (data) => {
  const length = data.length;
  const item = data[length - 1];
  const cpcApproval = +item[pollConstants.CPC_APPROVAL_RATINGS];
  const cpcDisapproval = +item[pollConstants.CPC_DISAPPROVAL_RATINGS];
  const cpcDontKnow = 100 - cpcApproval - cpcDisapproval;
  const lpcApproval = +item[pollConstants.LPC_APPROVAL_RATINGS];
  const lpcDisapproval = +item[pollConstants.LPC_DISAPPROVAL_RATINGS];
  const lpcDontKnow = 100 - lpcApproval - lpcDisapproval;
  const ndpApproval = +item[pollConstants.NDP_APPROVAL_RATINGS];
  const ndpDisapproval = +item[pollConstants.NDP_DISAPPROVAL_RATINGS];
  const ndpDontKnow = 100 - ndpApproval - ndpDisapproval;

  // let cpcApproval = 0, cpcDisapproval = 0, cpcDontKnow = 0;
  // let lpcApproval = 0, lpcDisapproval = 0, lpcDontKnow = 0;
  // let ndpApproval = 0, ndpDisapproval = 0, ndpDontKnow = 0;
  // data.forEach(item => {
  //   /** Conservative Party of Canada */
  //   cpcApproval += +item[pollConstants.CPC_APPROVAL_RATINGS];
  //   cpcDisapproval += +item[pollConstants.CPC_DISAPPROVAL_RATINGS];
  //   cpcDontKnow += +item[pollConstants.CPC_DONT_KNOW];
    
  //   /** Liberal Party of Canada */
  //   lpcApproval += +item[pollConstants.LPC_APPROVAL_RATINGS];
  //   lpcDisapproval += +item[pollConstants.LPC_DISAPPROVAL_RATINGS];
  //   lpcDontKnow += +item[pollConstants.LPC_DONT_KNOW];

  //   /** NDP */
  //   ndpApproval += +item[pollConstants.NDP_APPROVAL_RATINGS];
  //   ndpDisapproval += +item[pollConstants.NDP_DISAPPROVAL_RATINGS];
  //   ndpDontKnow += +item[pollConstants.NDP_DONT_KNOW];
  // });

  // cpcApproval /= length;
  // cpcApproval = Math.round(cpcApproval);
  // cpcDisapproval /= length;
  // cpcDisapproval = Math.round(cpcDisapproval);
  // cpcDontKnow = 100 - cpcApproval - cpcDisapproval;

  // lpcApproval /= length;
  // lpcApproval = Math.round(lpcApproval);
  // lpcDisapproval /= length;
  // lpcDisapproval = Math.round(lpcDisapproval);
  // lpcDontKnow = 100 - lpcApproval - lpcDisapproval;

  // ndpApproval /= length;
  // ndpApproval = Math.round(ndpApproval);
  // ndpDisapproval /= length;
  // ndpDisapproval = Math.round(ndpDisapproval);

  // ndpDontKnow = 100 - ndpApproval - ndpDisapproval;

  // // const cpc = {
  // //   party: 'Conservative Party of Canada',
  // //   positive: cpcApproval,
  // //   negative: cpcDisapproval,
  // //   neutral: cpcDontKnow,
  // //   candidate: 'Andrew Scheer', 
  // //   image: 'https://i0.wp.com/www.canadianatheist.com/wp-content/uploads/2017/05/andrew-scheer.jpg?resize=1000%2C1250&amp;ssl=1'
  // // };

  const cpc = candidateProfile.CPC;
  cpc.positive = cpcApproval;
  cpc.negative = cpcDisapproval;
  cpc.neutral = cpcDontKnow;
  
  // const lpc = {
  //   party: 'Liberal Party of Canada',
  //   positive: lpcApproval,
  //   negative: lpcDisapproval,
  //   neutral: lpcDontKnow,
  //   candidate: 'Justin Trudeau', 
  //   image: 'https://postmediatorontosun.files.wordpress.com/2018/07/justin-trudeau1-e1532124806568.jpg'
  // };

  const lpc = candidateProfile.LPC;
  lpc.positive = lpcApproval;
  lpc.negative = lpcDisapproval;
  lpc.neutral = lpcDontKnow;

  // const ndp = {
  //   party: 'New Democratic Party',
  //   positive: ndpApproval,
  //   negative: ndpDisapproval,
  //   neutral: ndpDontKnow,
  //   candidate: 'Jagmeet Singh',
  //   image: 'https://sikhsiyasat.net/wp-content/uploads/Jagmeet-Singh-NDP-MPP.jpg'
  // };

  const ndp = candidateProfile.NDP;
  ndp.positive = ndpApproval;
  ndp.negative = ndpDisapproval;
  ndp.neutral = ndpDontKnow;

  return [cpc, lpc, ndp];

};

export const getDonutData = (approval, disapproval, dontknow) => 
  [approval, disapproval, dontknow]

export const getLabels = (pollData) => pollData.map((poll) => poll.finish);

export const getData = (data) => {
  const ndp = [];
  const cpc = [];
  const lpc = [];
  data.forEach((item) => {
    ndp.push(item.ndpapp);
    cpc.push(item.cpcapp);
    lpc.push(item.lpcapp);
  });

  const ndpDataset = {
    label: "NDP",
    borderColor: ndpColor,
    backgroundColor: ndpColor,
    pointBorderColor: "#fff",
    data: ndp,
    fill: false
  };

  const cpcDataset = {
    label: "CPC",
    borderColor: cpcColor,
    backgroundColor: cpcColor,
    pointBackgroundColor: cpcColor,
    pointBorderColor: "#fff",
    data: cpc,
    fill: false
  }; 
  const lpcDataset = {
    label: "LPC",
    backgroundColor: lpcColor,
    borderColor: lpcColor,
    pointBackgroundColor: lpcColor,
    pointBorderColor: "#fff",
    data: lpc,
    fill: false
  };
  
  return [ndpDataset, cpcDataset, lpcDataset];
};

export const getProvinceData = (data, province='National', parties=['NDP', 'CPC', 'LPC']) => {
  const provinceData = data.filter((item) => item['Province'] === province);
  return parties.map((party) => {
    let partyColor = lpcColor;
    if (party === 'CPC') {
      partyColor = cpcColor;
    } else if (party === 'NDP') {
      partyColor = ndpColor;
    }
    const items = provinceData.map((dataItem) => dataItem[partyConstants[party]]);
    return {
      label: party,
      data: items,
      fill: false,
      backgroundColor: partyColor,
      borderColor: partyColor,
      pointBackgroundColor: partyColor,
      pointBorderColor: "#fff",
    };
  });
};

export const getProvinceDataLabels = (data) => {
  const provinceData = data.filter((item) => item['Province'] === 'National');
  return provinceData.map((item) => item.Date);
};

export const getPartyData = (data, party) => {
  let approvalKey = 'lpcapp';
  let disapprovalKey = 'lpcdis';
  let unknownKey = 'lpcdk';
  if (party === 'CPC')  {
    approvalKey = 'cpcapp';
    disapprovalKey = 'cpcdis';
    unknownKey = 'cpcdk';
  } else if (party  === 'NDP') {
    approvalKey = 'ndpapp';
    disapprovalKey = 'ndpdis';
    unknownKey = 'ndpdk';
  }
  const approval = [];
  const disapproval = [];
  const unknown = [];
  data.forEach((item) => {
    approval.push(item[approvalKey]);
    disapproval.push(item[disapprovalKey]);
    unknown.push(item[unknownKey]);
  });

  const approvalDataset = {
    label: strings.APPROVAL,
    borderColor: approvalColor,
    backgroundColor: approvalColor,
    pointBorderColor: "#fff",
    data: approval,
    fill: false
  };

  const disapprovalDataset = {
    label: strings.DISAPPROVAL,
    borderColor: disapprovalColor,
    backgroundColor: disapprovalColor,
    pointBackgroundColor: disapprovalColor,
    pointBorderColor: "#fff",
    data: disapproval,
    fill: false
  }; 
  const unknownDataset = {
    label: strings.NOT_DECIDED,
    backgroundColor: dontknowColor,
    borderColor: dontknowColor,
    pointBackgroundColor: dontknowColor,
    pointBorderColor: "#fff",
    data: unknown,
    fill: false
  };
  
  return [approvalDataset, disapprovalDataset, unknownDataset];
};