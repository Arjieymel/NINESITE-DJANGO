from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Genders
from .models import Users
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .utils import login_required_custom
from django.views.decorators.cache import never_cache
from django.db.models import Q




@login_required_custom
@never_cache
def gender_list(request):
    try:
        genders = Genders.objects.all() #SELECT ALL FROM TBL_GENDERS

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')
@login_required_custom
@never_cache
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Genders.objects.create(gender=gender).save() # INSERT ALL TBL_GENDERS(GENDER) VALUES(GENDER)
            messages.success(request, 'Gender Added Succesfully!')         
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
       return HttpResponse(f'Error occured during add gender: {e}')
@login_required_custom
@never_cache
def edit_gender(request, genderId):
    try:
        if request.method =='POST':
            genderObj = Genders.objects.get(pk=genderId) #SELECT ALL FROM TBL_GENDERS WHERE GENDER_ID = GENDERID
            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save() #UPDATE the gender list

            messages.success(request, 'Gender updated successfully!')

            data = {
            'gender': genderObj
        }
 
            return redirect('/gender/list')
        
        else:
          genderObj = Genders.objects.get(pk=genderId) #SELECT ALL FROM TBL_GENDERS WHERE GENDER_ID = GENDERID

        data = {
            'gender': genderObj
        }

        return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required_custom
@never_cache
def delete_gender(request, genderId):
    try:
        if request.method =='POST':
            genderObj = Genders.objects.get(pk=genderId) #SELECT ALL FROM TBL_GENDERS WHERE GENDER_ID = GENDERID
            genderObj.delete() #UPDATE the gender list

            messages.success(request, 'Gender Deleted Successfully!')
            
            return redirect('/gender/list')
        else:
          genderObj = Genders.objects.get(pk=genderId) #SELECT ALL FROM TBL_GENDERS WHERE GENDER_ID = GENDERID

          data = {
            'gender': genderObj
         }
    
        return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during delete genders: {e}')
    

@login_required_custom
@never_cache
def user_list(request):
    try:
        query = request.GET.get('search', '')  # Get search value
        if query:
            user_list = Users.objects.filter(
                Q(full_name__icontains=query) |
                Q(email__icontains=query) |
                Q(address__icontains=query)
            )
        else:
            user_list = Users.objects.all()

        paginator = Paginator(user_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'userObj': page_obj,
            'search_query': query  # Pass it back to keep input value
        }

        return render(request, 'user/UsersList.html', data)

    except Exception as e:
        return HttpResponse(f"Error occurred during user list! {e}")

@login_required_custom
def add_user(request):
    try:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender_id = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            previous_data = {
                'full_name': full_name,
                'gender': gender_id,
                'birth_date': birth_date,
                'address': address,
                'contact_number': contact_number,
                'email': email,
                'username': username,
                'password': password,
                'confirm_password': confirm_password

            }

            if not all([full_name, gender_id, birth_date, address, contact_number, email, username, password]):
                messages.error(request, 'All fields are required.')
                genders = Genders.objects.all()
                return render(request, 'user/AddUser.html', {'genders': genders, 'previous_data': previous_data})

            if password != confirm_password:
                messages.error(request, 'Password and Confirm Password do not match!')
                genders = Genders.objects.all()
                return render(request, 'user/AddUser.html', {'genders': genders, 'previous_data': previous_data})

            try:
                gender = Genders.objects.get(pk=gender_id)
            except Genders.DoesNotExist:
                messages.error(request, 'Invalid gender selected.')
                genders = Genders.objects.all()
                return render(request, 'user/AddUser.html', {'genders': genders, 'previous_data': previous_data})

            Users.objects.create(
                full_name=full_name,
                gender=gender,
                birth_date=birth_date,
                address=address,
                contact_number=contact_number,
                email=email,
                username=username,
                password=make_password(password)
            )

            messages.success(request, 'User added successfully!')
            return redirect('/users/list')

        else:
            genders = Genders.objects.all()
            return render(request, 'user/AddUser.html', {'genders': genders})

    except Exception as e:
        messages.error(request, f"Error occurred during user creation: {e}")
        genders = Genders.objects.all()
        return render(request, 'user/AddUser.html', {'genders': genders, 'previous_data': request.POST})


@login_required_custom
@never_cache


@login_required_custom
@never_cache
def edit_user(request, userId):
    try:
        userobj = get_object_or_404(Users, pk=userId)

        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender_id = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            gender_instance = get_object_or_404(Genders, pk=gender_id)

            userobj.full_name = full_name
            userobj.gender = gender_instance
            userobj.birth_date = birth_date
            userobj.address = address
            userobj.contact_number = contact_number
            userobj.email = email
            userobj.username = username
            userobj.password = password

            userobj.save()
            messages.success(request, 'User Updated Succesfully!')
            return redirect('/users/list')

        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()

            data = {
                'user': userObj,
                'gender': genderObj
            }

        return render(request, 'user/EditUser.html', data)

    except Exception as e:
        return HttpResponse(f"error {e}")

@login_required_custom
@never_cache
def delete_user(request, userId):
    try:
        user = get_object_or_404(Users, pk=userId)
        
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User Deleted Succesfully!') 
            return redirect('/users/list')  # Redirect after delete
        
        # If GET request, show confirmation page
        return render(request, 'user/DeleteUser.html', {'user': user})
    
    except Exception as e:
        return HttpResponse(f"Error occurred during deletion: {e}")
    

@never_cache
def log_in(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                # Set session variable to mark user as logged in
                request.session['user_id'] = user.pk
                return redirect('/users/list')
            else:
                messages.error(request, 'Invalid password')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username')

    return render(request, 'layout/Login.html')

@login_required_custom
def password(request, userId=None):
    if not userId:
        messages.error(request, 'User ID is required to change the password.')
        return redirect('/user/list/')

    user = get_object_or_404(Users, pk=userId)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect(f'/user/password/{userId}/')

            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('/users/list')
        else:
            messages.error(request, 'Password fields cannot be empty!')

    return render(request, 'user/ChangePassword.html', {'user': user})


def log_out(request):
    request.session.flush()  # Clears all session data
    return redirect('login/')  # Change to your login UR




    