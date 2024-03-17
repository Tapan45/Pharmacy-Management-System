from django.shortcuts import render,redirect,get_object_or_404
from .models import Medicine,Prescription,UserProfile,CartItem,Sales,SalaryDetails,Supplier,Inventory,Address,PaymentAmount,SelectAddress
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import LabBooking
from django.http import HttpResponse





#Home page
def home(request):
    return render(request,'index.html')

#Admin view page

def  admin_dashboard(request):
    return render(request,'Admin/admin_dashboard.html')

def add_salary(request):
    if request.method == 'POST':
        # Get form data from request.POST
        username = request.POST.get('username')
        basic = request.POST.get('basic')
        hra = request.POST.get('hra')
        others = request.POST.get('others')
        conv = request.POST.get('conv')
        max_epf_wages = request.POST.get('maxEpfWages')
        max_esi_wages = request.POST.get('maxEsiWages')
        lta = request.POST.get('lta')
        medical = request.POST.get('medical')
        rest_allow = request.POST.get('restAllow')
        gross_salary = request.POST.get('grossSalary')
        net_pay = request.POST.get('netPay')
        ctc = request.POST.get('ctc')
        employee_epf = request.POST.get('employeeEpf')
        employee_esi = request.POST.get('employeeEsi')
        employer_epf = request.POST.get('employerEpf')
        employer_esi = request.POST.get('employerEsi')
        print(f"Debug: Form data - "
         f"username: {username}, "
         f"basic: {basic}, "
         f"hra: {hra}, "
         f"others: {others}, "
         f"conv: {conv}, "
         f"max_epf_wages: {max_epf_wages}, "
         f"max_esi_wages: {max_esi_wages}, "
         f"lta: {lta}, "
         f"medical: {medical}, "
         f"rest_allow: {rest_allow}, "
         f"gross_salary: {gross_salary}, "
         f"net_pay: {net_pay}, "
         f"ctc: {ctc}, "
         f"employee_epf: {employee_epf}, "
         f"employee_esi: {employee_esi}, "
         f"employer_epf: {employer_epf}, "
         f"employer_esi: {employer_esi}")

        try:
            # Retrieve the user object based on the selected username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User with username {username} does not exist.")
            return redirect('add_salary')  # Redirect back to the form with an error message

        # Create and save SalaryDetails object
        salary_details = SalaryDetails.objects.create(
            user=user,
            basic=basic,
            hra=hra,
            others=others,
            conv=conv,
            max_epf_wages=max_epf_wages,
            max_esi_wages=max_esi_wages,
            lta=lta,
            medical=medical,
            rest_allow=rest_allow,
            gross_salary=gross_salary,
            net_pay=net_pay,
            ctc=ctc,
            employee_epf=employee_epf,
            employee_esi=employee_esi,
            employer_epf=employer_epf,
            employer_esi=employer_esi
        )

        messages.success(request, "Salary details added successfully.")
        return redirect('view_salary')  # Assuming 'view_salary' is the URL name for viewing salaries

    else:
        # If not a POST request, render the form template
        user_list = UserProfile.objects.all()
        return render(request, 'Admin/add_pharmassist_salary.html', {'user_list': user_list})





#Pharmacist View page
def  pharmassist_dashboard(request):
    return render(request,'pharmassist/pharmassist_dashboard.html')

def inventory_dashboard(request):
   
    return render(request, 'pharmassist/inventory_dashboard.html')

def add_medicine(request):
    if request.method == 'POST':
        medicine = Medicine(
            medicine_id=request.POST['medicine_id'],
            medicine_name=request.POST['medicine_name'],
            description=request.POST['description'],
            manufacturing_date=request.POST['manufacturing_date'],
            expire_date=request.POST['expire_date'],
            quantity=request.POST['quantity'],
            selling_price=request.POST['selling_price'],
            discounted_price=request.POST['discounted_price'],
            medicine_image=request.FILES['medicine_image'],
            category=request.POST['category'],
            subcategory=request.POST['subcategory']
        )
        medicine.save()
        return redirect('add_medicine')  # Redirect to a success page

    return render(request, 'pharmassist/add_medicine.html')

def view_medicine(request):
    medicine_list = Medicine.objects.all()
    context = {
        'medicine_list': medicine_list,
    }
    return render(request, 'inventory/view_medicine.html', context)

def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    medicine.delete()
    return redirect('view_medicine')


