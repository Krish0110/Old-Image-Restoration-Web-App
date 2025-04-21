import React, {useRef, useState} from 'react'
import Button from '../Button/Button';
import {ImageDisplay, ImagesConatiner, InpaintAppContainer, InpaintAppPopUpBox, ButtonHolder, InpaintAppQueryBox} from './InpaintAppComponentStyled';
import { postImageApi } from '../../pages/InpaintApp/InpaintAppApi';
import DrawingCanvas from './MaskDrawingCanvasComponent';

const InpaintAppComponent = () => {
  const fileInputRef = useRef(null);
  const [selectedImageUrl, setSelectedImageUrl] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [binaryMaskOutputImgaeUrl, setBinaryMaskOutputImageUrl] = useState(null);
  const [resizedInputImageUrl, setResizedInputImageUrl] = useState(null);
  const [inpaintedImageurl, setInpaintedImageUrl] = useState(null);
  const [finalOutputImageUrl, setFinalImageOutputUrl] = useState(null);

  const [isImageUploaded, setIsImageUploaded] = useState(false)
  const [showDrawMaskPopup, setShowDrawMaskPopup] = useState(false);
  const [showMask, setShowMask] = useState(true);
  const [showColor, setShowColor] = useState(false);
  const [showUploadButton, setShowUploadButton] = useState(true);
  const [originalImageSize, setOriginalImageSize] = useState({ width: null, height: null });


  const handleButtonClicked = async () => {
    const formData = new FormData();
    formData.append('image', selectedImage);
    if (!isImageUploaded) {
      fileInputRef.current.click();
    } else {
      try {
        const response = await postImageApi('/api/detect-damage/', formData);
        console.log("Response from component", response);

        console.log('Resized Input:', response.resized_input);
        console.log('Binary Mask:', response.binary_mask);

        const resizedInputImageDataUrl = `data:image/png;base64,${response.resized_input}`;
        const binaryMaskDataUrl = `data:image/png;base64,${response.binary_mask}`;

        setResizedInputImageUrl(resizedInputImageDataUrl);
        setBinaryMaskOutputImageUrl(binaryMaskDataUrl);
        setIsImageUploaded(false);
        setShowUploadButton(false);
      } catch (error) {
        console.error('Error during image processing:', error);
        alert('Failed to process the image. Please try again.');
      }
    }
  }

  const handleFileChange = (event) =>{
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
      setSelectedImageUrl(URL.createObjectURL(file));
      setSelectedImage(file);
      setIsImageUploaded(true);

      const img = new Image();
      img.onload = () => {
        setOriginalImageSize({ width: img.naturalWidth, height: img.naturalHeight });
        console.log('Original Image Size:', img.naturalWidth, img.naturalHeight);
      };
      img.src = URL.createObjectURL(file);
    } else {
      alert("Please select a valid image file.")
    }
  }

  const handleDrawMask = () => {
    setShowDrawMaskPopup(true);
  };  

  const base64ToBlob = (base64Data, contentType = 'image/png') => {
    const byteCharacters = atob(base64Data.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length).fill().map((_, i) => byteCharacters.charCodeAt(i));
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
  };

  const handleContinueWithGeneratedMask = async () => {
    const resizedInputBlob = base64ToBlob(resizedInputImageUrl);
    const binaryMaskBlob = base64ToBlob(binaryMaskOutputImgaeUrl);

    const formData = new FormData();
    formData.append('input_image', resizedInputBlob, 'resized_input.png');
    formData.append('mask_image', binaryMaskBlob, 'mask.png');
  
    try {
      const response = await postImageApi('/api/inpaint-image/', formData);
      console.log('Inpainting response:', response);
      
      const inpaintedImageDataUrl = `data:image/png;base64,${response.inpainted_image}`;

      setInpaintedImageUrl(inpaintedImageDataUrl);

      // Example: log first 100 chars
      console.log('Inpainted Image:', inpaintedImageDataUrl.slice(0, 100));
    } catch (error) {
      console.error('Inpainting failed:', error.message);
    }

    setShowMask(false);
    setShowColor(true)
  };

  const handleAddColor = async() => {
    const inpaintedImageBlob = base64ToBlob(inpaintedImageurl);

    const formData = new FormData();
    formData.append('inpainted_image', inpaintedImageBlob, 'inpainted_image.png');
    formData.append('width', originalImageSize.width);
    formData.append('height', originalImageSize.height);
  
    try {
      const response = await postImageApi('/api/add-color/', formData);
      console.log('Inpainting response:', response);
      
      const finalOutputImageDataUrl = `data:image/png;base64,${response.final_image_output}`;

      setFinalImageOutputUrl(finalOutputImageDataUrl)

      // Example: log first 100 chars
      console.log('Final Image:', finalOutputImageDataUrl.slice(0, 100));
    } catch (error) {
      console.error('Inpainting failed:', error.message);
    }
    setShowColor(false)
    setShowUploadButton(true)
  }

  const handleContinueWithoutColor = async() => {
    const inpaintedImageBlob = base64ToBlob(inpaintedImageurl);

    const formData = new FormData();
    formData.append('inpainted_image', inpaintedImageBlob, 'inpainted_image.png');
    formData.append('width', originalImageSize.width);
    formData.append('height', originalImageSize.height);
  
    try {
      const response = await postImageApi('/api/improve-reso/', formData);
      console.log('Inpainting response:', response);
      
      const finalOutputImageDataUrl = `data:image/png;base64,${response.final_image_output}`;

      setFinalImageOutputUrl(finalOutputImageDataUrl)

      // Example: log first 100 chars
      console.log('Final Image:', finalOutputImageDataUrl.slice(0, 100));
    } catch (error) {
      console.error('Inpainting failed:', error.message);
    }
    setShowColor(false)
    setShowUploadButton(true)
  }

  return (
    <>
      <InpaintAppContainer>
        <h3>{ isImageUploaded ? "Selected Image:" : "Upload your image to restore" }</h3>
        <ImagesConatiner>
          {selectedImageUrl && (
            <ImageDisplay >
              <img
                src={selectedImageUrl}
                alt="Uploaded Preview"
                style={{ maxWidth: '150px', height: 'auto', borderRadius: '10px' }}
              />
            </ImageDisplay>
          )}
          {showMask && (
            <>
              {resizedInputImageUrl && (
                <ImageDisplay>
                  <img
                    src={resizedInputImageUrl}
                    alt="Resized Input"
                    style={{ maxWidth: '150px', height: 'auto', borderRadius: '10px' }}
                  />
                </ImageDisplay>
              )}
              {binaryMaskOutputImgaeUrl && (
                <ImageDisplay>
                  <img
                    src={binaryMaskOutputImgaeUrl}
                    alt="Binary Mask Output"
                    style={{ maxWidth: '150px', height: 'auto', borderRadius: '10px' }}
                  />
                </ImageDisplay>
              )}
            </>
          )}

          {inpaintedImageurl && (
            <ImageDisplay >
              <img
                src={inpaintedImageurl}
                alt="Inpainted output"
                style={{ maxWidth: '150px', height: 'auto', borderRadius: '10px' }}
              />
            </ImageDisplay>
          )}

          {finalOutputImageUrl && (
            <ImageDisplay >
              <img
                src={finalOutputImageUrl}
                alt="Final output"
                style={{ maxWidth: '150px', height: 'auto', borderRadius: '10px' }}
              />
            </ImageDisplay>
          )}      
        </ImagesConatiner>

        {showUploadButton && 
          <Button title={ isImageUploaded ? "Create Mask" : "Upload" } onClick={handleButtonClicked}  />
        }

        <input 
          type="file"
          ref={fileInputRef}
          style={{display:'none'}}
          accept="image/*"
          onChange={handleFileChange}
        />
      </InpaintAppContainer>
      {(resizedInputImageUrl && binaryMaskOutputImgaeUrl && showMask) &&(
          <InpaintAppQueryBox>
            <p>Do you want to draw you mask yourself or continue with the generated mask?</p>
            <ButtonHolder>
              <Button title={"Draw the mask"} onClick={handleDrawMask}/>
              <div></div>
              <Button title={"Continue with generated mask"} onClick={handleContinueWithGeneratedMask}/>
            </ButtonHolder>
          </InpaintAppQueryBox>
      )}

      {(inpaintedImageurl && showColor) && 
        <InpaintAppQueryBox>
          <p>Do you want to add color to your image?</p>
          <ButtonHolder>
            <Button title={"Add Color"} onClick={handleAddColor}/>
            <div></div>
            <Button title={"Continue Without Color"} onClick={handleContinueWithoutColor}/>
          </ButtonHolder>
        </InpaintAppQueryBox>
      }

      {showDrawMaskPopup && (
        <InpaintAppPopUpBox>
          <DrawingCanvas
            imageUrl={resizedInputImageUrl}
            width={512}
            height={512}
            onClose={() => setShowDrawMaskPopup(false)}
            onInpainted={(imgUrl) => {
              setInpaintedImageUrl(imgUrl);
              setShowDrawMaskPopup(false);
              setShowMask(false);
              setShowColor(true);
            }}
          />
        </InpaintAppPopUpBox>
      )}
    </>
  )
}

export default InpaintAppComponent;