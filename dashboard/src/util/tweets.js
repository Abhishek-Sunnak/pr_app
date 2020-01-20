import { ndpColor, cpcColor, lpcColor, approvalColor, disapprovalColor, dontknowColor } from '../styles/d3Colors';
import strings from '../constants/strings';

export const filterTweetData = (allData, parties) => {
  if(parties.length === 3) {
    return allData['all']
  }
  return allData[parties[0]];
};
  // allData.filter((item) => {
  //   let include = false;
  //   item.party.forEach((party) => {
  //     if (parties.includes(party)) {
  //       include = true;
  //     }
  //   });
  //   return include;
  // })
// );

export const filterTweetsSentimentData = (allData, province='National', parties=['NDP', 'LPC', 'CPC']) => {
  const provinceData = allData.filter((item) => {
    return item.province === province;
  });

  return parties.map((party) => {
    let partyColor = lpcColor;
    if (party === 'NDP') {
      partyColor = ndpColor
    } else if (party === 'CPC') {
      partyColor = cpcColor;
    }
    const objects = provinceData.filter((item) => item.party === party);
    const partyData = objects.map((item) => item.number);

    return {
      label: party,
      data: partyData,
      fill: false,
      backgroundColor: partyColor,
      borderColor: partyColor,
      pointBackgroundColor: partyColor,
      pointBorderColor: "#fff",
    };
  });
}

export const filterTweetsNumberData = (allData, province='National', parties=['NDP', 'LPC', 'CPC']) => {
  const provinceData = allData.filter((item) => {
    return item.province === province;
  });

  return parties.map((party) => {
    let partyColor = lpcColor;
    if (party === 'NDP') {
      partyColor = ndpColor
    } else if (party === 'CPC') {
      partyColor = cpcColor;
    }
    const objects = provinceData.filter((item) => item.party === party);
    const partyData = objects.map((item) => item.number);

    return {
      label: party,
      data: partyData,
      fill: false,
      backgroundColor: partyColor,
      borderColor: partyColor,
      pointBackgroundColor: partyColor,
      pointBorderColor: "#fff",
    };
  });
}

// export const filterTweetsSentimentDataOnSentiment = (allData, province, parties) => {
  // const provinceData = allData.filter((item) => {
  //   return item.province === province && item.party === party;
  // });

  // const positiveData = provinceData.map((item) => item.number);
  // const negativeData = provinceData.map((item) => item.avgNegative);
  // const neutralData = provinceData.map((item) => item.avgNeutral);

  // return [{
  //   label: strings.POSITIVE,
  //   data: positiveData,
  //   fill: false,
  //   backgroundColor: approvalColor,
  //   borderColor: approvalColor,
  //   pointBackgroundColor: approvalColor,
  //   pointBorderColor: "#fff"
  // }, {
  //   label: strings.NEGATIVE,
  //   data: negativeData,
  //   fill: false,
  //   backgroundColor: disapprovalColor,
  //   borderColor: disapprovalColor,
  //   pointBackgroundColor: disapprovalColor,
  //   pointBorderColor: "#fff"
  // }, {
  //   label: strings.NEUTRAL,
  //   data: neutralData,
  //   fill: false,
  //   backgroundColor: dontknowColor,
  //   borderColor: dontknowColor,
  //   pointBackgroundColor: dontknowColor,
  //   pointBorderColor: "#fff"
  // }];
  // const provinceData = allData.filter((item) => {
  //   return item.province === province;
  // });

  // return parties.map((party) => {
  //   let partyColor = lpcColor;
  //   if (party === 'NDP') {
  //     partyColor = ndpColor
  //   } else if (party === 'CPC') {
  //     partyColor = cpcColor;
  //   }
  //   const objects = provinceData.filter((item) => item.party === party);
  //   const partyData = objects.map((item) => item.number);

  //   return {
  //     label: party,
  //     data: partyData,
  //     fill: false,
  //     backgroundColor: partyColor,
  //     borderColor: partyColor,
  //     pointBackgroundColor: partyColor,
  //     pointBorderColor: "#fff",
  //   };
  // });
  
// }

export const getLabelsSentimentData = (allData) => {
  const provinceData = allData.filter((item) => (
    item.province === 'National' && item.party === 'NDP'
  ));
  return provinceData.map((item) => item.time);
}