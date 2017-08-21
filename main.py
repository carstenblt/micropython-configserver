import uasyncio as asyncio
import configserver


loop = asyncio.get_event_loop(5)
loop.create_task(configserver.dns_server())
loop.create_task(app.get_task(host='0.0.0.0'))
loop.run_forever()