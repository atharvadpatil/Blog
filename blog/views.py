from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import BlogPostModelForm


from rest_framework import status
 
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authentication import TokenAuthentication

from rest_framework.pagination import PageNumberPagination

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticated
 
from rest_framework.response import Response

from blog.serializers import blogSerializer, registerationSerializer, userPropertiesSerializer

from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token




def blog_post_details_view(request, slug):
    #obj=BlogPost.objects.get(id=post_id)
    obj=get_object_or_404(BlogPost, slug=slug)
    template_name='blog\details.html'
    context={"object":obj}
    return render(request, template_name, context)


#CRUD

def blog_post_list_view(request):
    qs=BlogPost.objects.all()
    template_name='blog\list.html'
    context={"object_list":qs}
    return render(request, template_name, context)  


#def blog_post_create_view(request):
#    form = BlogPostForm(request.POST or None)
#    if form.is_valid():
#        obi =BlogPost.objects.create(**form.cleaned_data)
#        form = BlogPostForm()
#   template_name = "blog\create.html"
#   context={
#       'form' : form
#   }
#    return render(request, template_name, context)


#using modelForm
@login_required()
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BlogPostModelForm()
    template_name = "blog\create.html"
    context={
        'form' : form,
        'title': "Create BlogPost"
    }
    return render(request, template_name, context)

@login_required()
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(f"/blog_post/{obj.slug}")
    template_name = "blog\create.html"
    context={
        'form' : form,
        'title': f"update {obj.title}"
    }
    return render(request, template_name, context)

@login_required()
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    if request.method=="POST":
        obj.delete()
        return redirect("/blog_post")
    template_name = "blog\delete.html"
    context = {
        "obj" : obj
    }
    return render(request, template_name, context)






############# REST  #########
@api_view(["GET", "POST","DELETE"])

def BlogPost_list(request):
    if request.method == "GET":
        blogs = BlogPost.objects.all()
        serializer = blogSerializer(blogs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = blogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        count = BlogPost.objects.all().delete()
        return Response({'message': '{} Blogpost were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def BlogPost_detail_view(request, id):
    try:
        blog = BlogPost.objects.get(id=id)
    except:
        return Response({'message': 'The Blogpost does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        serializer = blogSerializer(blog, many=False)
        return Response(serializer.data)

    elif request.method=="DELETE":
        blog.delete()
        return Response({'message': 'Blogpost was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    else:
        blog_data = request.data
        serializer = blogSerializer(blog, data=blog_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class BlogList(generics.ListCreateAPIView): 
#    queryset = BlogPost.objects.all()
#    serializer_class = blogSerializer
 
#class BlogDetail(generics.RetrieveUpdateDestroyAPIView): 
#    queryset = BlogPost.objects.all()
#    serializer_class = blogSerializer

@api_view(['POST','GET'])
def registerView(request):
    if request.method=="POST":
        serializer = registerationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user = serializer.save()
            data['Response'] = "New User Successfully registered"
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['Token']=token
        else:
            data = serializer.errors
        return Response(data)
    else:
        users = User.objects.all()
        serializer = registerationSerializer(users, many=True)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIBlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = blogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

class APISearchView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = blogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'content')

@api_view(['GET'],)
def user_properties_view(request):
    try:
        user = request.user
    except User.DoesNotExists:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method=='GET':
        serializer = userPropertiesSerializer(user)
        return Response(serializer.data)

@api_view(['PUT'],)
def user_properties_update_view(request):
    try:
        user = request.user
    except User.DoesNotExists:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        serializer = userPropertiesSerializer(user, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "User Details Successfully Updated"
            return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    



