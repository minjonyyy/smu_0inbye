import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 80vh;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
`;

const MessageList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  margin-bottom: 10px;
`;

const MessageGroup = styled.div`
  display: flex;
  flex-direction: column;
  align-items: ${({ isSender }) => (isSender ? "flex-end" : "flex-start")};
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 10px;
  background-color: ${({ isSender }) => (isSender ? "#dcf8c6" : "#ffffff")};
  color: #333;
  border-radius: 10px;
  border-bottom-${({ isSender }) => (isSender ? "right" : "left")}-radius: 0;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.15);
  margin: 5px 0;
`;

const DateDivider = styled.div`
  display: flex;
  justify-content: center;
  color: #888;
  font-size: 0.85rem;
  margin: 10px 0;
`;

const Timestamp = styled.span`
  font-size: 0.75rem;
  color: #888;
  margin-top: 5px;
`;

const InputContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
`;

const SendButton = styled.button`
  padding: 10px;
  border: none;
  background-color: #4caf50;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #45a049;
  }
`;
const Server = process.env.REACT_APP_BACK_SERVER;

const ChatRoom = () => {
  const { username, roomId: paramRoomId } = useParams(); 
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [roomId, setRoomId] = useState(null);
  const messageListRef = useRef(null);
  const senderEmail = localStorage.getItem('userEmail');
  const navigate = useNavigate();

  // 채팅방 존재 여부 확인 및 설정 로직
  useEffect(() => {
    const fetchOrCreateRoom = async () => {
      const token = localStorage.getItem('access_token');
      try {
          let response;

          if (username) {
              const url = `${Server}/chat/check-room/${username}/`;
              response = await axios.get(url, { headers: { Authorization: `Bearer ${token}` } });
  
              if (response.data.room_exists) {
                  // 기존 방이 존재하는 경우 새 방 생성 대신 해당 방 사용
                  setRoomId(response.data.id);
                  console.log("기존 채팅방이 존재합니다.roomID:", response.data.id);
              } else {
                  // 기존 방이 없을 때만 새 방 생성
                  const createUrl = `${Server}/chat/create-room/${username}/`;
                  const createResponse = await axios.post(createUrl, {}, { headers: { Authorization: `Bearer ${token}` } });
                  setRoomId(createResponse.data.id);
                  console.log("새로운 채팅방을 생성합니다. roomID:", createResponse.data.id);
              }
          }
      } catch (error) {
          if (error.response && error.response.data.detail) {
              alert(error.response.data.detail);
              console.log("Error detail:", error.response.data.detail);
              navigate(-1);
          } else {
              console.error("채팅방 조회 오류:", error);
          }
      }
    };
  
  
  
    if (username && username === senderEmail) {
      alert("자기 자신과의 채팅방은 생성할 수 없습니다.");
      navigate(-1);
      return;
    }
  
    fetchOrCreateRoom();
  }, [username, paramRoomId, senderEmail, navigate]);

  // 메시지 불러오기 함수
  const fetchMessages = async () => {
    if (!roomId) return;

    const token = localStorage.getItem('access_token');
    try {
      const response = await axios.get(
        `${Server}/chat/messages/${roomId}/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      //console.log("Messages fetched:", response.data); 
      setMessages(response.data.map((msg) => ({
        ...msg,
        sender: msg.sender_email || "알 수 없는 사용자",
        timestamp: new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        date: new Date(msg.timestamp).toLocaleDateString()
      })));
    } catch (error) {
      console.error("기존 메시지 불러오기 오류:", error);
    }
  };

  // roomId 변경 시 메시지 로드
  useEffect(() => {
    fetchMessages();
  }, [roomId]);

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  // WebSocket 연결
  useEffect(() => {
    if (roomId) {
      const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomId}/`);

      ws.onopen = () => console.log("WebSocket 연결 성공!");

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // console.log("Message received:", data); 
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            sender: data.sender_email || "알 수 없는 사용자",
            message: data.message,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            date: new Date().toLocaleDateString()
          }
        ]);
      };

      ws.onclose = () => console.log("WebSocket 연결이 닫혔습니다.");
      ws.onerror = (error) => console.error("WebSocket 오류:", error);

      setSocket(ws);

      return () => ws.close();
    }
  }, [roomId]);

  // 메시지 전송
  const sendMessage = async () => {
    if (messageInput.trim() === '' || !roomId) return;

    const token = localStorage.getItem('access_token');

    try {
      await axios.post(
        `${Server}/chat/send/${roomId}/`,
        { message: messageInput },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      console.log("Message sent:", messageInput); 
      setMessageInput('');
    } catch (error) {
      console.error("메시지 전송 오류:", error);
    }
  };

  return (
    <ChatContainer>
      <h2>{`${username}님과의 채팅방`}</h2>
      <MessageList ref={messageListRef}>
        {messages.map((msg, index) => (
          <React.Fragment key={index}>
            {index === 0 || msg.date !== messages[index - 1].date ? (
              <DateDivider>{msg.date}</DateDivider>
            ) : null}
            <MessageGroup isSender={msg.sender === senderEmail}>
              <MessageBubble isSender={msg.sender === senderEmail}>
                {msg.message}
              </MessageBubble>
              <Timestamp>{msg.timestamp}</Timestamp>
            </MessageGroup>
          </React.Fragment>
        ))}
      </MessageList>
      <InputContainer>
        <Input
          type="text"
          value={messageInput}
          onChange={(e) => setMessageInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') sendMessage(); }}
          placeholder="메시지를 입력하세요"
        />
        <SendButton onClick={sendMessage}>전송</SendButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatRoom;