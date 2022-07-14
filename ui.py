""" 
This file contains code for structure based style transfer and its integration to 
the Web UI using streamlit.io 

"""

# Import necessary modules 
import streamlit as st
from PIL import Image
import base64
import torch
from lib import dataset
from lib.lightning.lightningmodel import LightningModel
import torchvision.transforms as T


# Define the Stylize Image function which performs structure based style transfer
def stylize_image(model, content_image, style_image, content_size=None):
    
    device = next(model.parameters()).device

    content = dataset.content_transforms(content_size)(content_image)
    style = dataset.style_transforms()(style_image)

    content = content.to(device).unsqueeze(0)
    style = style.to(device).unsqueeze(0)

    output = model(content, style)
    
    return output[0].detach().cpu()



#                               Format the background and the webpage design


# Set the title and subtitle of the web UI
st.title('Artisanal Futures Cultural Style Transfer (work in progress)')

st.header('Hello! Welcome to this page! This is nascent work in transfering not just style but cultural style')
st.text('We adopt Chandran et al (2021) to start this work')


#                               Content and Style Images  

# Upload content image 
content_img = st.file_uploader("Choose a content image...", type=["jpg", "jpeg", "png"])
content_file = st.empty()

# Upload style image 
style_img = st.file_uploader("Choose a style image...", type=["jpg", "jpeg", "png"])
style_file = st.empty()


# Check if content file is uploaded
if not content_img:
    content_file.info("Please upload a Content Image")
    
else:
    imgContent = Image.open(content_img)
    st.image(imgContent, caption='Content Image.', use_column_width=True)


# Check if style file is uploaded
if not style_img:
    style_file.info("Please upload a Style Image")
    
else:
    imgStyle = Image.open(style_img)
    st.image(imgStyle, caption='Style Image', use_column_width=True)


extensions = [".png", ".jpeg", ".jpg"]




#                            Perform the stylization    


if content_img is not None and style_img is not None:
    
    # Path to model 
    model_path = './model.ckpt'
    
    # Output Path 
    output_path = './output.png'
        
    # Make Button 
    stylize_button = st.button('Stylize Image')
    
    # Stylize Image
    if stylize_button:
        
        model = LightningModel.load_from_checkpoint(checkpoint_path = model_path)
        model = model.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
        model.eval()

        with torch.no_grad():
            output = stylize_image(model, imgContent, imgStyle)
            
        dataset.save(output, output_path)

        transform = T.ToPILImage()
        output = transform(output)
        
        # Display the stylised image 
        st.write("## Output Image")
        st.image(output, width=400, use_column_width=True)
        