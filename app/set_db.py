import asyncio

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Product, City, Category, Characteristic, PriceType, Price
from db.sqlalchemy import async_session_factory


# асинхронно потому что в последнем проекте использовали асинхронное
# подключение, что бы не терять время вытащил оттуда

async def set_db():
    session = async_session_factory()
    async with session.begin():
        new_city = City(
            name='Irkutsk'
        )
        session.add(new_city)
        new_category = Category(
            name='toys'
        )
        session.add(new_category)
        new_caracters = []
        for name in ['weight', 'height']:
            new_caracters.append(
                Characteristic(
                    name=name
                )
            )
        for caracter in new_caracters:
            session.add(caracter)
        new_price_types = []
        for name in ['sale', 'retail', 'wholesale']:
            new_price_types.append(
                PriceType(
                    name=name
                )
            )
        for type in new_price_types:
            session.add(type)
        await session.flush()
        new_product = []
        for name in ['random_toy', 'toy']:
            new_product.append(
                Product(
                    name=name,
                    category_id=new_category.id,
                )
            )
        for product in new_product:
            for caracter in new_caracters:
                product.characteristics.append(caracter)
            product.citys.append(new_city)
            session.add(product)
        await session.flush()
        new_price_1 = []
        new_price_2 = []
        value = 100
        for price_type in new_price_types:
            new_price_1.append(
                Price(
                    value=value,
                    link=f'{price_type}1',
                    type=price_type.id,
                    product_id=new_product[0].id
                )
            )
            new_price_2.append(
                Price(
                    value=value,
                    link=f'{price_type}2',
                    type=price_type.id,
                    product_id=new_product[1].id
                )
            )
            value += 100
        for price in new_price_1:
            asyncio.sleep(1)
            session.add(price)

        for price in new_price_2:
            asyncio.sleep(1)
            session.add(price)

        await session.commit()

    session = async_session_factory()
    async with session.begin():
        new_price = Price(
                value=999,
                link='1111',
                type=1,
                product_id=1
        )
        session.add(new_price)
        await session.commit()

if __name__ == '__main__':
    asyncio.run(set_db())
