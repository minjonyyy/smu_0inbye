import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const ChatListContainer = styled.div`
  padding: 20px;
  display: flex;
  flex-direction: column;
`;

const ChatItem = styled.div`
  padding: 10px;
  margin: 10px 0;
  background-color: #f0f0f0;
  border-radius: 10px;
  cursor: pointer;

  &:hover {
    background-color: #e0e0e0;
  }
`;
const Server = process.env.REACT_APP_BACK_SERVER;

const ChatList = () => {
    const [chatRooms, setChatRooms] = useState([]);
    const navigate = useNavigate();
  
    useEffect(() => {
      const fetchChatRooms = async () => {
        const token = localStorage.getItem('access_token');
        try {
          const response = await axios.get(`${Server}/chat/list/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("채팅방 리스트:", response.data);
          setChatRooms(response.data);
        } catch (error) {
          console.error("Error:", error.response ? error.response.data : error.message);
        }
      };
      fetchChatRooms();
    }, []);
  
    return (
      <ChatListContainer>
        <h2>채팅방 목록</h2>
        {chatRooms.map((room) => {
          const otherParticipantEmail = room.participant_email;
          const otherUsername = otherParticipantEmail.split('@')[0];

          return (
            <ChatItem
              key={room.id}
              onClick={() => {
                console.log(`${otherUsername}과의 채팅방 접속`);
                navigate(`/chat/${otherUsername}`);
              }}
            >
              {`${otherUsername}`}
            </ChatItem>
          );
        })}
      </ChatListContainer>
    );
  };
  
  export default ChatList;