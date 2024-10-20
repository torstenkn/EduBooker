from django.contrib import admin
from .models import MediaCategory, LibrarySite, MediaType, Media

class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'colour', 'colour_code', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('code', 'name', 'colour')
    list_filter = ('colour', 'created_by')
    
    # Only make timestamps readonly
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        """Automatically set `created_by` and `updated_by` fields based on the logged-in user."""
        if not obj.pk:  # New instance
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

# Register the MediaCategory model with the admin
admin.site.register(MediaCategory, MediaCategoryAdmin)



class LibrarySiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_by')
    readonly_fields = ('created_at', 'updated_at')

    # Exclude `created_by` and `updated_by` from the form altogether
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        """Automatically set `created_by` and `updated_by` fields based on the logged-in user."""
        if not obj.pk:  # New instance
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

# Register the LibrarySite model with the admin
admin.site.register(LibrarySite, LibrarySiteAdmin)

class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    # Exclude `created_by` and `updated_by` from the form
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        """Automatically set `created_by` and `updated_by` fields based on the logged-in user."""
        if not obj.pk:  # New instance
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

# Register the MediaType model with the admin
admin.site.register(MediaType, MediaTypeAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_number', 'title', 'site', 'category', 'media_type', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('title', 'authors', 'media_number', 'isbn13')
    list_filter = ('site', 'category', 'media_type', 'created_by', 'updated_by')
    
    # Make `media_number` read-only
    readonly_fields = ('media_number', 'created_at', 'updated_at')

    # Exclude `created_by` and `updated_by` from the form
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        """Automatically set `created_by` and `updated_by` fields based on the logged-in user."""
        if not obj.pk:  # New instance
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Media, MediaAdmin)