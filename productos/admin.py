from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html


# ---- PREVIEW DE IMÁGENES ----
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "hot", "image_preview")
    list_editable = ("hot",)
    search_fields = ("name",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = "Vista previa"


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "image_preview")
    list_filter = ("category",)
    search_fields = ("name", "description")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = "Vista previa"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)