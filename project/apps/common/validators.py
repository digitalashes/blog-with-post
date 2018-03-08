from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:

    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height

    def __call__(self, value, *args, **kwargs):
        errors, image_width, image_height = [], value.width, value.height
        if self.width < image_width:
            errors.append(f'Width should be less than {self.width} px.')
        if self.height < image_height:
            errors.append(f'Height should be  less than {self.height} px.')
        if errors:
            raise ValidationError(errors)
