import React from 'react'
import { CloseButton, ModalContainer, ModalContentContainer } from './ModalComponentStyled';

const ModalComponent = ({visible,title, description, onClose}) => {
  if(!visible){
    return null;
  } else {
    return(
      <ModalContainer>
        <CloseButton onClick={onClose}>✖</CloseButton> {/* Cross button */}
        <ModalContentContainer>
          <h3>{title}</h3>
          <h5>{description}</h5>
        </ModalContentContainer>
      </ModalContainer>
    )
  }
}

export default ModalComponent;