import React from 'react'
import Body from '../../components/Body/Body'
import InpaintAppComponent from '../../components/InpaintAppComponent/InpaintAppComponent';

const InpaintApp = () => {
  return(
    <Body children={<InpaintAppComponent />} />
  );
};

export default InpaintApp;