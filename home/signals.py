from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
import os, fitz
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


@receiver(post_save, sender=Book)
def post_save_post(sender, instance, created, **kwargs):

        if instance.thumbnail:
            return
        
        pdf_path = instance.pdf_file.path
        doc = fitz.open(pdf_path)
        page = doc.load_page(0) 
        pix = page.get_pixmap()

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.thumbnail((300,400))
        
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=85)
        image_io.seek(0)

        thumbnail_name = f'{os.path.splitext(os.path.basename(pdf_path))[0]}_thumbnail.jpg'
        instance.thumbnail.save(thumbnail_name, InMemoryUploadedFile(image_io, None, 'thumbnail.jpg', 'image/jpeg', image_io.tell(), None), save=True)
        instance.save()
        return