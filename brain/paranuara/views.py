from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError
from wstypes import TypeBase
from wstypes.error import NoResultsError, Error
from lib.person import PersonTable

def ws_response(ws_resp):
    """
    Return a Json HTTP response for the response provided.

    :param ws_resp: The response to be returned.
    :type ws_resp: str or TypeBase
    :return: Json response or HTTP Error.
    :rtype: JsonResponse or HttpResponseServerError
    """
    try:
        if isinstance(ws_resp, TypeBase):
            return JsonResponse(ws_resp.to_json(), safe=False)
        return JsonResponse(ws_resp, safe=False)
    except Exception, e:
        print "Error: Response couldn't be converted into json: %s" % e
    return HttpResponseServerError()

# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt # Skip CSRF verification for all API requests
def get_empolyees(request):
    """ Get all the employees for the provided company. """
    try:
        name = request.GET.get('name')
        if not name:
            msg = "Error: Please provide a valid company name in the url " \
                  "parameter 'name'"
            return ws_response(NoResultsError(message=msg))
        employees = PersonTable().get_by_company(name)
        return ws_response(employees)
    except Exception, e:
        print "Error: Failed to retrieve employees: %s" % e
    return ws_response(NoResultsError())

# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt # Skip CSRF verification for all API requests
def get_friends(request):
    """ 2 provided person info along with their common friends who are alive
    and have brown eyes. """
    try:
        p1 = request.GET.get('p1')
        p2 = request.GET.get('p2')
        if not p1 or not p2:
            msg = "Error: Please provide a valid person name in the url " \
                  "parameter 'p1' and 'p2'"
            return ws_response(NoResultsError(message=msg))
        json_info = PersonTable().get_common_friends(p1, p2)
        return ws_response(json_info)
    except Exception, e:
        print "Error: Failed to retrieve common friends: %s" % e
    return ws_response(NoResultsError())

# Create your views here.
@require_http_methods(["GET"])
@csrf_exempt # Skip CSRF verification for all API requests
def get_person(request):
    """ Get a person info by the provided username. """
    try:
        username = request.GET.get('username')
        if not username:
            msg = "Error: Please provide a valid username in the url " \
                  "parameter 'username'"
            return ws_response(NoResultsError(message=msg))
        person = PersonTable().get_by_username(username)
        if isinstance(person, Error):
            return person

        # Return json response without type Person
        json_person = person.to_json()
        return ws_response(json_person['Person'])
    except Exception, e:
        print "Error: Failed to retrieve person: %s" % e
    return ws_response(NoResultsError())