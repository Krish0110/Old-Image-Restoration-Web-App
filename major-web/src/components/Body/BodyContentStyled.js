import styled from 'styled-components';

const BodyContentContainer = styled.div`
  z-index: 100;
  position: absolute; 
  margin-top: 50px;
  top: 50%;
  left: 50%;
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

const BodyHeader = styled.h1`
  font-size: 3rem;
`

const BodyText = styled.p`
  font-size: 1.5rem;
`
const BodyAnchorTag = styled.a`
  color: white;
  font-size: 1.2rem;
  text-decoration: underline;
`

export { 
  BodyContentContainer,
  BodyHeader,
  BodyText,
  BodyAnchorTag
};
