import { ndpColor, cpcColor, lpcColor, approvalColor, disapprovalColor, dontknowColor} from '../styles/d3Colors';
import strings from '../constants/strings';

export const filterNewsData = (allData, parties) => (
  allData.filter((item) => {
    let include = false;
    item.party.forEach((party) => {
      if (parties.includes(party)) {
        include = true;
      }
    });
    return include;
  })
);

export const getBiasPieData = (data, key='all') => (
  data[key].map((item) => item.value)
);

export const getBiasPieDataLabels = (data) => (
  data['all'].map((item) => item.bias)
);

export const getArticlesForCandidate = (allData, parties = ['NDP', 'CPC', 'LPC'], bias='data') => {
  return parties.map((party) => {
    let partyColor = lpcColor;
    if (party === 'CPC') {
      partyColor = cpcColor;
    } else if (party === 'NDP') {
      partyColor = ndpColor;
    }
    const data = allData[party].map((item) => item[bias]);
    return {
      label: party,
      backgroundColor: partyColor,
      borderColor: 'rgb(255,255,255)',
      borderWidth: 1,
      hoverBackgroundColor: partyColor,
      hoverBorderColor: 'rgb(255,255,255)',
      data: data
    };
  });
}

export const getNewsArticlesForCandidateLabels = (allData) => {
  return allData['CPC'].map(item => item.publication);
}

export const formatDataForStackedBarChart = (data) => {
  const positive = [data.CPC.positive, data.LPC.positive, data.NDP.positive];
  const negative = [data.CPC.negative, data.LPC.negative, data.NDP.negative];
  const neutral = [data.CPC.neutral, data.LPC.neutral, data.NDP.neutral];

  return [
    {
      label: strings.POSITIVE,
      backgroundColor: approvalColor,
      borderColor: 'rgb(255,255,255)',
      borderWidth: 1,
      hoverBackgroundColor: approvalColor,
      hoverBorderColor: 'rgb(255,255,255)',
      data: positive
    },
    {
      label: strings.NEGATIVE,
      backgroundColor: disapprovalColor,
      borderColor: 'rgb(255,255,255)',
      borderWidth: 1,
      hoverBackgroundColor: disapprovalColor,
      hoverBorderColor: 'rgb(255,255,255)',
      data: negative
    },
    {
      label: strings.NEUTRAL,
      backgroundColor: dontknowColor,
      borderColor: 'rgb(255,255,255)',
      borderWidth: 1,
      hoverBackgroundColor: dontknowColor,
      hoverBorderColor: 'rgb(255,255,255)',
      data: neutral
    }
  ];
}

export const filterNewsNumberArticles = (allData, partyClicked, bias) => {
  let parties = ['NDP', 'CPC', 'LPC']
  if(partyClicked) {
    parties = [partyClicked]
  }

  let biasKey = 'data';
  if(bias) {
    biasKey = bias;
  }
  return getArticlesForCandidate(allData, parties, biasKey);
}

export const filterNewsStackedSentimentArticles = (allData, bias) => {
  let biasKey = 'all';
  if (bias) {
    biasKey = bias;
  }
  return formatDataForStackedBarChart(allData[biasKey]);
}