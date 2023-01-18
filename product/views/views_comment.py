from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Comment
from product.serializers import CommentSerializer, CommentPostSerializer


class CommentCreateView(APIView):
    """
    Only authorized can create a comment
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=404)


class CommentUpdateView(APIView):
    """
    Only authorized and author can put a comment
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        snippet = get_object_or_404(Comment, id=pk)
        serializer = CommentPostSerializer(snippet, data=request.data, context={'request': request})
        if serializer.is_valid():
            if request.user == snippet.user:
                serializer.save()
                return Response(serializer.data)
            return Response("you are not author")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    """
    Only authorized and author can delete a comment
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        snippet = get_object_or_404(Comment, id=pk)

        if request.user == snippet.user:
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"you are not author"}, status=status.HTTP_400_BAD_REQUEST)
