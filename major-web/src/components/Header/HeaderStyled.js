import styled from 'styled-components'

const HeaderContainer = styled.div`
  width: 100%;
  height: 100px;
  background-color: rgba(51, 51, 57, 0.75);
  display: flex;
  justify-content: space-around;
  align-items: center;
  color: white;
  position: fixed;
  z-index: 5;
  border-bottom: solid 1px white;
`

const LinkContainer = styled.nav`
  display: flex;
  gap: 20px;
  font-size: 20px;
  
  a{
    text-decoration: none;
    color: #D4AF37;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 5px;
    transition: all 0.3s ease;

    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
      color: #f0a500; 
    }

    &:active {
      transform: scale(0.95); 
    }
  }

  .selected {
    text-decoration: underline;
  }
`

export {
  HeaderContainer,
  LinkContainer,
}