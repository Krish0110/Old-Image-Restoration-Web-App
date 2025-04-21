import styled from 'styled-components'

const ButtonStyled = styled.button`
    background-color: black;
    width: auto;
    height: 40px;
    border: solid 1px black;
    color: #F0D78C;
    padding: 10px 20px;
    cursor: pointer;
    text-align: center;
    border-radius: 10px;
    font-size: 15px;

    &:hover {
      background-color: #F0D78C;
      color: black;
      transition: background-color 0.3s;
    }

    &:disabled {
    opacity: 0.5;
    }
`

export default ButtonStyled