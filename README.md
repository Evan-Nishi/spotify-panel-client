# LED Spotify Interface

> Note this is a very brief guide and not at all exhaustive

## Parts List
- [Adafruit Bonnet](https://www.adafruit.com/product/3211) or [HAT](https://www.adafruit.com/product/2345)
- [64x32 LED panel](https://www.adafruit.com/product/2278)
- [Raspberry pi 0w](https://www.adafruit.com/product/3400)
- Pin headers
- SD card (at least 16gb is reccommended)
- 5v Power supply

## Other Equipment
- Wire
- Wire strippers
- Soldering iron

expect the build cost to be around ~$80-$100 depending on what is in stock in the adafruit store
and shipping


## Hardware Setup
Setup the raspi 0w in headless mode with ssh and UART enabled.  Raspian lite is recommended.

Enable PWM by soldering a jumper between pins 4 and 18 (optional, reduces flickering)

Connect and solder the bonnet to the pi using the pin headers

Connect wires from board to bonnet 

## Software Setup

Run /scripts/setup.py

If that fails manually install cython and install the submodule

Install other python dependencies

Create a dotenv file named .env with the same structure as example.env
* REF_TOKEN can be gotten by calling the spotify api request and granting permission
* CLIENT_ID and CLIENT_SECRET can be obtained after making a spotify app

It might be a good idea to have the program run on startup by putting the run command in rc.local(optional)