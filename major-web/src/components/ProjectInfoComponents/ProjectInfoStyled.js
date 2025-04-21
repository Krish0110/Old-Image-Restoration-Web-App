import styled from 'styled-components';

const MainContainer = styled.div`
  z-index: 100;
  position: absolute; 
  margin-top: 50px;
  top: 50%;
  left: 50%;
  width: 50%;
  transform: translate(-50%, -50%);
  color: #D4AF37;
  text-align: center;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 1);
  background-color: rgba(10, 10, 10, 0.3);
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
`
const TopicsContainer = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
`

const EachTopicContainer = styled.button`
  background-color: white;
  color: black;
  border-radius: 5px;
  margin-bottom: 10px;
  padding: 10px;
  width: 50%;
`

export { 
  MainContainer,
  EachTopicContainer,
  TopicsContainer
};
