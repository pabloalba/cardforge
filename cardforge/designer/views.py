from django.shortcuts import redirect


def home(request):
    # return render(request, 'home.html')
    print("HOMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    return redirect('http://cardforge.net/home.html')
