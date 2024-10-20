from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from .functions import validate_isbn13

class MediaCategory(models.Model):
    code = models.CharField(
        max_length=3, 
        unique=True, 
        help_text="Unique code for the category, e.g., LTB."
    )
    name = models.CharField(
        max_length=255, 
        help_text="Category name, e.g., 'Sachbücher Naturwissenschaften Tiere Pflanzen'."
    )
    colour = models.CharField(
        max_length=50, 
        help_text="Colour name for the category, e.g., 'green'."
    )
    colour_code = models.CharField(
        max_length=7, 
        validators=[RegexValidator(
            regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$', 
            message='Enter a valid hex colour code (e.g., #000000 for black).')],
        help_text="Hex colour code representing the colour, e.g., '#ffffff' for white."
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Optional description of the category."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='categories_created', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who created the category."
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='categories_updated', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who last updated the category."
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Media Category'
        verbose_name_plural = 'Media Categories'

    def __str__(self):
        return f'{self.code} - {self.name}'
    

class MediaType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the media type, e.g., Book, Game, Music CD.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='media_types_created', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who created this media type."
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='media_types_updated', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who last updated this media type."
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Media Type'
        verbose_name_plural = 'Media Types'

    def __str__(self):
        return self.name

class LibrarySite(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Unique name of the library site.")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the library site.")
    opening_hours = models.TextField(blank=True, null=True, help_text="Opening hours for the library site.")
    is_active = models.BooleanField(default=True, help_text="Set to false if the site is deactivated.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='sites_created', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who created the site."
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='sites_updated', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who last updated the site."
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Library Site'
        verbose_name_plural = 'Library Sites'

    def __str__(self):
        return self.name
    

class Media(models.Model):
    title = models.CharField(max_length=255, help_text="Full title of the media.")
    authors = models.CharField(max_length=255, blank=True, null=True, help_text="Authors of the media (optional).")
    site = models.ForeignKey(LibrarySite, on_delete=models.CASCADE, help_text="Library site where this media is stored.")
    category = models.ForeignKey(MediaCategory, on_delete=models.CASCADE, help_text="Media category (e.g., Fiction, Science).")
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE, help_text="Type of media (e.g., Book, Game, Music CD).")
    legacy_media_number = models.CharField(max_length=4, blank=True, null=True, help_text="Legacy media number (0001-9999).")
    media_number = models.CharField(max_length=10, unique=True, help_text="Automatically generated media number.")
    isbn13 = models.CharField(max_length=13, blank=True, null=True, help_text="ISBN13 number (optional).")
    acquisition_date = models.DateField(blank=True, null=True, help_text="Acquisition date of the media (optional).")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price of the media (optional).")
    left_library_date = models.DateField(blank=True, null=True, help_text="Date when the media left the library (optional).")
    comments = models.TextField(blank=True, null=True, help_text="Additional comments (optional).")
    publisher = models.CharField(max_length=255, blank=True, null=True, help_text="Publisher of the media (optional).")
    publishing_date = models.DateField(blank=True, null=True, help_text="Publishing date of the media (optional).")
    short_description = models.TextField(blank=True, null=True, help_text="Short description of the media (optional).")
    media_file = models.FileField(upload_to='media_files/', blank=True, null=True, help_text="Reference to uploaded media (optional).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='media_created', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who created this media."
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='media_updated', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="User who last updated this media."
    )

    class Meta:
        ordering = ['media_number']
        verbose_name = 'Media'
        verbose_name_plural = 'Media'

    def clean(self):
        """
        Custom validation for the Media model.
        Validates the ISBN-13 number if it is provided.
        Ensures media_number is set based on legacy_media_number or auto-incremented.
        """
        super().clean()  # Call the parent class's clean method

        # Validate ISBN-13 if provided
        if self.isbn13 and not validate_isbn13(self.isbn13):
            raise ValidationError("The ISBN-13 number is not valid.")

    def save(self, *args, **kwargs):
        """
        Override save method to set the media_number automatically.
        """
        # If legacy_media_number is provided, use it as media_number
        if self.legacy_media_number:
            self.media_number = f"{self.category.code}{self.legacy_media_number.zfill(4)}"
        else:
            # Find the highest media_number in the same category
            last_media = Media.objects.filter(category=self.category).order_by('-media_number').first()

            if last_media:
                # Extract the numeric part from the media_number and increment it
                last_number = int(last_media.media_number[len(self.category.code):])
                new_number = last_number + 1
            else:
                new_number = 1  # Start with 0001 if no media in this category

            self.media_number = f"{self.category.code}{str(new_number).zfill(4)}"
        
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return f"{self.media_number} - {self.title}"