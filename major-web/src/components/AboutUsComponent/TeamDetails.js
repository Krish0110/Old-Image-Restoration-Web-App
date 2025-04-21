import React from 'react'
import { DetailsContainer, EachMemberContainer, MembersContainer } from './AboutUsComponentStyled'

const TeamDetails = () => {
  return (
    <DetailsContainer style={{ marginBottom: '40px' }}>
      <h3>TeamDetails</h3>
      <MembersContainer>
        <EachMemberContainer>
          <p>Aakrit Dangol</p>
          <p>077bct002</p>
          <p>Email</p>
        </EachMemberContainer>
        <EachMemberContainer>
          <p>Biraj Kumar Karanjit</p>
          <p>077bct020</p>
          <p>Email</p>
        </EachMemberContainer>
        <EachMemberContainer>
          <p>Krishala Prajapati</p>
          <p>077bct038</p>
          <p>Email</p>
        </EachMemberContainer>
      </MembersContainer>
    </DetailsContainer>
  )
}

export default TeamDetails