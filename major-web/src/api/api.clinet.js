import axios from 'axios'

const post = async (url, body, responseType) => {
  console.log("URL from config",url)
  try {
    const response = await axios.post(url, body,{
      responseType: responseType,
    });

    console.log("Image upload response", response);
    return response.data;
 } catch (error) {
  console.log('Error uploading file:', error.message)
 }
};

export {post};