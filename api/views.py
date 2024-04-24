from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from work.models import Task
from api.serializer import TaskSerializer
from rest_framework.response import Response

class Taskviewset(ViewSet):

    def list(self,request,*args,**kwargs):
        qs=Task.objects.all()
        serializers=TaskSerializer(qs,many=True)
        return Response(data=serializers.data)
    
    def create(self,request,*args,**kwargs):
        serializer=TaskSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        return Response(serializers.errors)
    
    def retrieve(self,request,*args,**kwargs):
        k=kwargs.get("pk")
        qs=Task.objects.get(id=k)
        serializers=TaskSerializer(qs)
        return Response(data=serializers.data)
   
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.get(id=id).delete()
        return Response()
    
    def update(self,request,*args,**kwargs):
        k=kwargs.get("pk")
        qs=Task.objects.get(id=k)
        serializers=TaskSerializer(data=request.data,instance=qs)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        return Response(serializers.errors)





