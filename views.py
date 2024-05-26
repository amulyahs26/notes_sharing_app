from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from document.models import Register
from datetime import date
from teacherhome.models import Notes

def teacherhome(request):
    return render(request,'teacherhome.html')

def profile_teacher(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    info=Register.objects.get(user=user)
    I={'info':info,'user':user}
    return render(request,'profile_teacher.html',I)

def edit_profile_t(request):
    if not request.user.is_authenticated:
          return redirect('login')
    user=User.objects.get(id=request.user.id)
    info=Register.objects.get(user=user)
    error = False
    if request.method == 'POST':
        n = request.POST['name'] 
        t = request.POST['teacher_id']
        c = request.POST['contact'] 
        b = request.POST['branch']
        y = request.POST['year']
        user.first_name = n
        info.contact = c
        info.branch = b
        info.year = y
        info.teacher_id = t
        user.save()
        info.save()
        error="no"
    
    I={'info':info,'user':user,'error':error}
    return render(request,'edit_profile_t.html',I)

def change_password_t(request):
    if not request.user.is_authenticated: 
         return redirect('login')
    error=""
    if request.method=="POST":
        o = request.POST['old' ] 
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
             U = User.objects.get(username__exact=request.user.username)
             U.set_password (n)
             U.save()
             error="no"
        else:
             error="yes"
    d={'error':error} 
    return render(request,'change_password_t.html',d)
    

from django.shortcuts import render, get_object_or_404


def contact_teacher(request):
    user = get_object_or_404(User, id=request.user.id)
    info = get_object_or_404(Register, user=user)
    return render(request, 'contact_teacher.html', {'info': info})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notes
from datetime import date

def upload_notes(request):
    if request.method == 'POST':
        branch = request.POST.get('Branch')
        year = request.POST.get('year')
        subject = request.POST.get('subject')
        notes = request.FILES.get('notesfile')
        filetype = request.POST.get('filetype')

        # Check if all required fields are provided
        if branch and year and subject and notes and filetype:
            try:
                # Create a new Notes object and save it to the database
                Notes.objects.create(user=request.user, uploaded_date=date.today(), branch=branch,year=year, subject=subject, notesfile=notes, filetype=filetype,)
                messages.success(request, 'Notes uploaded successfully.')
                return redirect('upload_notes')
            except Exception as e:
                # Handle any exceptions or errors that occur during the saving process
                print(e)
                messages.error(request, 'Failed to upload notes. Please try again.')
        else:
            messages.error(request, 'Please fill out all required fields.')

    # Render the upload_notes template
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user=user)
    register_instance = Register.objects.get(user=user)
    
    
    registered_branch = register_instance.branch
       
    year = request.POST.get('year')  # Assuming the year is submitted via POST
    
    
    data = {'registered_branch':registered_branch}
   
    return render(request, 'upload_notes.html',data)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Notes

def view_notes(request):      
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user=user)
    
    # Get the Register instance associated with the user
    register_instance = Register.objects.get(user=user)
    
    # Debugging: Print the branch from the Register instance
    print(f"Branch from Register: {register_instance.branch}")
    
    # Iterate over each note and set its branch from the associated Register instance
    for note in notes:
        note.branch = register_instance.branch
        note.save()  # Save the updated note with branch
        
        # Debugging: Print note ID and its branch
        print(f"Note ID: {note.id}, Branch: {note.branch}")
    year = request.POST.get('year')  # Assuming the year is submitted via POST
   
    
    data = {'notes': notes, 'year': year}
   
    return render(request, 'view_notes.html', data)


def delete_notes (request, pid): 
    if not request.user.is_authenticated: 
        return redirect('login')
    notes=Notes.objects.get(id=pid) 
    notes.delete()
    return redirect('view_notes')



