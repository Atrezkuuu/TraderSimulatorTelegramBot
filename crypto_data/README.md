# crypto_data/
В файле crypto_graph хранится график цены на все монеты в боте который обновляется каждый час и сбрасывается каждый день.

Начальная структура файла:
{
    "BTC": [],
    "ETH": [],
    "USDT": [],
    "XRP": []
}

Структура при добавлении точки(-ек) цены:
{
    "BTC": [ТОЧКА, ТОЧКА...],
    "ETH": [ТОЧКА, ТОЧКА...],
    "USDT": [ТОЧКА, ТОЧКА...],
    "XRP": [ТОЧКА, ТОЧКА...]
}