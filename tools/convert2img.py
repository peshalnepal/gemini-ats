
from PIL.Image import Image
import pdf2image
import io
import base64
def upload(upload_file):
    #converting pdf to image
    file_images=pdf2image.convert_from_bytes(upload_file.read())
    pdf_parts=[]
    if file_images:
        for image in file_images:
            first_pages=image
            img_byte_arr = io.BytesIO()
            first_pages.save(img_byte_arr, format="JPEG")
            img_byte_arr=img_byte_arr.getvalue()
            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            })
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
