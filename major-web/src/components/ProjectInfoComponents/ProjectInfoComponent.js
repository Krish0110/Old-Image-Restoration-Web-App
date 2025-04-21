import React, { useState } from 'react'
import { EachTopicContainer, MainContainer, TopicsContainer } from './ProjectInfoStyled'
import ModalComponent from '../ModalComponents/ModalComponent'
import reportDetails from '../../data/reportDetails.json'

const ProjectInfoComponent = () => {
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState({title: '', description: ''});

  const handleClick = (topic) => {
    setModalContent({title: topic.title, description: topic.description})
    setShowModal(true)
  }

  return (
    <>
      <MainContainer>
        <div>
          <h3>
            Major Project
          </h3>
          <h1>
            IMAGE INPAINTING OF OLD PHOTOS USING GAN
          </h1>
        </div>
        <TopicsContainer>
          {reportDetails.map((reportDetail) => (
            <EachTopicContainer key={reportDetail.id} onClick={() => handleClick(reportDetail)}>
              {reportDetail.title}
            </EachTopicContainer>
          ))}
        </TopicsContainer>
      </MainContainer>
      <ModalComponent 
        visible={showModal}
        title={modalContent.title}
        description={modalContent.description}
        onClose={() => setShowModal(false)}
      />
    </>
  )
}

export default ProjectInfoComponent