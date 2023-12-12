import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Product
from db.sqlalchemy import async_session_factory

logging.basicConfig(level=logging.INFO)

# асинхронно потому что в последнем проекте использовали асинхронное
# подключение, что бы не терять время вытащил оттуда


async def get_product_with_actual_price():
    session = async_session_factory()
    async with session.begin():
        query = select(
            Product
        ).options(
            # без этого в асинхронной алхимии никак, лениво не умеет грузить
            selectinload(Product.prices)
        )
        result = (await session.execute(query)).scalars()
        # тут пытался сортировать и фильтровать price с помощтю подзапросов,
        # но не смог xD
        # поэтому хоть так. Если можно то хотелось бы узнать как с подзапросом
        # сделать это.
        for product in result:
            last_prices = sorted(
                product.prices, key=lambda price: price.updated_at
            )[-1]
            logging.info(
                f'id:{product.id} name:{product.name} '
                f'price:{last_prices.value}'
            )


if __name__ == '__main__':
    asyncio.run(get_product_with_actual_price())
