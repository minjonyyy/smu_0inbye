import React from 'react';
import styled from 'styled-components';
import kakao from '../../images/kakao_login_large_wide1.png';

const Container = styled.div`
    width: 100%;
    height: 80vh; /* 화면 전체 높이 사용 */
    display: flex;
    flex-direction: column;
    align-items: center; /* 수평 중앙 정렬 */
    justify-content: center; /* 수직 중앙 정렬 */
    font-family: "Spoqa Han Sans Neo"; /* 일관된 폰트 사용 */
`;

const Text1 = styled.div`
    color: #000;
    font-size: 1.5vw; /* 글씨 크기 설정 */
    font-weight: 700;
    text-align: center; /* 텍스트 중앙 정렬 */
    margin-bottom: 60px; /* 이미지와의 간격 조정 */
`;

const Kakaoimage = styled.img`
    width: 90%; /* 화면 너비의 90%로 설정 */
    max-width: 350px; /* 최대 너비 설정 */
    cursor: pointer;
    transition: transform 0.3s; /* 부드러운 확대 효과 */

    &:hover {
        transform: scale(1.05); /* 마우스 오버 시 확대 */
    }
`;

const Kakaologin = () => {

    const KAKAO_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.REACT_APP_KAKAO_CLIENT_ID}&redirect_uri=http://localhost:3000/oauth&response_type=code`;


    const clickToKakao = () => {
        window.location.replace(KAKAO_URL);
    }

    return (
        <Container>
            <Text1>간편하게 로그인하고<br />다양한 서비스를 이용하세요.</Text1>
            <Kakaoimage onClick={clickToKakao} src={kakao} alt="카카오 로그인" />
        </Container>
    );
}

export default Kakaologin;
