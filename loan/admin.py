from django.contrib import admin
from .models import Borrower
from .functions import get_school_year_choices

class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('given_name', 'surname', 'entry_school_year', 'initial_grade', 'actual_grade', 'borrower_class', 'inactive', 'user', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('given_name', 'surname', 'entry_school_year', 'borrower_class')
    list_filter = ('inactive', 'borrower_class', 'entry_school_year')

    readonly_fields = ('actual_grade', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'entry_school_year':
            kwargs['choices'] = get_school_year_choices()
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Automatically set the created_by and updated_by fields based on the logged-in user."""
        if not obj.pk:  # New instance
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Borrower, BorrowerAdmin)