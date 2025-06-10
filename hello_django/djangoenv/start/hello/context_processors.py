def user_info(request):
    return {
        'user_type': request.session.get('user_type'),
        'user_name': request.session.get('user_name'),
        'user_id': request.session.get('user_id'),
    } 