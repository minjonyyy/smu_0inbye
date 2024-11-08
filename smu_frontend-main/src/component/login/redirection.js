import axios from 'axios'
import { useNavigate } from 'react-router-dom';

const Server = process.env.REACT_APP_BACK_SERVER;

const Redirection = () => {
    const AUTHORIZE_CODE = new URL(window.location.href).searchParams.get("code");
    const navigate = useNavigate();

    if (AUTHORIZE_CODE) {
        console.log("Sending AUTHORIZE_CODE:", AUTHORIZE_CODE); // 추가된 로그
        axios.post(`${Server}/oauth/`, {
            AUTHORIZE_CODE: AUTHORIZE_CODE
        })
        .then(response => {
            const accessToken = response.data.access;
            const refreshToken = response.data.refresh;
            const email = response.data.email;  // 서버에서 반환된 이메일

            // access 토큰은 로컬스토리지에 저장
            localStorage.setItem('access_token', accessToken);
            // 이메일을 로컬스토리지에 저장
            localStorage.setItem('userEmail', email);

            // refresh 토큰은 쿠키에 저장
            document.cookie = `refresh_token=${refreshToken}; path/;`;

            navigate('/');
        })
        .catch(error => {
            console.error("오류났음", error.response.data); 
        });
    } else {
        console.error("코드가 없습니다."); 
    }
};

export default Redirection;