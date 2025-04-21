import React from 'react'
import ButtonStyled from './ButtonStyled'

const Button = ({title,onClick}) => {
  return (
    <ButtonStyled onClick = {onClick} >
      {title}
    </ButtonStyled>
  )
}

export default Button;