@login_required
def create_sales(request):
    user_list = UserProfile.objects.all()

    if request.method == 'POST':
        user = request.user
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        total_amount = request.POST.get('totalamount')

        # Create a new Sales instance
        sales_instance = Sales.objects.create(user=user, state=state, zipcode=zipcode, address=address, total_amount=total_amount)

        # Process and save SalesItem instances
        medicine_ids = request.POST.getlist('medicine[]')
        quantities = request.POST.getlist('quantity[]')
        amounts = request.POST.getlist('amount[]')

        for i in range(len(medicine_ids)):
            medicine = Medicine.objects.get(id=medicine_ids[i])
            quantity = int(quantities[i])
            amount = float(amounts[i])

            # Create a new SalesItem instance
            SalesItem.objects.create(sales=sales_instance, medicine=medicine, quantity=quantity, amount=amount)

        messages.success(request, 'Sales record created successfully.')
        return redirect('create_sales')  # Replace 'your_redirect_url' with the actual URL to redirect after successful submission

    # If the request is not a POST request, render the sales form
    return render(request, 'inventory/create_sales_medicine.html', {'user_list': user_list})  # Replace 'your_app_name' and 'your_sales_form_template' with actual values



from django.http import JsonResponse
from django.contrib.auth.models import User  # Import the User model

def get_user_details(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        print(f"Fetching details for user: {user_id}")

        try:
            user = User.objects.get(username=user_id)  # Correct the query to use 'username'

            user_details = {
                'state': user.profile.state,
                'zipcode': user.profile.zipcode,
                'address': user.profile.address,
            }

            print(f"User details: {user_details}")

            # Return JsonResponse with the user details
            return JsonResponse(user_details)

        except User.DoesNotExist:
            print("User not found")
            # Return JsonResponse with a 404 status and an error message
            return JsonResponse({'error': 'User not found'}, status=404)

    print("Invalid request")
    # Return JsonResponse with a 400 status and an error message
    return JsonResponse({'error': 'Invalid request'}, status=400)



def change_password(request):
    return render(request,'pharmassist/change_password.html')

def create_holiday(request):
    return render(request,'pharmassist/create_holidays.html')

def salary_slip(request):
    return render(request,'pharmassist/salary_slip.html')


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Supplier

def get_supplier_details(request):
    if request.is_ajax() and request.method == 'GET':
        supplier_id = request.GET.get('supplier_id')
        supplier = get_object_or_404(Supplier, id=supplier_id)

        supplier_details = {
            'name': supplier.name,
            'gst': supplier.gst,
            'phone': supplier.phone,
        }

        return JsonResponse(supplier_details)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


# Customer view Page
def customer_create(request):
    if request.method == 'POST':
        # Extract form data
        name= request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')

        # Add any additional validation as needed

        if password != confirmpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('your_registration_view_name')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('your_registration_view_name')

        # Create a new user instance and save to the database
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create a corresponding UserProfile instance
        user_profile = UserProfile(name=name ,user=user, phone=phone, state=state, address=address, zipcode=zipcode)
        user_profile.save()

        messages.success(request, "Registration successful. You can now login.")
      

    return render(request, 'Customer/customer_registration.html')
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('customer_dashboard')  # Replace 'your_dashboard_view_name' with the actual name of your dashboard view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Customer/customer_login.html')  # Replace with the actual login template path

def my_order(request):
    return render(request,'Customer/order_status.html')

def notifications(request):
    return render(request,'Customer/notifications.html')






@login_required
def  customer_dashboard(request):
    print("User:", request.user)
    print("Is authenticated:", request.user.is_authenticated)
    medicine_list = Medicine.objects.all()
    context = {
        'medicine_list': medicine_list,
    }
    
    return render(request,'Customer/customer_dashboard.html',context)
@login_required
def add_prescription(request):
    if request.method == 'POST':
        user = request.user  # Assuming user is logged in
        prescription = Prescription(user=user, prescription_file=request.FILES['prescription'])
        prescription.save()
        return redirect('customer_dashboard')
    return render(request, 'Customer/customer_dashboard.html')
@login_required
def delete_prescription(request, prescription_id):
    
    prescription = get_object_or_404(Prescription, pk=prescription_id)

    if request.method == 'POST':
       
        prescription.delete()
      
        return redirect('view_prescription')
    
  
@login_required
def view_prescription(request):
    prescription_list = Prescription.objects.all()
    context = {
        'prescription_list': prescription_list,
    }
    return render(request, 'pharmassist/prescription_list.html', context)
@login_required
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    return render(request, 'Customer/medicine_detail.html', {'medicine': medicine})
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = calculate_total_amount(cart_items)  # You need to implement this function
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'Customer/cart_view.html', context)


@csrf_exempt
def update_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        action = request.POST.get('action')
        print(f"Received request to {action} cart item with ID: {cart_item_id}")

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease':
                cart_item.quantity = max(1, cart_item.quantity - 1)

            cart_item.save()

            messages.success(request, 'Cart quantity updated successfully.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Cart item not found.')

        return redirect('cart_view')
    
