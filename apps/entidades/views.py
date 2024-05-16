from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.base.views import BaseModelViewSet
from apps.entidades import serializers

# Create your views here.


class MaestroViewSet(BaseModelViewSet):
    serializer_class = serializers.MaestroSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_types = {
        "list": ["all"],
        "create": ["all"],
        "update": ["all"],
        "retrieve": ["all"],
        "destroy": ["all"],
    }

    def list(self, request):
        offset = int(self.request.query_params.get("offset", 0))
        limit = int(self.request.query_params.get("limit", 10))

        searched_objects = self.queryset.all()[offset : offset + limit]
        serializer_class = (
            self.out_serializer_class(searched_objects, many=True)
            if self.out_serializer_class
            else self.serializer_class(searched_objects, many=True)
        )
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_class = self.serializer_class(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            for salon in request.data["salones"]:
                salon_serializer = serializers.SalonSerializer(data=salon)
                if salon_serializer.is_valid():
                    salon_serializer.save()
                else:
                    print("salon")
                    print(salon_serializer.errors)
                    return Response(
                        data=salon_serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            maestro = self.get_object(serializer_class.data.get("id"))
            maestro_out_serializer = self.serializer_class(maestro)
            return Response(
                data=maestro_out_serializer.data, status=status.HTTP_201_CREATED
            )
        print("maestro")
        print(serializer_class.errors)
        return Response(
            data=serializer_class.errors, status=status.HTTP_406_NOT_ACCEPTABLE
        )

    def retrieve(self, request, pk):
        searched_object = self.get_object(pk)
        serializer_class = (
            self.out_serializer_class(searched_object)
            if self.out_serializer_class
            else self.serializer_class(searched_object)
        )
        return Response(data=serializer_class.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        searched_object = self.get_object(pk)
        serializer_class = (
            self.out_serializer_class(searched_object, data=request.data, partial=True)
            if self.out_serializer_class
            else self.serializer_class(searched_object, data=request.data, partial=True)
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(data=serializer_class.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        searched_object = self.get_object(pk)
        searched_object.is_active = False
        searched_object.save()
        return Response(data={"message": "Deleted"}, status=status.HTTP_200_OK)
