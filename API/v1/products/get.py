from fastapi import Depends

from .router import router
from API.services.shop import ProductService, get_product_service


@router.get("/")
async def get_products(service: ProductService = Depends(get_product_service)):
    return await service.get_products()

@router.get("/categories")
async def get_categories(service: ProductService = Depends(get_product_service)):
    return await service.get_categories()

@router.get("/categories/pair")
async def get_categories(service: ProductService = Depends(get_product_service)):
    data = await service.get_categories()
    
    second = False
    pair_categories = []
    
    for cat in data:
        if not second:
            pair_categories.append([cat])
            second = True
        else:
            pair_categories[-1].append(cat)
            second = False
            
    return pair_categories

@router.get("/product/{id}")
async def get_product(id: int, service: ProductService = Depends(get_product_service)):
    return await service.get_product(id=id)

@router.get("/filter/category/{id}")
async def get_products_by_category(id: int, service: ProductService = Depends(get_product_service)):
    return await service.filter_products(data={"categories": [id]})