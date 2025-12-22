from django.db import models
from django.utils.text import slugify
from product.models.category import Category  
from decimal import Decimal


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    general_category = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="products")
    free_shipping = models.BooleanField(default=False)
    available = models.CharField(max_length=50, default="in")
    sold = models.PositiveIntegerField(default=0)
    items_in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    variant_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.product.title})"


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_products")
    related = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="related_to")

    def __str__(self):
        return f"{self.product.title} -> {self.related.title}"


class BuyTogether(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="buy_together")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="part_of_bundle")

    def __str__(self):
        return f"{self.product.title} buy with {self.item.title}"
