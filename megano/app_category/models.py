from django.core.exceptions import ValidationError
from django.db import models

def category_image_directory_path(instance, filename):
    """
    Creating path for category image
    :param instance: Category object
    :param filename: Name of the file
    :return: Path string
    """

    return 'categories/images/{filename}'.format(
        filename=filename
    )

def validate_svg(value):
    """
    Validate that file is a svg file
    """

    if not value.name.endswith('.svg'):
        raise ValidationError(
            '%(value)s is not an svg file',
            params={'value': value},
        )


class Category(models.Model):
    """
    Category model with foreign key to itself (for creating subcategory)
    """

    title = models.CharField(max_length=50, verbose_name='category')
    image = models.FileField(
        null=True,
        blank=True,
        upload_to=category_image_directory_path,
        verbose_name='category image', validators=[validate_svg])
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               db_index=True,
                               related_name='subcategories')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'