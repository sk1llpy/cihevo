from datetime import date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.config import BaseModel


class CategoriesTable(BaseModel):
    __tablename__ = 'shop_category'
    
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()
    category_type: Mapped[str] = mapped_column()

    products: Mapped[list["ProductsTable"]] = relationship(lazy="selectin", back_populates="category")


class BrandsTable(BaseModel):
    __tablename__ = 'shop_brand'
    
    title: Mapped[str] = mapped_column()
    logo: Mapped[str] = mapped_column()

    products: Mapped[list["ProductsTable"]] = relationship(lazy="selectin", back_populates="brand")


class ProductsTable(BaseModel):
    __tablename__ = 'shop_product'
    
    title: Mapped[str] = mapped_column()
    brand_id: Mapped[int] = mapped_column(ForeignKey('shop_brand.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('shop_category.id'))
    description: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()
    cost_price: Mapped[float] = mapped_column()
    price: Mapped[float] = mapped_column()
    in_sale: Mapped[bool] = mapped_column(default=False)
    sale_price: Mapped[float] = mapped_column()
    
    brand: Mapped["BrandsTable"] = relationship(lazy="selectin", back_populates="products")
    category: Mapped["CategoriesTable"] = relationship(lazy="selectin", back_populates="products")

    saved_products: Mapped[list["SavedProductsTable"]] = relationship(lazy="selectin", back_populates="product")
    basket: Mapped[list["BasketTable"]] = relationship(lazy="selectin", back_populates="product")
    product_photos: Mapped[list["ProductPhotosTable"]] = relationship(lazy="selectin", back_populates="product")
    store_products: Mapped[list["StoreProductsTable"]] = relationship(lazy="selectin", back_populates="product")
    

class ProductPhotosTable(BaseModel):
    __tablename__ = 'shop_productphoto'
    
    product_id: Mapped[int] = mapped_column(ForeignKey('shop_product.id'))
    photo: Mapped[str]
    is_main: Mapped[bool] = mapped_column(default=False)
    
    product: Mapped["ProductsTable"] = relationship(lazy="selectin", back_populates="product_photos")


class StoreProductsTable(BaseModel):
    __tablename__ = 'shop_storeproduct'
    
    product_id: Mapped[int] = mapped_column(ForeignKey('shop_product.id'))
    size: Mapped[str] = mapped_column()
    barcode: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=0)
    
    product: Mapped["ProductsTable"] = relationship(lazy="selectin", back_populates="store_products")
