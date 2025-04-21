import React from 'react'
import {NavLink} from 'react-router-dom'
import { HeaderContainer, LinkContainer } from './HeaderStyled'


const Header = () => {
  return (
    <HeaderContainer>
      {/* <div>LOGO</div> */}
      <div>
        <LinkContainer>
          <NavLink 
            to="/" 
            exact activeClassName="selected" 
          >
            Home
          </NavLink>

          <NavLink 
            to="/about-us" 
            activeClassName="selected" 
          >
            About Us
          </NavLink>

          <NavLink
            to="/project-info"
            activeClassName="selected"
          >
            Project Info
          </NavLink>

          <NavLink
            to="/inpaint-app"
            activeClassName="selected"
          >
            Restore Image
          </NavLink>
        </LinkContainer>
      </div>
    </HeaderContainer>
  )
}

export default Header