import io
import os
from typing import Optional
from PIL import Image, ImageOps


try:
    from rembg import remove
except Exception as e:
    reove=None



Max_UPload_Mb=15
Allow_Type=["image/png","image/jpeg","image/jpg"]



def byte_to_pil(image_bytes:bytes)-> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGBA")



def pil_to_byte(image:Image.Image,format:str="PNG")-> bytes:
    buffer=io.BytesIO()
    image.save(buffer,format=format)
    return buffer.getvalue()


def remove_background_with_rembg(pil_image:Image.Image)-> Image.Image:
    if remove is None:
        raise RuntimeError("rembg is not installed dear Hassan!")
    input_bytes=pil_to_byte(pil_image,format="PNG")
    output_bytes=remove(input_bytes)
    outer_image=byte_to_pil(output_bytes)
    return outer_image




def composite_with_color(foreground:Image.Image ,bg_image:Image.Image)->Image.Image:
    bg_resized=ImageOps.contain(bg_image.convert("RGBA"),foreground.size)
    if bg_resized.size != foreground.size:
        full_bg=Image.new("RGBA",foreground.size,(0,0,0,255))
        x=(foreground.width -bg_resized.width)// 2
        y=(foreground.height -bg_resized.height)// 2
        full_bg.paste(bg_resized,(x,y))
        bg_resized=full_bg
    
    composed=Image.alpha_composite(bg_resized,foreground)
    return composed.convert("RGB")



def validate_upload(uploaded_file)->Optional[str]:
    if uploaded_file is None:
        return "No file uploaded"
    
    uploaded_file.seek(0 , os.SEEK_END)
    size_mb=uploaded_file.tell() / (1024 *1024)
    uploaded_file.seek(0)
    if size_mb > Max_UPload_Mb :
        return f"File size  is too large{size_mb:.1f}Mb). Max allowed is {Max_UPload_Mb} MB limit"
    
    if uploaded_file.type not in Allow_Type:
        return f"Unsupported file type.{uploaded_file.type} Only PNG and JPEG are allowed"
    
    return None





def prepare_download_image(final_image:Image.Image, output_format:str):
    buffer=io.BytesIO()
    if output_format.startswith("PNG"):
        if final_image.mode != "RGBA":
            save_image=final_image.convert("RGBA")
        else:
            save_image=final_image
        save_image.save(buffer, format="PNG")
        mime="image/png"
        filename="result.png"
    else:
        if final_image.mode =="RGBA":
            flatten =Image.new("RGB", final_image.size,(255,255,255))
            flatten.paste(final_image, mask=final_image.split()[3])
            flatten.save(buffer, format="JPEG", quality=95)
        else:
            final_image.convert("RGB").save(buffer, format="JPEG", quality=95)
        mime="image/jpeg"
        filename="result.jpg"
    return buffer.getvalue(), mime, filename
