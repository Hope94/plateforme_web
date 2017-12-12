from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if myfile.name.split('.')[-1]=='apk':
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'detection_app/result.html', {
                'uploaded_file_url': uploaded_file_url
            })
        else:
            return render(request, "detection_app/index.html",{'message':'Veuillez charger un fichier .apk !'})

    return render(request,"detection_app/index.html")

