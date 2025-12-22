from django.contrib import admin
from product.models.product import Product, ProductImage, ProductVariant, BuyTogether, RelatedProduct
from product.models.category import Category

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(BuyTogether)
admin.site.register(RelatedProduct)
