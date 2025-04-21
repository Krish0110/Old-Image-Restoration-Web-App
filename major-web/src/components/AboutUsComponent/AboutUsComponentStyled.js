import styled from "styled-components";

const ContentContainer = styled.div`
  margin-top: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`

const DetailsContainer = styled.div`
  background-color: white;
  margin-top: 40px;
  border-radius: 10px;
  padding: 20px;
  width: 75%;
`
const EachMemberContainer = styled.div`
  background-color: black;
  color: white;
  width: 100%;
  border-radius: 5px;
`
const MembersContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 2fr);
  align-items: center;
  gap: 16px;
  margin-top: 10px;
  margin-bottom: 20px;
`

export {
  ContentContainer,
  DetailsContainer,
  EachMemberContainer,
  MembersContainer
}