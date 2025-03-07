from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_user_data(request):
    user = request.user
    data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "organization": {
            "id": user.organization.id,
            "name": user.organization.name,
        },
    }
    return Response(data)
