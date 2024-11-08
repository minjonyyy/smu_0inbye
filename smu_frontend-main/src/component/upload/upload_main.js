import React, { useState } from 'react';
import styled from 'styled-components';
// 사진
import Apart from '../../images/apart.png';
import office from '../../images/office.png';
import House from '../../images/House.png';
import Bed from '../../images/Bed.png';
import Light from '../../images/LightBulb.png';
import Warning from '../../images/Warning.png';

import { useNavigate } from 'react-router-dom';

const Text1 = styled.div`
    width: 100%;
    height: 10%;
    color: #000;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.5vw;
    font-weight: 700;
    margin-top: 3%;
    margin-left: 5%;
`;

const Rectangle2 = styled.div`
    width: 90%;
    height: 35%;
    border-radius: 24px; 
    background: #F3F3F3;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
`;

const Imgwaring = styled.div`
    padding: 2% 2% 0 2%;
`;

const Text2 = styled.div`
    color: #000;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.2vw;
    font-weight: 400;
    padding: 2% 2% 0 2%;
`;

const Imglightbulb = styled.div`
    padding-top: 3%;
    padding-left: 2%;
`;

const Text3 = styled.div`
    color: #000;
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.2vw;
    font-weight: 400;
    padding: 2% 2% 0 2%;
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
    background-color: ${({ selected }) => (selected ? '#19254D' : '#F3F3F3')};
    width: 40%;
    height: 65%;
    border-radius: 24px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;

    &:hover {
        background-color: #19254D;
        transform: scale(1.05);
    }
`;

const Text = styled.div`
    color: ${({ selected }) => (selected ? 'white' : '#000')};
    font-family: "Spoqa Han Sans Neo";
    font-size: 1.3vw;
    font-weight: 700;
    transition: color 0.3s;

    ${Rectangle}:hover & {
        color: white; // Change text color to white on hover
    }
`;

const Uploadmain = () => {
    const navigate = useNavigate();
    const [selectedType, setSelectedType] = useState(null);

    const handleSelect = (type) => {
        setSelectedType(type);
        if (type === 'apart') {
            navigate('/selectpurchase');
        } else {
            alert('준비중입니다.');
        }
    };

    return (
        <>
            <Text1>매물 올리기</Text1>
            <Rectangle2>
                <Imgwaring><img src={Warning} alt="경고" /></Imgwaring>
                <Text2>* 방 등록 시 방 정보와 계정정보(가입된 ID, 이름, 연락처 등)가 노출됩니다.<br />
                       * 허위(계약 완료, 중복 등록, 허위 정보 기재) 등록 및 중개매물, 원룸텔, 쉐어하우스 등록 후 <br />
                       * 적발 시 이용이 제한될 수 있습니다.
                </Text2>
                <Imglightbulb><img src={Light} alt="빛" /></Imglightbulb>
                <Text3>* 다음 단계에서 간편하게 등기부등본을 등록해보세요.</Text3>
            </Rectangle2>
            <Section>
                <Rectangle selected={selectedType === 'apart'} onClick={() => handleSelect('apart')}>
                    <img src={Apart} alt="아파트" />
                    <Text selected={selectedType === 'apart'}>아파트</Text>
                </Rectangle>
                <Rectangle selected={selectedType === 'house'} onClick={() => handleSelect('house')}>
                    <img src={House} alt="빌라,주택" />
                    <Text selected={selectedType === 'house'}>빌라,주택</Text>
                </Rectangle>
            </Section>
            <Section>
                <Rectangle selected={selectedType === 'bed'} onClick={() => handleSelect('bed')}>
                    <img src={Bed} alt="오피스텔" />
                    <Text selected={selectedType === 'bed'}>오피스텔</Text>
                </Rectangle>
                <Rectangle selected={selectedType === 'office'} onClick={() => handleSelect('office')}>
                    <img src={office} alt="상가,사무실" />
                    <Text selected={selectedType === 'office'}>상가,사무실</Text>
                </Rectangle>
            </Section>
        </>
    );
}

export default Uploadmain;