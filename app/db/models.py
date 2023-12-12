import datetime
from typing import Annotated, Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

created_at = Annotated[datetime.datetime, mapped_column(
    TIMESTAMP(timezone=True),
    server_default=text("TIMEZONE('utc', now())")
)]
updated_at = Annotated[datetime.datetime, mapped_column(
    TIMESTAMP(timezone=True),
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow
)]


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category.id', ondelete='SET NULL')
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    prices: Mapped[list['Price']] = relationship(
        back_populates='product',
        uselist=True
    )
    category: Mapped['Category'] = relationship(
        back_populates='products',
        uselist=False
    )
    characteristics: Mapped[list['Characteristic']] = relationship(
        back_populates='products',
        uselist=True,
        secondary='product_characteristic'
    )
    citys: Mapped[list['City']] = relationship(
        back_populates='products',
        uselist=True,
        secondary='product_city'
    )


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

    products: Mapped[list['Product']] = relationship(
        back_populates='citys',
        uselist=True,
        secondary='product_city'
    )


class ProductCity(Base):
    __tablename__ = 'product_city'

    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
        primary_key=True
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey('city.id', ondelete='CASCADE'),
        primary_key=True
    )


class Characteristic(Base):
    __tablename__ = 'characteristic'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

    products: Mapped[list['Product']] = relationship(
        back_populates='characteristics',
        uselist=True,
        secondary='product_characteristic'
    )


class ProductCharacteristic(Base):
    __tablename__ = 'product_characteristic'

    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
        primary_key=True
    )
    characteristic_id: Mapped[int] = mapped_column(
        ForeignKey('characteristic.id', ondelete='CASCADE'),
        primary_key=True
    )
    value: Mapped[Optional[int]]


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

    products: Mapped['Product'] = relationship(
        back_populates='category',
        uselist=False
    )


# хотел через enum, но если в дальнейшем что-то поменять, то так проще,
# на мой взгляд.
class PriceType(Base):
    __tablename__ = 'pricetype'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)


class Price(Base):
    __tablename__ = 'price'

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    type: Mapped[int] = mapped_column(
        ForeignKey('pricetype.id', ondelete='SET NULL')
    )
    link: Mapped[str] = mapped_column(String(256), unique=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE')
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    product: Mapped['Product'] = relationship(
        back_populates='prices',
        uselist=False
    )
