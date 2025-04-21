import React from 'react'
import Body from '../components/Body/Body'
import ProjectInfoComponent from '../components/ProjectInfoComponents/ProjectInfoComponent'

const ProjectInfo = () => {
  return (
    <div>
      <Body children={<ProjectInfoComponent />} />
    </div>
  )
}

export default ProjectInfo;