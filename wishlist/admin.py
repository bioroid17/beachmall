from django.contrib import admin
from wishlist.models import Wishlist

# Register your models here.
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("wishNum", "userId", "prodNum")
admin.site.register(Wishlist, WishlistAdmin)