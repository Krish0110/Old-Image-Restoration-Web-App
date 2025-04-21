import React from 'react'
import Body from '../components/Body/Body'
import BodyContent from '../components/Body/BodyContent'

const Home = () => {
  return (
    <div>
      <Body children={<BodyContent />} />
    </div>
  )
}

export default Home