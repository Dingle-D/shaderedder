from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import CollectionView

router = APIRouter(prefix="/collections", tags=["collections"])

@router.get("/", response_model=List[CollectionView])
def read_users_me():
    ret = [CollectionView(id=1, title="collection 1", preview=['https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg', 
                                                               'https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg',
                                                               'https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg',
                                                               'https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg'], tags=['fragment', 'vertex', 'animated', 'scene', 'not_animated', 'material', 'orange']), 
           CollectionView(id=2, title="collection 2", preview=['https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg',
                                                               'https://tailwindcss.com/plus-assets/img/ecommerce-images/category-page-04-image-card-01.jpg'], tags=['fragment', 'vertex', 'animated', 'scene', 'not_animated', 'material', 'orange']), 
           ]
    print(ret)
    return ret
