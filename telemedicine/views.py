from django.shortcuts import render

#def home(request):
    #return render(request, "home.html")

def aboutpage(request):
   return render(request,'about.html')
