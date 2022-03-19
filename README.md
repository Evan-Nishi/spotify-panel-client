# LED Spotify Interface

> Note this is a very brief guide and not at all exhaustive, feel free to contribute to the wiki

## Parts List
- [Adafruit Bonnet](https://www.adafruit.com/product/3211) or [HAT](https://www.adafruit.com/product/2345)
- [64x32 LED panel](https://www.adafruit.com/product/2278)
- [Raspberry pi 0w](https://www.adafruit.com/product/3400)
- Pin headers
- SD card (at least 16gb is reccommended)
- 5v Power supply

## Other Equipment
- Wire
- Wire strippers (optional)
- Soldering iron (techincally can be done solderless, but highly recommended)

expect the build cost to be at least around ~$80-$100 depending on what is in stock in the adafruit store
and shipping

## Hardware Setup
(optional) Enable PWM by soldering a jumper between pins 4 and 18 (reduces flickering, you will have to change settings in main.py if you are not using pwm)

Connect and solder the bonnet to the pi using the pin headers

Connect wires from board to bonnet 

(optional, highly recommended) Cut off pitchfork connectors, strip ends off wire, and put wire into terminal (this is to prevent connectors from shorting each other as they are exposed)
* Alternative: cover pitchfork connectors in electrical tape or heat shrink
(optional) Make a cover to diffuse light such as frosted plexiglass or even paper
(optional) 3D print a housing for the board

## Software Setup
Setup the raspi 0w headless with ssh and UART enabled.  Sometimes rpi-imager won't automatically enable UART even when using advanced settings and you may need to manually edit `/boot/config.txt` by adding `enable_uart=1` at the end.  Raspian lite is recommended.

Disable onboard sound by switching `dtparam-audio=off` in `/boot/config.txt` as the LED library and onboard sound don't get along

Clone the repo 

Run /scripts/setup.py from root of project

If that fails manually install cython, install the submodule, and build the package and install other dependencies with `sudo apt-get install libopenjp2-7`, `pip install python-dotenv` and `sudo pip3 install pillow` (libopenjp2-7 does not come default with rasbpian lite)

Create a dotenv file named .env with the same structure as example.env
* REF_TOKEN can be gotten by calling the spotify api request and granting permission
* CLIENT_ID and CLIENT_SECRET can be obtained after making a spotify app

(optional) It might be a good idea to have the program run on startup by putting the run command in rc.local