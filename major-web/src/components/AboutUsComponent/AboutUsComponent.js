import React from 'react'
import TeamDetails from './TeamDetails'
import { ContentContainer, DetailsContainer } from './AboutUsComponentStyled'

const AboutUsComponent = () => {
  return (
    <ContentContainer>
      <DetailsContainer>
        <h3>Project Overview</h3>
        <p>Our project focuses on reviving old, damaged photos using advanced AI techniques. With this tool, users can restore torn, scratched, or faded images, preserving their precious memories for years to come.</p>
      </DetailsContainer>
      <DetailsContainer>
        <h3>Purpose and Inspiration</h3>
        <p>We were inspired by the timeless value of old photographs and the need to preserve them in the digital age. Our goal is to simplify the process of photo restoration and make it accessible to everyone.</p>
      </DetailsContainer>
      <TeamDetails/>
    </ContentContainer>
  )
}

export default AboutUsComponent