from django.http import JsonResponse
from .models import Post


def posts(request):
    order_by = request.GET.get("order")
    if order_by is not None:
        ordering_attr = order_by.lstrip("-")
        if not hasattr(Post, ordering_attr):
            return JsonResponse({
                "error": "Ordering attribute {} "
                         "does not exist".format(ordering_attr)})

    try:
        offset = int(request.GET.get("offset", 0))
        if offset < 0:
            raise ValueError("Negative numbers are not valid")
    except ValueError:
        return JsonResponse({
            "error": "Offset {} is not valid".format(request.GET["offset"])})
    try:
        limit = int(request.GET.get("limit", 5))
        if limit < 0:
            raise ValueError("Negative numbers are not valid")
    except ValueError:
        return JsonResponse({
            "error": "Limit {} is not valid".format(request.GET["limit"])})

    objects = Post.objects.order_by(order_by)
    if offset and limit:
        objects = objects[offset:offset + limit]
    elif offset:
        # if offset is too big then objects is []
        objects = objects[offset:]
    elif limit:
        objects = objects[:limit]

    return JsonResponse([
        {
            "id": o.id,
            "title": o.title,
            "url": o.url,
            "created": o.created
        } for o in objects
    ], safe=False)
