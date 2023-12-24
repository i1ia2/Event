import asyncio
import aiohttp
import aiosqlite
from models import init_db, close_db, SwapiPeople, Session
from more_itertools import chunked

CHUNK_SIZE = 10


async def inser_people(people_list):
    people_list = [SwapiPeople(json=person) for person in people_list]
    async with Session() as session:
        session.add_all(people_list)
        await session.commit()


async def get_person(person_id):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{person_id}/")
    json_response = await response.json()
    await session.close()
    return json_response



async def main():
    await init_db()

    for person_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
        coros = [get_person(person_id) for person_id in person_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(inser_people(result))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await close_db()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

 # import asyncio
    # import aiohttp
    # from sqlalchemy import create_engine
    # from more_itertools import chunked
    # from models import init_db, close_db, SwapiPeople, async_session
    #
    #
    # CHUNK_SIZE = 10
    #
    # async def inser_people(people_list):
    #     people_list = [SwapiPeople(json=person) for person in people_list]
    #     async with async_session() as session:
    #         session.add_all(people_list)
    #         await session.commit()
    #
    #
    #
    # async def fetch_person(session, person_id):
    #     url = f'https://swapi.dev/api/people/{person_id}/'
    #     async with session.get(url) as response:
    #         return await response.json()
    #
    # async def main():
    #     await init_db()
    #
    #     async with aiohttp.ClientSession() as session:
    #         # tasks = [inser_people(await fetch_person(session, person_id)) for person_id in range(1, 100)]
    #         for person_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
    #             coros = [fetch_person(session, person_id) for person_id in person_id_chunk]
    #             result = await asyncio.gather(*coros)
    #             asyncio.create_task(inser_people(result))
    #         tasks = asyncio.all_tasks() - {asyncio.current_task()}
    #
    #         await asyncio.gather(*tasks)
    #
    #     await close_db()
    #
    #
    # if __name__ == "__main__":
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #     asyncio.run(main())

