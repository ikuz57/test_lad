import asyncio
import logging

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from db.models import Product, Price
from db.sqlalchemy import async_session_factory

logging.basicConfig(level=logging.INFO)

# асинхронно потому что в последнем проекте использовали асинхронное
# подключение, что бы не терять время вытащил оттуда


async def get_product_with_actual_price():
    # session = async_session_factory()
    # async with session.begin():
    #     query = select(
    #         Product
    #     ).options(
    #         # без этого в асинхронной алхимии никак, лениво не умеет грузить
    #         selectinload(Product.prices)
    #     )
    #     result = (await session.execute(query)).scalars()
    #     # тут пытался сортировать и фильтровать price с помощтю подзапросов,
    #     # но не смог xD
    #     # поэтому хоть так. Если можно то хотелось бы узнать как с подзапросом
    #     # сделать это.
    #     for product in result:
    #         last_prices = sorted(
    #             product.prices, key=lambda price: price.updated_at
    #         )[-1]
    #         logging.info(
    #             f'id:{product.id} name:{product.name} '
    #             f'price:{last_prices.value}'
    #         )
    session = async_session_factory()
    async with session.begin():
        # В принципе с оконными функция разобрался xD
        # Получение отсортированного списка цен для каждого продукта
        subquery = select(
            Price.product_id,
            func.max(
                Price.updated_at
            ).over(
                partition_by=Price.product_id
            ).label('min_updated')
        ).group_by(Price.product_id, Price.id).subquery('subquery')

        subquery_prices = select(Price).join(
            subquery,
            and_(
                Price.product_id == subquery.c.product_id,
                Price.updated_at == subquery.c.min_updated
            )
        ).subquery('subquery_prices')
        # Получение всех продуктов, где в поле "product.prices" содержится
        # только одна цена
        products = select(
            Product,
            subquery_prices.c.value.label('price_value'),
            subquery_prices.c.type.label('price_type'),
            subquery_prices.c.link.label('price_link')
        ).join(
            subquery_prices,
            Product.id == subquery_prices.c.product_id
        ).distinct()

        result = (await session.execute(products)).all()
        for res in result:
            logging.info(
                f'Product: id={res[0].id}, name={res[0].name}, price={res[1]}'
            )


if __name__ == '__main__':
    asyncio.run(get_product_with_actual_price())
