from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django import forms
from .forms import UploadFileForm
from .forms import UploadFileForm2
from .forms import UploadFileModel
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import UploadFileModel
from mainapp.models import Post
from mainapp.pdf2jpg import convert
import asyncio
from Vcsite import settings
import glob, os, os.path

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('/mainapp/'))
    else:
        '''form = UploadFileForm()'''
    print(form.files)
    for filename, file in request.FILES.items():
        name = request.FILES[filename].name
    print(name)
    post = UploadFileForm2(data=request.POST, files=request.FILES)
    post = Post()
    post.profile_pic = request.FILES.get('uploadfile')
    post.pdf = request.FILES.get('uploadfile')
    print(request.FILES.get('uploadfile'))
    post.save()
    #convert('mainapp/input',200)
    '''
    uploadfilemodel = UploadFileModel()
    uploadfilemodel.title = request.POST.get('uploadfile', None)
    print(request.POST.get('uploadfile'))
    uploadfilemodel.save()'''
    return render(request, 'mainapp/index.html')

@csrf_exempt
def upload_final(request):
    if request.method == 'POST':
        color = request.POST.get('color','')
        print(type(color))
        print(color)
        form = UploadFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('/mainapp/'))
    else:
        '''form = UploadFileForm()'''

    convert('mainapp/input', 200, color)
    filelist = glob.glob(os.path.join('mainapp/input',"*"))
    for f in filelist:
        os.remove(f)

    return render(request, 'mainapp/index.html')

def index(request):
    template = loader.get_template('mainapp/index.html')
    context = {
        'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))
