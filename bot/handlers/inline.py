from aiogram import types

from bot import dp



@dp.inline_handler()
async def inline_query_filer(iq: types.InlineQuery):
    offset =  int(iq.offset) if iq.offset else 1
    results = []
    text = "Test Inline Results"
    for i in range(int(offset), 10):
        url = f"https://picsum.photos/id/{i}/200/300"
        results.append(
            types.InlineQueryResultPhoto(
                id=str(i),
                title=i.meme_file_size,
                photo_url=url,
                thumb_url=url,
            )
        )
    await iq.answer(
        results=results,
        cache_time=10,
        switch_pm_text=text,
        switch_pm_parameter="inline",
        next_offset=str(offset + len(results)),
        is_personal=False
    )