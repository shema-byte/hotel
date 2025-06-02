from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .models import Booking
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .forms import SignUpForm, LoginForm ,BookingForm
from datetime import datetime, timedelta



def index(request):
    """Render the homepage."""
    context = {}
    if request.user.is_authenticated:
        # Get bookings for the current user
        bookings = Booking.objects.filter(email=request.user.email).order_by('-check_in')
        context['bookings'] = bookings
    return render(request, 'index.html', context)

def customer_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_obj = None

            # Try to find the user by username or email
            if User.objects.filter(username=login_input).exists():
                user_obj = User.objects.get(username=login_input)
            elif User.objects.filter(email=login_input).exists():
                user_obj = User.objects.get(email=login_input)
            else:
                return render(request, 'Customer_login.html', {
                    'form': form,
                    'error': 'No account found with that username or email.'
                })

            # Check if the user is a staff member
            if user_obj.is_staff:
                return render(request, 'Customer_login.html', {
                    'form': form,
                    'error': 'This login is for customers only. Please use the admin login.'
                })

            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')  # redirect to homepage after customer login
            else:
                return render(request, 'Customer_login.html', {
                    'form': form,
                    'error': 'Incorrect password. Please try again.'
                })
    else:
        form = LoginForm()
    return render(request, 'Customer_login.html', {'form': form})

def book_room(request):
    """Handle room booking."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        number_of_people = request.POST.get('number_of_people')
        room_type = request.POST.get('room_type')
        guest_type = request.POST.get('guest_type')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Save booking to the database
        booking = Booking(
            full_name=full_name,
            mobile_number=mobile_number,
            email=email,
            number_of_people=number_of_people,
            room_type=room_type,
            guest_type=guest_type,
            check_in=check_in,
            check_out=check_out
        )
        booking.save()

        # Set the booking confirmation message
        messages.success(request, 'Booking confirmed! Thank you for choosing Vibestay Hotels.')
        return redirect('index')  # Ensure 'index' is your homepage/view with the modal
    return render(request, 'book_room.html')

@login_required
def dashboard(request):
    today = date.today()
    bookings_today = Booking.objects.filter(booking_date__date=today)  # ensure booking_date is a DateTimeField

    context = {
        'total_rooms': 20,
        'active_bookings': Booking.objects.count(),
        'bookings': Booking.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def booking_history(request):
    one_month_ago = datetime.today() - timedelta(days=30)
    bookings = Booking.objects.filter(check_in__gte=one_month_ago)
    return render(request, 'booking_history.html', {'bookings': bookings})
def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'add_booking.html', {'form': form})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    return redirect('dashboard')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['email']  # Can be email or username
            password = form.cleaned_data['password']

            user_obj = None

            # Try to find the user by username or email
            if User.objects.filter(username=login_input).exists():
                user_obj = User.objects.get(username=login_input)
            elif User.objects.filter(email=login_input).exists():
                user_obj = User.objects.get(email=login_input)
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'No account found with that username or email.'
                })

            # Check if the user is a staff member
            if not user_obj.is_staff:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'This login is for admin users only. Please use the customer login.'
                })

            # Authenticate using the username (required by Django)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Update with your actual URL name
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Incorrect password. Please try again.'
                })
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def signup(request):
    """Handle user signup."""
    # Get the source of signup (customer or admin)
    signup_source = request.GET.get('source', 'customer')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already in use.')
            else:
                # Create user but ensure they are not staff
                user = form.save(commit=False)
                # Set staff status based on signup source
                user.is_staff = (signup_source == 'admin')
                user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                
                # Redirect based on signup source
                if signup_source == 'admin':
                    return redirect('login')  # Admin login URL
                else:
                    return redirect('customer_login')  # Customer login URL
    else:
        form = SignUpForm()

    # Pass the source to the template context
    context = {
        'form': form,
        'signup_source': signup_source
    }
    return render(request, 'signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    next_page = request.GET.get('next', 'customer_login')  # or 'home'
    return redirect(next_page)


def user_logout(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


def forgot_password(request):
    """Handle password reset requests."""
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html',
                subject_template_name='password_reset_subject.txt',
                from_email=None
            )
            messages.info(request, 'Password reset instructions have been sent to your email.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'forgot_password.html', {'form': form})