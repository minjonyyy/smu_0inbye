import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
`;

const Title = styled.h1`
  text-align: center;
  margin-bottom: 20px;
  color: #19254D;
`;

const Card = styled.div`
  border: none;
  margin-bottom: 20px;
`;

const CardHeader = styled.div`
  background: #19254D;
  color: white;
  padding: 10px 15px;
  border-radius: 5px 5px 0 0;
`;

const CardBody = styled.div`
  padding: 15px;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 5px 5px;
`;

const ListGroup = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const ListGroupItem = styled.li`
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
  &:last-child {
    border-bottom: none;
  }
`;

const Icon = styled.span`
  vertical-align: middle;
  margin-right: 5px;
  color: #19254D;
`;

const DownloadLink = styled.a`
  display: inline-block;
  margin-top: 10px;
  background: #28a745;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 14px;
  &:hover {
    background: #218838;
  }
`;

const tips = [
  {
    icon: 'info', // info 아이콘으로 변경
    title: '부동산 직거래 과정',
    content: [
      {
        subTitle: '1. 매물 확인',
        subContent: [
          '매물 가격이 부동산 주변 시세 대비 너무 낮거나 높지는 않은지 확인',
          '등기부등본 열람하여, 내용 확인',
        ],
      },
      {
        subTitle: '2. 가격 협상',
        subContent: [],
      },
      {
        subTitle: '3. 계약서 작성',
        subContent: [
          '표준 계약서 사용',
          '임차인 또는 매도자 측에서 2부 출력',
          '합의된 매매 대금, 계약금, 중도금, 잔금의 금액과 날짜 기입',
        ],
        pdf: 'contract.pdf',  // 여기서 PDF 파일 경로를 설정
      },
      {
        subTitle: '4. 계약금 입금',
        subContent: [
          '매도자와 매수자의 성명과 주민등록번호',
          '물건의 종류와 위치',
          '거래가격과 계약금 금액',
          '입금일과 입금방법',
          '날짜와 서명',
        ],
      },
      {
        subTitle: '5. 실거래가 신고',
        subContent: [
          '부동산 매매계약서',
          '매도자와 매수자의 주민등록증 사본',
          '매도자와 매수자의 인감증명서',
          '매도자와 매수자의 인감도',
          '소유권 이전 신고서',
        ],
      },
      {
        subTitle: '6. 중도금 입금',
        subContent: [],
      },
      {
        subTitle: '7. 잔금 입금',
        subContent: [],
      },
      {
        subTitle: '8. 소유권 이전 등기',
        subContent: [],
      },
    ],
  },
];

const Tips = () => (
  <Container>
    <Title>부동산 직거래 팁</Title>
    {tips.map((tip, index) => (
      <Card key={index}>
        <CardHeader>
          <Icon className="material-icons">{tip.icon}</Icon> {tip.title}
        </CardHeader>
        <CardBody>
          <ListGroup>
            {tip.content.map((item, idx) => (
              <ListGroupItem key={idx}>
                <h5>
                  <Icon className="material-icons">{tip.icon}</Icon> {item.subTitle}
                </h5>
                {item.subContent.length > 0 && (
                  <ul>
                    {item.subContent.map((subItem, subIdx) => (
                      <li key={subIdx}>{subItem}</li>
                    ))}
                  </ul>
                )}
                {item.pdf && (
                  <DownloadLink href={item.pdf} download="표준계약서.pdf">
                    표준 계약서 다운로드
                  </DownloadLink>
                )}
              </ListGroupItem>
            ))}
          </ListGroup>
        </CardBody>
      </Card>
    ))}
  </Container>
);

export default Tips;