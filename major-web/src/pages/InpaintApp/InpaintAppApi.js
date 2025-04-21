//this is api call that will pass image to backend
import * as apiCall from '../../api/api.clinet'
import backendUrl from '../../config'; 

const baseUrl = "http://localhost:8000"
console.log(backendUrl,"from config")

export const postImageApi = async (path, formData) => {
  const responseType = 'json'

  console.log("formdata", Array.from(formData))

  try {
    const response = await apiCall.post(baseUrl + path, formData, responseType);
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.error('Error uploading image:', error.message);
    throw new Error('Image upload failed.');
  }
}