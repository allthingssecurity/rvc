import cloudinary.uploader
          
cloudinary.config( 
  cloud_name = "djepbidi1", 
  api_key = "531731913696587", 
  api_secret = "_5ePxVQEECYYOukhSroYXq7eKL0" 
)

cloudinary.uploader.upload("test.mp3", 
  public_id = "test")