from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Artist

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_image')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        artist_user_ids = Artist.objects.values_list('user_id', flat=True)
        return qs.exclude(user_id__in=artist_user_ids)

    def profile_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:50%"/>',
                obj.image.url
            )
        return "No Image"

    profile_image.short_description = 'Profile Pic'


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_image')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def profile_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:50%"/>',
                obj.image.url
            )
        return "No Image"

    profile_image.short_description = 'Profile Pic'
