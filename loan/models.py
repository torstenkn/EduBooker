from django.db import models
from django.conf import settings
from datetime import date
from .functions import calculate_current_school_year, calculate_actual_grade, get_school_year_choices

class Borrower(models.Model):
    given_name = models.CharField(max_length=255, help_text="Given name of the borrower.")
    surname = models.CharField(max_length=255, help_text="Surname of the borrower.")
    entry_school_year = models.CharField(max_length=9, choices=get_school_year_choices(), help_text="The school year the borrower started.")
    initial_grade = models.PositiveIntegerField(help_text="Initial grade when the borrower started.")
    borrower_class = models.CharField(max_length=10, help_text="Class of the borrower.")
    inactive = models.BooleanField(default=False, help_text="Set to true if the borrower is inactive.")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional reference to a Django user.")
    
    # Timestamps and user tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='borrowers_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who added this borrower."
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='borrowers_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who last updated this borrower."
    )

    @property
    def actual_grade(self):
        """Calculate the actual grade based on the entry school year, initial grade, and current year."""
        current_school_year = calculate_current_school_year()
        return calculate_actual_grade(self.entry_school_year, self.initial_grade, current_school_year)

    def save(self, *args, **kwargs):
        """Override save method to set the created_by and updated_by fields automatically."""
        if not self.pk:  # New instance
            self.created_by = kwargs.pop('user', None)
        self.updated_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)  # Call the real save method

    def __str__(self):
        return f"{self.given_name} {self.surname}"