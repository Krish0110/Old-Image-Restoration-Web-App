import React from 'react'
import { BodyHeader, BodyContentContainer, BodyText, BodyAnchorTag } from './BodyContentStyled'

const BodyContent = () => {
  return (
    <BodyContentContainer>
      <BodyHeader>
        Revive Your Old Memories with AI!
      </BodyHeader>
      <BodyText>
        Automatically detect and restore damaged photos with cutting-edge AI technology
      </BodyText>
      <BodyAnchorTag href="/inpaint-app" >
        Try Now
      </BodyAnchorTag>
    </BodyContentContainer>
  )
}

export default BodyContent