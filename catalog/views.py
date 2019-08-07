from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import boto3
from catalog.forms import EmployeeForm
from django.contrib.auth import views as auth_views
# Create your views here.

from .models import Book, Author, BookInstance, Genre,Employee
# @login_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
            'num_visits':num_visits},
    )

def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1IjoiaGFyaWN1ZGFudCIsImEiOiJjanl3MHRhM2YwdDNiM2JuNDd4amt1M3YxIn0.92iW1CftlEE32xmhO2ob0Q'
    return render(request, 'home.html',
                  { 'mapbox_access_token': mapbox_access_token })

login_required
from django.views import generic
from django.contrib.auth.decorators import login_required

class BookListView(generic.ListView):
    """
    Generic class-based view for a list of books.
    """
    model = Book
    paginate_by = 10
from django.contrib.auth.decorators import login_required


class BookDetailView(generic.DetailView):
    """
    Generic class-based detail view for a book.
    """
    model = Book

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

class AuthorListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Author
    paginate_by = 10 


class AuthorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')  


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

# from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    
    
    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.conf import settings

class AuthorCreate( CreateView):
    model = Author
    initial={'date_of_death':'05/01/2018',}
    permission_required = 'catalog.can_mark_returned'

    fields = '__all__'





class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
    

#Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'



def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                email = 'x18131581@student.ncirl.ie'
                print(email + "jjkjhkjhkajhdajdhpwpqoiw")
                message = 'Thanks for Verfying your City Library account. Please click the below link to continue..  http://ec2-54-154-11-155.eu-west-1.compute.amazonaws.com:8000/catalog'
                subject = 'This is my master piece'
                sqs = boto3.client('sqs', aws_access_key_id='AKIAX5756CDNQQXY5E47',
                                   aws_secret_access_key='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',
                                   region_name='eu-west-1')
                queue_url = 'https://sqs.eu-west-1.amazonaws.com/545456525531/send_otp'

                response = sqs.send_message(
                    QueueUrl=queue_url,
                    DelaySeconds=10,
                    MessageAttributes={
                        'email': {
                            'DataType': 'String',
                            'StringValue': email
                        },
                        'subject': {
                            'DataType': 'String',
                            'StringValue': subject
                        },
                        'message': {
                            'DataType': 'String',
                            'StringValue': message
                        }
                    },
                    MessageBody=('SES email trigger'
                                 )
                )
                return HttpResponseRedirect('/success/')
            except:
                pass
    else:
            print('gjgkjgvkjgvkjvkgvgkv kjgvkjvvgvg')
            form = EmployeeForm()
            return render(request,'success.html',{'form':form})
#
# @login_required
# def author(request):
#   return render(request,'success.html')

# def admin(request):
#     return render (request()


from django.contrib.auth import(

    authenticate,
    get_user_model,
    login,
    logout

)


from .forms import UserLoginForm, UserRegisterForm


def loginView(request):
    next = request.GET.get('next') ##
    form =UserLoginForm(request.POST or None)
    if form.is_valid():
        username =form.cleaned_data.get('username')
        password =  form.cleaned_data.get('password')
        user  =authenticate(username=username, password = password)
        login(request, user)

        if next:
            return redirect(next)
        return HttpResponseRedirect('/catalog')

    context ={
        'form' :form,
    }
    return render(request, "registration/login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form =UserRegisterForm(request.POST or None)
    if form.is_valid():
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                try:
                    email = 'x18170625@student.ncirl.ie'
                    print(email + "jjkjhkjhkajhdajdhpwpqoiw")
                    message = 'Thanks for Verfying your City Library account. Please click the below link to continue..  http://ec2-54-154-11-155.eu-west-1.compute.amazonaws.com:8000/catalog'
                    subject = 'This is my master piece'
                    sqs = boto3.client('sqs', aws_access_key_id='AKIAX5756CDNQQXY5E47',
                                       aws_secret_access_key='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',
                                       region_name='eu-west-1')
                    queue_url = 'https://sqs.eu-west-1.amazonaws.com/545456525531/send_otp'

                    response = sqs.send_message(
                        QueueUrl=queue_url,
                        DelaySeconds=10,
                        MessageAttributes={
                            'email': {
                                'DataType': 'String',
                                'StringValue': email
                            },
                            'subject': {
                                'DataType': 'String',
                                'StringValue': subject
                            },
                            'message': {
                                'DataType': 'String',
                                'StringValue': message
                            }
                        },
                        MessageBody=('SES email trigger'
                                     )
                    )
                    return HttpResponseRedirect('/success/')
                except:
                    pass
        else:
            print('gjgkjgvkjgvkjvkgvgkv kjgvkjvvgvg')
            form = UserRegisterForm()
            return render(request, 'success.html', {'form': form})
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password (password)
        user.save()
        new_user =authenticate(username = user.username, password = password)
        login(request, new_user)
        if next:
            return redirect(next)
        return HttpResponseRedirect('/success')

    context ={
        'form':form

    }
    return render(request, "sign_up.html", context)

# Create your views here.


def logout_view(request):
    logout(request)
    return render(request, "registration/logged_out.html")
