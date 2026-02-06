from fastapi import Depends, Body

from .router import router
from API.services.shop import ProductService, get_product_service
from API.schemas.products import FilterSchema


@router.post("/filter")
async def filter_products(data: FilterSchema = Body(), service: ProductService = Depends(get_product_service)):
    return await service.filter_products(data=data.dict())
