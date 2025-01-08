from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(image):

    # Check if the file extension is valid
    if not image.name.endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError('Invalid file type. Please upload a JPEG, PNG file.')

    # Check if the file size is valid (maximum 2MB)
    if image.size > 4 * 1024 * 1024:
        raise ValidationError('File size too large. Maximum file size allowed is 4MB.')

    # Check if the dimensions are valid (maximum 500x500 pixels)
    width, height = get_image_dimensions(image)
    if width > 500 or height > 500:
        raise ValidationError('Image dimensions too large. Maximum dimensions allowed are 500x500 pixels.')
