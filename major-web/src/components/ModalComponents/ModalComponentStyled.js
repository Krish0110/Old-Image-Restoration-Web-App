import styled from 'styled-components';

const ModalContainer = styled.div`
  z-index: 100;
  position: absolute; 
  margin-top: 50px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

`;

const ModalContentContainer = styled.div`
  background-color: black;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
`
const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #333;
  &:hover {
    color: #f00;
  }
`


export {
  ModalContainer,
  ModalContentContainer,
  CloseButton
}

