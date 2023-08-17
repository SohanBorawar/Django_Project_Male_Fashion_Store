from django.db import models

# Create your models here.
class Contact(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.name

class User(models.Model):

    Organization_role = models.CharField(max_length=100,default='')
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100,default='')
    address = models.TextField()
    mobile = models.PositiveIntegerField()
    password = models.CharField(max_length=100,default='')

    def __str__(self) -> str:
        return self.fname + " " + self.lname
    
class Seller(models.Model):

    Organization_role = models.CharField(max_length=100,default='Seller')
    company_logo = models.ImageField(upload_to='company_logo/',default='')
    company_name = models.CharField(max_length=100,default='')
    first_name = models.CharField(max_length=100,default='')
    last_name = models.CharField(max_length=100,default='')
    email = models.EmailField()
    country = models.CharField(max_length=100,default='')
    address = models.CharField(max_length=100,default='')
    mobile = models.PositiveIntegerField()
    password = models.CharField(max_length=100,default='')
    admin_access = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.company_name + "--" + self.first_name
    
class Product(models.Model):

    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    choice1 = (
        ("Clothing","clothing"),
        ("Shoes","Shoes"),
        ("Accessories","Accessories"),
        )
    choice2 = (
        ("Formal Shirt","Formal Shirt"),
        ("Formal Pant","Formal Pant"),
        ("Casual Shirt","Casual Shirt"),
        ("Casual Pant","Casual Pant"),
        ("T-Shirt","T-Shirt"),
        ("Analog watch","Analog watch"),
        ("Smart watch","Smart watch"),
        ("Sport Shoes","Sport Shoes"),
        ("Casual Shoes","Casual Shoes"),
        ("Sunglasses","Sunglasses")
        )
    choice3 = (
        ("Regular","Regular"),
        ("Summer","Summer"),
        ("Winter","Winter"),
        ("Traditional","Traditional"),
        ("Party","Party"),
        )
    choice4 = (
        ("FITNESS","FITNESS"),
        ("LIFESTYLE","LIFESTYLE"),
        ("DISCIPLINE","DISCIPLINE"),
        ("EXERCISE","EXERCISE"),
        ("HEALTH","HEALTH"),
        ("Skin","Skin"),
        ("Body","Body"),
        )
    product_title = models.CharField(max_length=100)
    product_description = models.TextField()
    display_image = models.ImageField(upload_to='product_img')
    display_image1 = models.ImageField(upload_to='product_img')
    display_image2 = models.ImageField(upload_to='product_img')
    regular_price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    product_id = models.CharField(max_length=100,default='')
    category = models.CharField(max_length=100,choices=choice1)
    product_type = models.CharField(max_length=100,choices=choice2)
    collection = models.CharField(max_length=100,choices=choice3)
    tags = models.CharField(max_length=100,choices=choice4)
    date_time = models.CharField(max_length=100,default='')


    def __str__(self) -> str:
        return self.seller.company_name + "--" + self.product_title

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.fname + " " + self.product.product_title
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_price = models.PositiveIntegerField()
    product_qty = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    payment_status = models.BooleanField(default=False)
    date_time = models.CharField(max_length=100,default='')

    def __str__(self) -> str:
        return self.user.fname + " " + self.product.product_title
        