@csrf_exempt
def delete_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        print(f"Received request to delete cart item with ID: {cart_item_id}")

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()

            messages.success(request, 'Cart item deleted successfully.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Cart item not found.')

        return redirect('cart_view')
    








def calculate_total_amount(cart_items):
    # Calculate the total amount based on your logic
    total_amount = sum(cart_item.medicine.discounted_price * cart_item.quantity for cart_item in cart_items)
    return total_amount



@login_required
def add_to_cart(request, medicine_id):
    # Retrieve the medicine object
    medicine = Medicine.objects.get(pk=medicine_id)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, medicine=medicine)

    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')  

def password_change(request):
    return render(request,'Customer/change_password.html')

def profile_view(request):
    # Get the UserProfile object associated with the currently logged-in user
    user_profile = request.user.userprofile  # Assuming UserProfile is related to the User model via a OneToOneField
    
    context = {
        'user_profile': user_profile
    }
    
    return render(request, 'Customer/profile_view.html', context)




def view_coupon(request):
    return render(request,'Customer/view_coupon.html')


@login_required
def apply_coupon(request, coupon_code):
    user = request.user

    # Check if the coupon exists
    try:
        coupon = Coupon.objects.get(user=user, coupon_code=coupon_code, is_applied=False)
    except Coupon.DoesNotExist:
        # Coupon does not exist or is already applied
        return redirect('some_failure_url')

    # Apply the coupon
    coupon.is_applied = True
    coupon.save()

    return redirect('cart_view')


# Inventory

def dashboard(request):
    total_customers = UserProfile.objects.count()
    total_medicines = Medicine.objects.count()
    
    # Calculate total medicine stock
    total_stock = sum([medicine.quantity for medicine in Medicine.objects.all()])
    
    context = {
        'total_customers': total_customers,
        'total_medicines': total_medicines,
        'total_stock': total_stock,
    }
    return render(request, 'inventory/dashboard.html', context)



