from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from community.models import SaleArticle, PurchaseArticle

from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []
        timeleft = []
        timeleft_user = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
            if (item.timeleft <= 0): # if timeleft 0,1,2, the notice will be added.
                timeleft.append(item.name + " : " + str(item.timeleft))
                timeleft_user.append(item.username)
        sales = SaleArticle.objects.order_by('-time')[:3]
        purchases = PurchaseArticle.objects.order_by('-time')[:3]

        context = {
            'labels'    : labels,
            'data'      : data,
            'timeleft'  : timeleft,
            'timeleft_user': timeleft_user,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)

class HelpView(TemplateView):
    template_name = "help.html"

class SignUpView(TemplateView):
    template_name = "signup.html"
    #template_name = "home2.html"

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
