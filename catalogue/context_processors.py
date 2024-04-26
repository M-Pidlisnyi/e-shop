
def default(request):
    products_num = sum(1 for key in request.session.keys() if key.startswith('product_'))
    return {'products_num': products_num}