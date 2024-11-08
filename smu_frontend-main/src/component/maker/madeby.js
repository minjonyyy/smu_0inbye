import React from 'react';
import styled from 'styled-components';

import Wonho from '../../images/wonho.png';
import Jin from '../../images/jeongjin.png';
import Minjeong from '../../images/minjung.png';
import Euna from '../../images/euna.png';

const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100vh;
  padding-bottom: 50px;
`;

const Title = styled.h1`
  font-family: 'Spoqa Han Sans Neo', sans-serif;
  font-size: 2em;
  color: #333;
  margin: 20px 0;
`;

const TeamContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 80%;
  padding: 20px;
  box-sizing: border-box;
`;

const TeamCard = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  }
`;

const ProfileImage = styled.img`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
`;

const Name = styled.h2`
  font-size: 1.2em;
  color: #333;
  margin: 5px 0;
`;

const Role = styled.p`
  font-size: 0.9em;
  color: #1864AB;
  font-weight: bold;
`;

const Info = styled.p`
  font-size: 0.85em;
  color: #555;
  margin: 5px 0;
  line-height: 1.4;
`;

const Makermain = () => {
  return (
    <MainContainer>
      <Title>Our Team</Title>
      <TeamContainer>
        <TeamCard>
          <ProfileImage src={Jin} alt="정진" />
          <Name>박정진</Name>
          <Role>팀장 - 프론트엔드 / 백엔드</Role>
          <Info>wjdwls7883@naver.com</Info>
          <Info>상명대학교 융합공학대학 지능 · 데이터 융합학부 휴먼지능정보공학 전공</Info>
        </TeamCard>
        <TeamCard>
          <ProfileImage src={Wonho} alt="원호" />
          <Name>정원호</Name>
          <Role>팀원 - 프론트엔드</Role>
          <Info>harry7860@naver.com</Info>
          <Info>상명대학교 융합공학대학 지능 · 데이터 융합학부 휴먼지능정보공학 전공</Info>
        </TeamCard>
        <TeamCard>
          <ProfileImage src={Minjeong} alt="민정" />
          <Name>이민정</Name>
          <Role>팀원 - 백엔드</Role>
          <Info>minjonyyy@naver.com</Info>
          <Info>상명대학교 융합공학대학 지능 · 데이터 융합학부 휴먼지능정보공학 전공</Info>
        </TeamCard>
        <TeamCard>
          <ProfileImage src={Euna} alt="은아" />
          <Name>함은아</Name>
          <Role>팀원 - 백엔드</Role>
          <Info>hamea1209@naver.com</Info>
          <Info>상명대학교 융합공학대학 지능 · 데이터 융합학부 휴먼지능정보공학 전공</Info>
        </TeamCard>
      </TeamContainer>
    </MainContainer>
  );
}

export default Makermain;
