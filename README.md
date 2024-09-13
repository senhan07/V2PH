# F4CK V2PH
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F2K9CHH)
<a href="https://www.buymeacoffee.com/_ramen_"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=_ramen_&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" height="30px"/></a>

![GitHub repo size](https://img.shields.io/github/repo-size/senhan07/V2PH?label=SIZE&style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/senhan07/V2PH?color=red&label=Issues&style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/senhan07/V2PH?label=Pull%20Requests&style=flat-square)
<br>
F4CK V2PH is a script for scraping images from the V2PH website. It supports album scraping, image URL extraction, and an image downloader.

## Main Features
- **Scrape Album URLs Based on Names**: Input the name of a model to scrape image albums associated with the name.
- **Retrieve Image URLs from Albums**: Fetch individual image URLs after scraping albums.
- **Download Images**: Download images from URLs specified in a `.txt` file.

---

### Demo
#### Scrapping albums
The output will be saved on `albums_url/[NAME].txt`  
Example `albums_url\2024-03-22_Jangjoo.txt`
```
https://www.v2ph.com/album/a9m6e8oa.html
https://www.v2ph.com/album/an3nx54z.html
https://www.v2ph.com/album/z69nxe8a.html
```

---

#### Scrapping images
The output will be saved on `image_url/[NAMES]/[ALBUM_TITLE].txt`  
Example `image_url\2024-03-22_Jangjoo\[ArtGravia] VOL.162 Jang Joo.txt`
```
https://cdn.v2ph.com/photos/TJqv9cajZNKBo1xR.jpg
    out=[ArtGravia] VOL.162 Jang Joo 35.jpg
https://cdn.v2ph.com/photos/UMRnw_W4l9rOsTru.jpg
    out=[ArtGravia] VOL.162 Jang Joo 3.jpg
https://cdn.v2ph.com/photos/EwVJlPhy88rHjMFY.jpg
    out=[ArtGravia] VOL.162 Jang Joo 15.jpg
```
> [!NOTE] 
> You can turn off the headless mode by change into `headless=False` on `module > driver.py`

https://github.com/user-attachments/assets/841214ec-39b7-4c10-97e6-afbe275ce83c

---

#### Downloading images
The output will be saved on `images\[NAME]\[NAME.jpg]`  
Example `images\[ArtGravia] VOL.154 Jang Joo`
```
images\[ArtGravia] VOL.154 Jang Joo\[ArtGravia] VOL.154 Jang Joo 0.jpg
images\[ArtGravia] VOL.154 Jang Joo\[ArtGravia] VOL.154 Jang Joo 1.jpg
images\[ArtGravia] VOL.154 Jang Joo\[ArtGravia] VOL.154 Jang Joo 2.jpg
```
https://github.com/user-attachments/assets/4332cce7-7418-4bac-9a07-0f544aad4932

## Prerequisites
- **Python 3.8+** (Tested on Python `3.10.9`)
- **Google Chrome** (Tested on version `128.0.6613.138`)
- **aria2c** (Tested on version `1.37.0`)


## Installation

1. Clone this repository:
```
git clone https://github.com/senhan07/V2PH.git
```

2. Navigate to the project directory:
```
cd V2PH
```

3. Install the required packages:  
   Recomended using virtual enviroment <i>(optional)</i>
   ```
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
   or without it
   ```
   pip install -r requirements.txt
   ```

5. Run
```
python main.py
```

## Notes
- Each account has 16 tokens, which reset every 24 hours.
- The script will automatically create a new account if all tokens are exhausted.
- It prioritizes using accounts with the highest available tokens.
- Before running, the script checks the last login for each account, resetting tokens if it has been 24 hours.
- **Just watch out for IP bans :)**.

## Todo
- [ ] Fix delay issue when checking existing scraped URLs.
- [ ] Implement proxy support for IP rotation.
- [x] Bypass Cloudflare Turnstile.
- [x] ~~Bypass Captcha with RecaptchaSolver~~.

## Disclaimer
This script is purely intended for practicing my programming and logic skills, not because of any personal interest in the content itself.

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License
This script is licensed under the [MIT License](LICENSE).