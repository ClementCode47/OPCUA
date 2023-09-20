import asyncio
from asyncua import ua, uamethod, Server

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.cleanup()

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://10.4.1.212:4840")
    server.set_server_name("FreeOpcUa Example Server")

    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    led_node = await server.nodes.objects.add_object(idx, "LED1")
    red_node = await led_node.add_variable(idx, "RedLed", False)
    green_node = await led_node.add_variable(idx, "GreenLed", False)
    blue_node = await led_node.add_variable(idx, "BlueLed", False)

    @uamethod
    def fermerLed(parent):
        parent.get_child(idx, "RedLed", False).set_writable()
        parent.get_child(idx, "GreenLed", False).set_writable()
        parent.get_child(idx, "BlueLed", False).set_writable()

    async with server:
        while True:
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())