# Warp Cloner

![warp-cloner](https://socialify.git.ci/totoroterror/warp-cloner/image?description=1&descriptionEditable=Simple%20Python%20script%20that%20can%20clone%20Warp%20Plus%20(1.1.1.1)%20keys%20and%20generate%2012PB%20keys.&language=1&name=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light)

Simple Python script that can clone [Warp Plus](https://1.1.1.1/) keys.

With this script you will be able to clone 12 PB keys in large amounts.

## Installation

1. Clone this repository
2. Install [Python 3.11](https://www.python.org/downloads/) or higher
3. Install dependencies using `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill variables (see next section)
5. Launch script using `python -u src/main.py`
6. Wait for results in console.

## Configuration

- `BASE_KEYS` (not required) - keys to clone divided by comma, if none then default keys will be used (script may not work with default keys)
- `THREADS_COUNT` (default: `1`) - amount of threads.
- `DEVICE_MODELS` (not required) - custom device model names divided by comma
- `PROXY_FILE` (not required) - path to proxy file, if none then script will be launched in proxyless mode.
- `DELAY` (default: `25`) - seconds to sleep after key clone
- `OUTPUT_FILE` (default: `output.txt`) - file to append generated keys
- `OUTPUT_FORMAT` (default: `{key} | {referral_count}`) - output format

## Notes

You can use ipv6 proxy as far as ipv4 proxy if they don't block Warp API endpoint.

## Contributing

I will support this project as far as I can, but issues and pull requests are always welcome!

## License

This project licensed under MIT License.

## Support me

You can support my further developments or support this project by buying me a coffee or pizza.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/totoroterror)
