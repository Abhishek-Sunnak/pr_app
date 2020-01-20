import scheer from '../images/scheer.png';
import trudeau from '../images/trudeau.png';
import singh from '../images/singh.png';
const cpc = {
  party: 'Conservative Party of Canada',
  candidate: 'Andrew Scheer', 
  // image: 'https://i0.wp.com/www.canadianatheist.com/wp-content/uploads/2017/05/andrew-scheer.jpg?resize=1000%2C1250&amp;ssl=1',
  image:  scheer
};

const lpc = {
  party: 'Liberal Party of Canada',
  candidate: 'Justin Trudeau', 
  // image: 'https://postmediatorontosun.files.wordpress.com/2018/07/justin-trudeau1-e1532124806568.jpg'
  image: trudeau
};

const ndp = {
  party: 'New Democratic Party',
  candidate: 'Jagmeet Singh',
  // image: 'https://sikhsiyasat.net/wp-content/uploads/Jagmeet-Singh-NDP-MPP.jpg'
  image: singh
}

export default {
  CPC: cpc,
  LPC: lpc,
  NDP: ndp
};