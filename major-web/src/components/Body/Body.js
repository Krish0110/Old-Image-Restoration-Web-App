import React from 'react'
import { BodyBgImageContainer, ContentContainer, ImageOverlay } from './BodyStyled'

const Body = ({children={}}) => {
  return (
    <BodyBgImageContainer>
      <ImageOverlay/>
      <ContentContainer>
        {children}
      </ContentContainer>
    </BodyBgImageContainer>
  )
}

export default Body