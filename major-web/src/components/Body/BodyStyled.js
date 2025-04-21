import styled from 'styled-components'
import backgroundImage from '../../assests/background.png';

const BodyBgImageContainer = styled.div`
  position: fixed; 
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-image: url('${backgroundImage}');
  background-size: cover;
  background-position: center;
  filter: brightness(75%) sepia(30%);
  opacity: 0.8;
  z-index: -1;
`
const ContentContainer = styled.div`
  position: relative;
  width: 100%;
  height: 100vh; /* Full viewport height */
  overflow-y: auto; /* Enable vertical scrolling */
  z-index: 1; /* Ensure it is above the background */
`;

const ImageOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(100,100, 100, 0.4);
  z-index: 0;
  pointer-events: none;
`

export {
  BodyBgImageContainer,
  ImageOverlay,
  ContentContainer,
}