def add_supplier(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gst = request.POST.get('gst')
        address = request.POST.get('address')

        # Create a new Supplier instance and save to the database
        Supplier.objects.create(name=name, phone=phone, email=email, gst=gst, address=address)

        return redirect('add_supplier')  # Redirect to a success page

    return render(request, 'inventory/add_supplier.html')

def delete_supplier(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
    except Supplier.DoesNotExist:
        return HttpResponse("Supplier not found", status=404)

    # Your logic to delete the supplier goes here
    supplier.delete()

    # Redirect to a different URL after successful deletion
    return redirect('view_suppliers')  
    
    






def view_suppliers(request):
    # Retrieve all suppliers from the database
    suppliers = Supplier.objects.all()

    # Pass the suppliers to the template
    context = {'suppliers': suppliers}
    return render(request, 'inventory/view_supplier.html', context)



def add_purchase(request):
    suppliers = Supplier.objects.all()
    
    context = {'suppliers': suppliers}
    return render(request,'inventory/add_purchase.html',context)

def create_holidays(request):
    return render(request,'inventory/create_holidays.html')

from django.http import HttpResponse

def lab_test(request):
    if request.method == 'POST':
        patient_name = request.POST.get('lab_name')
        patient_mobile = request.POST.get('lab_mobile')
        patient_pincode = request.POST.get('lab_pincode')
        lab_test = request.POST.get('lab_test')

        # Handle the checkbox value properly
        terms_agreed = request.POST.get('terms', False) == 'on'

        # Validate and process the data as needed
        # For simplicity, let's just save it to the database
        LabBooking.objects.create(
            patient_name=patient_name,
            patient_mobile=patient_mobile,
            patient_pincode=patient_pincode,
            lab_test=lab_test,
            terms_agreed=terms_agreed
        )

        messages.success(request, 'Thank you for booking! Our employee will contact you soon.')

    return render(request, 'Customer/lab_test.html')

from .models import Client

def add_client(request):
    if request.method == 'POST':
        # Get form data from POST request
        client_name = request.POST.get('clientName')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        gst_no = request.POST.get('gstNo')
        address = request.POST.get('address')

        # Create a new Client instance
        new_client = Client(
            client_name=client_name,
            phone_number=phone_number,
            email=email,
            gst_no=gst_no,
            address=address,
        )

        # Save the new client to the database
        new_client.save()

        # Redirect to a success page or do whatever you need
        return redirect('add_client')  # Replace 'success_page' with your actual success page URL

    return render(request, 'inventory/add_client.html')



def add_inventory(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        quantity = request.POST.get('quantity')

        # Create a new inventory entry
        Inventory.objects.create(product_name=product_name, quantity=quantity)

        return redirect('add_inventory') 

    return render(request, 'inventory/add_inventory.html')

def view_inventory(request):
    inventories = Inventory.objects.all()
    return render(request, 'inventory/view_inventory.html', {'inventories': inventories})


from django.http import JsonResponse

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return JsonResponse({'cart_count': 0})
    
@login_required
def make_payment(request):
    if request.method == 'POST':
        total_payable_amount = request.POST.get('cart_total_payable')
        user = request.user

        payment = Payment.objects.create(user=user, amount=total_payable_amount)

        # Redirect to a success page or any other page
        return redirect('payment_success')
    else:
        return HttpResponse("Invalid request")
    
    
def get_user_details(request):
    user_id = request.GET.get('user_id', None)

    if user_id:
        user_profile = UserProfile.objects.filter(user_id=user_id).first()

        if user_profile:
            user_details = {
                'state': user_profile.state,
                'zipcode': user_profile.zipcode,
                'address': user_profile.address,
            }
            return JsonResponse(user_details)

    return JsonResponse({'error': 'User details not found'}, status=400)


def get_supplier_details(request):
   
        supplier_id = request.GET.get('supplier_id',None)
        if supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier_details = {
                'name': supplier.name,  # Use supplier.name instead of Supplier.name
                'phone': supplier.phone,  # Use supplier.phone instead of Supplier.phone
                 # Use supplier.email instead of Supplier.email
                'gst': supplier.gst,  # Use supplier.gst instead of Supplier.gst
                 # Use supplier.address instead of Supplier.address
            }
            return JsonResponse(supplier_details)
     
        return JsonResponse({'error': 'Supplier not found'}, status=404)

# views.py
from django.http import JsonResponse
from .models import Medicine

def search_medicine(request):
    query = request.GET.get('query', '')
    medicines = Medicine.objects.filter(medicine_name__icontains=query)

    medicine_data = [{'medicine_id': med.medicine_id,
                      'medicine_name': med.medicine_name,
                      'manufacturing_date': med.manufacturing_date.strftime('%Y-%m-%d'),
                      'expiry_date': med.expire_date.strftime('%Y-%m-%d'),
                      'discounted_price': med.discounted_price} for med in medicines]

    return JsonResponse(medicine_data, safe=False)



def add_address(request):
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        if address:  # Check if address is not empty
            Address.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                address=address,
                state=state,
                zipcode=zipcode
            )
            # Redirect to another page after successful form submission
            return redirect('address')
    return render(request, 'Customer/address_detail.html', {'addresses': addresses})

def select_address(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        if selected_address_id:
            selected_address = Address.objects.get(pk=selected_address_id)
            user = request.user
            SelectAddress.objects.create(user=user, address=selected_address)
            # Redirect to a page after successful selection
            return redirect('captcha')  # Replace 'success_page' with your desired URL name
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'Customer/address_detail.html', {'addresses': addresses})



def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    
    # Ensure that the address belongs to the current user before deleting
    if address.user == request.user:
        address.delete()
    
    # Redirect to the address page after deletion
    return redirect('address')



def captcha(request):
    return render(request,'Customer/captcha.html')

def order_placed(request):
    return render(request,'Customer/thank_you.html')


def save_payment(request):
    if request.method == 'POST':
        user = request.user
        mrp_total = request.POST.get('mrp_total')
        additional_discount = request.POST.get('additional_discount')
        total_amount = request.POST.get('total_amount')
        shipping_charge = request.POST.get('shipping_charge')
        total_payable = request.POST.get('total_payable')
        total_savings = request.POST.get('total_saving')
        
        # Save payment details into the database
        payment = PaymentAmount.objects.create(
            user=user,
            mrp_total=mrp_total,
            additional_discount=additional_discount,
            total_amount=total_amount,
            shipping_charge=shipping_charge,
            total_payable=total_payable,
            total_savings=total_savings
        )
        payment.save()
        
        return redirect('address')
    
    
def order_request(request):
    addresses = SelectAddress.objects.all()
    cart_items = CartItem.objects.all()
    users = User.objects.all()
    amounts = PaymentAmount.objects.all()

    # Combine the data for display
    combined_data = []
    for user in users:
        user_data = {
            'user': user,
            'address': addresses.filter(user=user).first(),  # Assuming each user has one address
            'cart_items': cart_items.filter(user=user),  # Assuming multiple cart items per user
            'amount': amounts.filter(user=user).first()  # Assuming each user has one amount
        }
        combined_data.append(user_data)

    context = {
        'combined_data': combined_data,
    }
    return render(request,'inventory/order_request.html',context)
    

def order_invoice(request):
    return render(request,'inventory/order_invoice.html')