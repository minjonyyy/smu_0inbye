import axios from 'axios';

const Server = process.env.REACT_APP_BACK_SERVER;

const KakaoPay = async () => {

     window.location.replace(`${Server}`);
};


export default KakaoPay;