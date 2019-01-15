from django.shortcuts import render
import logging
import os
import datetime
import json
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import response, schemas
from model_utils.solve import solve
from pickerservice.models import Solver
from pickerservice import urls

# schema_view = get_swagger_view(title='Picker Service API')


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((AllowAny,))
def schema_view(request):
    generator = schemas.SchemaGenerator(title='API Docs', patterns=urls.urlpatterns)
    return response.Response(generator.get_schema())

@api_view(['GET'])
# @renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
@permission_classes((IsAuthenticated, ))
def solve_request(request, format=None):
    """
    Endpoint used to pass HTTP request to find out if the customer request can be satisfied from the paint factory

    :param request: must contain 'input' param object containing 3 keys:
            colors: int
            customers: int
            demands: list of lists
    :return: Response object

    responseMessages:
        - code: 200
          message: Response returned
        - code: 400
          message: Bad request
    """
    if request.method == 'GET':
        user = request.user
        resp = solve(request.GET.get('input'))
        Solver.objects.create(problem=request.GET.get('input'), username=request.user.username,
                              req_date=datetime.datetime.now())
        if resp:
            return Response(data=resp,
                            status=status.HTTP_200_OK)

        return Response(data={'error': 'Failed to solve the request provided. Please consult the logs for '
                                           'further details'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def history_request(request):
    """
    Returns history for requests for a given user
    :param request: request object
    :return: Response object
    """
    records = Solver.objects.filter(username=request.user.username)

    json_res = []
    for record in records:
        json_obj = dict(
            problem=record.problem,
            username=record.username,
            req_date=str(record.req_date)
        )
        json_res.append(json_obj)
    return Response(data=json.dumps(json_res),
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def crash_request(request):
    """
    Endpoint to force a shut down of the server
    :param request:
    :return:
    """
    print('Force shutting down server')
    os.system("kill -9 {}".format(os.getpid()))
    return Response(data='killed',
                            status=status.HTTP_200_OK)
