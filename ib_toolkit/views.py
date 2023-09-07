from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import CreateNetworkSerializer, GenericResposeSerializer
from .models import Datacenter, DatacenterNetworkBlock, Network
from .utils import err_res, create_next_avail_network_container
from core.utils import create_application_audit_log
from django.forms.models import model_to_dict




class CreateNewNetwork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateNetworkSerializer

    @extend_schema(
        # description='Retrieve a list of items.',
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(response=GenericResposeSerializer,
                                                     description='Created. New resource in response'),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(response=GenericResposeSerializer,
                                                         description='Error creating resource'),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Authentication issue"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(response=GenericResposeSerializer,
                                                       description="Parent container not found")

        },
    )
    def post(self, request, format=None):
        """
        Create a new network container
        """
        serializer = CreateNetworkSerializer(data=request.data)
        user = request.user

        print(user)
        if serializer.is_valid():
            application_name = serializer.validated_data['application_name']
            application_environment = serializer.validated_data['application_environment']
            cidr_size = serializer.validated_data['cidr_size']
            datacenter = serializer.validated_data['datacenter']
            # Create the post or do something else with the data

            container_networks = DatacenterNetworkBlock.objects.filter(datacenter__name=datacenter,
                                                                       child_network_size=cidr_size)

            # Checks if parent container is found in Database
            if len(container_networks) == 0:
                return Response(err_res(f'No parent container defined for /{cidr_size} in {datacenter} datacenter'),
                                status=status.HTTP_404_NOT_FOUND)

            new_network_request = {'message': 'Unable to find network'}
            for container_network in container_networks:
                print(container_network.child_network_size, container_network.container_network)
                new_network_request = create_next_avail_network_container(container_network.container_network,
                                                                          container_network.child_network_size,
                                                                          f'{datacenter} - {application_name} - {application_environment}'.upper())
                # Success Request
                if new_network_request['status']:
                    network = Network(application=application_name,
                                      application_environment=application_environment,
                                      network=new_network_request['details']['network'],
                                      infoblox_ref=new_network_request['details']['infoblox_ref'],
                                      datacenter_name=datacenter,
                                      created_by=user.username)
                    network.save()
                    # Todo:: Create log entry
                    network_dict =model_to_dict(network)
                    print(network_dict)
                    print(network)
                    audit_log = create_application_audit_log(user=user.username,
                                                             object_changed=network.id,
                                                             object_type='ib_network',
                                                             old_value=None,
                                                             new_value=network_dict,
                                                             message=f'{network.infoblox_ref} was created in IPAM')

                    return Response(new_network_request, status=status.HTTP_201_CREATED)

                if new_network_request['error_code'] == 'ib_connection_error':
                    # Todo:: Create log entry
                    break

            return Response(new_network_request, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Data is not valid, return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

