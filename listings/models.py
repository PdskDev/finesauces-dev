from tabnanny import verbose
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ('-name',)
        verbose_name_plural='categories' 

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse(
            'listings:products_list_by_category',
            args=[self.slug]
        )

class Products(models.Model):
    category=models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(max_length=100, unique=True)
    image=models.ImageField(upload_to='products/')
    description=models.TextField
    shu=models.CharField(max_length=100, unique=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    available=models.BooleanField(default=True)
    
    class Meta:
        ordering=('shu',)
        verbose_name_plural='products' 
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'listings:products_detail',
            args=[self.category.slug, self.slug]
        )

    def get_average_review_score(self):
        average_score=0.0
        if self.reviews.count()>0:
            total_score=sum([review.rating for review in self.reviews.all()])
            average_score=total_score/self.reviews.count()
            return round(average_score, 1)


class Reviews(models.Model):
    product=models.ForeignKey(
        Products, related_name='reviews', on_delete=models.CASCADE)

    author=models.CharField(max_length=50)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)



    

