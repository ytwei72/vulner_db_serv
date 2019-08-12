def req_get_param(request, param):
    return request.GET.get(param)


def req_get_param_int(request, param):
    data = req_get_param(request, param)
    return int(data)
