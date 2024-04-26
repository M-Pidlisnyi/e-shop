
def default(request):
    products_num = 0
    if len(request.session.keys()) > 0:
        for key in request.session.keys():
            if key.startswith('product_'):
                products_num += 1
    return {'products_num': products_num}