from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    zipcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    
    

class SelectAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    

    
    
class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('wellness', 'Wellness'),
        ('beauty', 'Beauty'),
    ]

    SUBCATEGORY_CHOICES = [
        ('covid_essential', 'COVID Essential'),
        ('diabetic_support', 'Diabetic Support'),
        ('eye_wear', 'Eye Wear'),
        ('hair_care', 'Hair Care'),
        ('skin_care', 'Skin Care'),
        ('mens_grooming', "Men's Grooming"),
    ]

    medicine_id = models.CharField(max_length=255)
    medicine_name = models.CharField(max_length=255)
    description = models.TextField()
    manufacturing_date = models.DateField()
    expire_date = models.DateField()
    quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_image = models.ImageField(upload_to='medicine_images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,blank='True')
    subcategory = models.CharField(max_length=20, choices=SUBCATEGORY_CHOICES,blank='True')

    def __str__(self):
        return self.medicine_name
    
class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    prescription_file = models.FileField(upload_to='prescriptions/')

  


class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, blank=True,null=True)
    zipcode = models.CharField(max_length=10 ,blank=True,null=True)
    address = models.CharField(max_length=255, blank=True,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class SalesItem(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate and update the amount based on the quantity and medicine's selling price
        self.amount = self.quantity * self.medicine.selling_price
        super().save(*args, **kwargs)
        
        
   
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.medicine_name} in {self.user.username}'s cart"
    
    
        
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)
    
    
    

class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=255)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.coupon_code}"
    
class SalaryDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)
    conv = models.DecimalField(max_digits=10, decimal_places=2)
    max_epf_wages = models.DecimalField(max_digits=10, decimal_places=2)
    max_esi_wages = models.DecimalField(max_digits=10, decimal_places=2)
    lta = models.DecimalField(max_digits=10, decimal_places=2)
    medical = models.DecimalField(max_digits=10, decimal_places=2)
    rest_allow = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    ctc = models.DecimalField(max_digits=10, decimal_places=2)
    employee_epf = models.DecimalField(max_digits=10, decimal_places=2)
    employee_esi = models.DecimalField(max_digits=10, decimal_places=2)
    employer_epf = models.DecimalField(max_digits=10, decimal_places=2)
    employer_esi = models.DecimalField(max_digits=10, decimal_places=2)

    

    def __str__(self):
        return f"{self.employee_name} - Basic: {self.basic}, HRA: {self.hra}"
    
    
class Holiday(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]

    start_day = models.DateField()
    end_day = models.DateField(blank=True, null=True)
    holiday_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    


    def is_sunday(self, date):
       
        return date.weekday() == 6

    def duration_in_days(self):
        if self.end_day:
            current_day = self.start_day
            total_days = 0
            sunday_count = 0

            while current_day <= self.end_day:
                total_days += 1

                if self.is_sunday(current_day):
                    sunday_count += 1

                current_day += timedelta(days=1)

            return {
                'total_days': total_days - sunday_count,
                'sunday_count': sunday_count,
            }
        else:
            # For single-day holidays
            if self.is_sunday(self.start_day):
                return {
                    'total_days': 0,
                    'sunday_count': 1,
                }
            else:
                return {
                    'total_days': 1,
                    'sunday_count': 0,
                }

    def __str__(self):
        return self.holiday_name


class LabBooking(models.Model):
    patient_name = models.CharField(max_length=50)
    patient_mobile = models.CharField(max_length=10)
    patient_pincode = models.CharField(max_length=6)
    lab_test = models.CharField(max_length=255)
    terms_agreed = models.BooleanField()

    def __str__(self):
        return self.patient_name
    
    
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gst = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Client(models.Model):
    client_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gst_no = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.client_name
    
    
    
class Inventory(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_name
    
    


class PaymentAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mrp_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    additional_discount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    shipping_charge = models.TextField(null=True)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f"Payment - {self.id}"

class CartSummary(models.Model):
    mrp_total = models.DecimalField(max_digits=10, decimal_places=2)
    additional_discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_applied = models.BooleanField(default=False)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cart Summary - ID: {self.id}"