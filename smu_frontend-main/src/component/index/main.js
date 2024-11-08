import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

import Vector from '../../images/Vector.png';
import Apart from '../../images/apart.png';
import office from '../../images/office.png';
import House from '../../images/House.png';
import Bed from '../../images/Bed.png';

const Text1 = styled.div`
    width: 100%;
    color: #000;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.5vw;
    font-weight: 700;
    line-height: normal;
    margin-top: 3%;
    margin-bottom: 2%;
    margin-left: 5%;
`;

const Rectangle2 = styled.div`
    background-color: #19254D;
    width: 90%;
    height: 25%;
    border-radius: 32px;
    margin: 0 auto;
    transition: background-color 0.3s, transform 0.3s;
    &:hover {
        background-color: #2A3A6A;
        transform: scale(1.02);
    }
`;

const Text2 = styled.div`
    color: #FFF;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.2vw;
    font-weight: 700;
    padding-left: 5%;
    padding-top: 3%;
`;

const Text3 = styled.div`
    color: #FFF;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.5vw;
    font-weight: 700;
    padding-left: 5%;
    padding-top: 5%;
`;

const Searchbox = styled.div`
    background-color: #FFFFFF;
    width: 90%;
    height: 20%;
    border-radius: 24px;
    margin: 2% auto;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
`;

const Imgvector = styled.div`
    width: 90%;
    padding-top: 1%;
    padding-left: 1%;
    display: flex;
    justify-content: space-between;
`;

const Textinput = styled.input.attrs({
    type: 'text',
    placeholder: '원하시는 지역명을 입력해주세요'
})`
    width: 95%;
    border: none;
    padding: 0.5% 1%;
    border-radius: 16px;
    &:focus {
        outline: none;
        background-color: #f0f4ff;
    }
`;

const Rectangle3 = styled.div`
    background-color: #D0EBFF;
    border-radius: 32px;
    width: 90%;
    height: 10%;
    margin: 0 auto;
    color: #1864AB;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.5vw;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    &:hover {
        background-color: #ffa0dc;
        color: white;
        transform: scale(1.05);
    }
`;

const Section = styled.div`
    width: 90%;
    height: 17%;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
`;

const Rectangle = styled.div`
    background-color: #F3F3F3;
    width: 40%;
    height: 65%;
    border-radius: 32px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
    transition: background-color 0.3s, color 0.3s;
    &:hover {
        background-color: #19254D;
    }
`;

const RectangleText = styled.div`
    color: #000;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.3vw;
    font-weight: 700;
    transition: color 0.3s;
    ${Rectangle}:hover & {
        color: white;
    }
`;

const Mainindex = () => {
    const navigate = useNavigate();

    const handleNotify = () => {
        alert('준비중입니다.'); // Show the notification when clicking on unimplemented sections
    };

    return (
        <>
            <Text1>사기 걱정없는 <br />부동산 직거래</Text1>
            <Rectangle2>
                <Text2>매물 검색하기</Text2>
                <Text3>어떤 집을 찾고 계세요?</Text3>
                <Searchbox>
                    <Imgvector>
                        <img src={Vector} alt="돋보기" />
                        <Textinput />
                    </Imgvector>
                </Searchbox>
            </Rectangle2>
            <Rectangle3 onClick={() => navigate('/upload')}>매물 올리기</Rectangle3>
            <Section>
                <Rectangle onClick={() => navigate('/board')}>
                    <img src={Apart} alt="아파트" />
                    <RectangleText>아파트</RectangleText>
                </Rectangle>
                <Rectangle onClick={handleNotify}> {/* Trigger notification for this section */}
                    <img src={House} alt="빌라,주택" />
                    <RectangleText>빌라,주택</RectangleText>
                </Rectangle>
            </Section>
            <Section>
                <Rectangle onClick={handleNotify}> {/* Trigger notification for this section */}
                    <img src={Bed} alt="오피스텔" />
                    <RectangleText>오피스텔</RectangleText>
                </Rectangle>
                <Rectangle onClick={handleNotify}> {/* Trigger notification for this section */}
                    <img src={office} alt="상가,사무실" />
                    <RectangleText>상가,사무실</RectangleText>
                </Rectangle>
            </Section>
        </>
    );
}

export default Mainindex;
