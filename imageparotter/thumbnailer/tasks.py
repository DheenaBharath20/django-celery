import os
from zipfile import ZipFile
from celery import shared_task
from PIL import Image
from django.conf import settings

@shared_task
def make_thumbnails(filepath, thumbnails=[]):
    os.chdir(settings.IMAGEDIR)
    path, file = os.path.splitext(filepath)
    filename, ext = os.path.splitext(file)

    zip_file = f"{filename}.zip"
    results = {'archive_path':f"{settings.MEDIA_URL}images/{zip_file}"}
    try:
        img = Image.open(filepath)
        zipper = ZipFile(zip_file,'w')
        zipper.write(file)
        os.remove(filepath)
        for w,h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w,h))
            thumbnail_file = f'{filename}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)
            os.remove(thumbnail_file)
        img.close()
        zipper.close()
    except IOError as e:
        print(e)


    return results