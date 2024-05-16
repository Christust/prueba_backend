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
            maestro = self.get_object(serializer_class.data.get("id"))
            if len(request.data["salones"]) > 3:
                return Response(
                    data={"msg": "No enviar mas de tres salones"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            for salon in request.data["salones"]:
                salon["codigo"] = salon["id"]
                salon["letra"] = salon["letra"] + salon["numero"]
                salon_serializer = serializers.SalonSerializer(data=salon)
                if salon_serializer.is_valid():
                    salon_serializer.save()
                    new_salon = serializers.SalonSerializer.Meta.model.objects.filter(
                        codigo=salon["id"]
                    ).first()
                    new_salon.maestro = maestro
                    new_salon.save()
                else:
                    return Response(
                        data=salon_serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
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
        response_data = serializer_class.data
        if self.request.query_params.get("completo", False):
            salones = serializers.SalonSerializer.Meta.model.objects.filter(
                maestro=serializer_class.data["id"]
            )
            salones = serializers.SalonSerializer(salones, many=True)
            response_data["salones"] = salones.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        searched_object = self.get_object(pk)
        serializer_class = (
            self.out_serializer_class(searched_object, data=request.data, partial=True)
            if self.out_serializer_class
            else self.serializer_class(searched_object, data=request.data, partial=True)
        )
        if serializer_class.is_valid():
            serializer_class.save()
            response_data = serializer_class.data

            for salon in request.data["salones"]:
                salon["codigo"] = salon["id"]
                salon["letra"] = salon["letra"] + salon["numero"]
                salon_exist = serializers.SalonSerializer.Meta.model.objects.filter(
                    codigo=salon["id"]
                ).first()
                if salon_exist:
                    print(int(pk, base=10))
                    salon_exist.letra = salon["letra"]
                    salon_exist.maestro = searched_object
                    salon_exist.save()
                    response_data["salones"] = serializers.SalonSerializer(
                        salon_exist
                    ).data

                else:
                    salon_serializer = serializers.SalonSerializer(data=salon)
                    if salon_serializer.is_valid():
                        salon_serializer.save()
                        new_salon = (
                            serializers.SalonSerializer.Meta.model.objects.filter(
                                codigo=salon["id"]
                            ).first()
                        )
                        new_salon.maestro = searched_object
                        new_salon.save()
                        response_data["salones"] = serializers.SalonSerializer(
                            new_salon
                        ).data
                    else:
                        return Response(
                            data=salon_serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
            return Response(data=response_data, status=status.HTTP_202_ACCEPTED)
        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        searched_object = self.get_object(pk)
        searched_object.delete()
        return Response(data={"message": "Deleted"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def questions(self, request):
        from django.db.models import Count

        maestros = serializers.MaestroSerializer.Meta.model.objects.annotate(
            num_salones=Count("salon")
        ).order_by("-num_salones")
        salones_count = serializers.SalonSerializer.Meta.model.objects.filter(
            codigo="COD"
        ).count()
        sueldos_totales = 0
        maestros_response = []
        for maestro in maestros:
            sueldos_totales += maestro.sueldo
            maestros_response.append(
                f"{maestro.nombre_completo} {maestro.num_salones} salones"
            )

        response_data = {
            "sueldos_totales": sueldos_totales,
            "salones_count": salones_count,
            "maestros": maestros_response,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
