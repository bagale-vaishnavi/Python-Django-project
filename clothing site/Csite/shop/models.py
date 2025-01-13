from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="")
    category= models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default = 0)

    desc = models.TextField(default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to="upload/prod", default="")

    def __str__(self):
        return self.product_name
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
    
    @staticmethod
    def get_product_by_id(ids):
        if ids:
            return Product.objects.filter(id__in=ids)
        else:
            return Product.get_all_products()

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email= models.CharField(max_length=50, default="")
    PhoneNo = models.CharField(max_length=50, default="")
    message = models.CharField(max_length=500, default="")
    

    def __str__(self):
        return self.name
    

class Order(models.Model):
    Order_id = models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone = models.CharField(max_length=111)
    payment_id = models.CharField(max_length=120, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
        return f"Order {self.id} - {self.name}"

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

def __str__(self):
    return self.update_desc[0:7] + "..."