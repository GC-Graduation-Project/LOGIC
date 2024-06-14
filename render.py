# render.py
import asyncio
from pyppeteer import launch
import os
import shutil
import platform

def find_chrome_executable():
    system = platform.system()
    if system == 'Windows':
        paths = [
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        ]
    elif system == 'Darwin':  # macOS
        paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ]
    else:  # Linux
        paths = [
            shutil.which('google-chrome'),
            shutil.which('chrome')
        ]

    for path in paths:
        if path and os.path.exists(path):
            return path
    return None

async def render_vextab_to_image(vextab_code, output_image_path):
    chrome_path = find_chrome_executable()
    if not chrome_path:
        raise FileNotFoundError("Could not find Chrome executable")

    # Pyppeteer를 사용하여 브라우저를 시작합니다.
    browser = await launch(
        executablePath=chrome_path,
        args=['--disable-infobars']
    )
    page = await browser.newPage()

    # 콘솔 로그를 출력합니다.
    page.on('console', lambda msg: print(f'Console log: {msg.text}'))

    # 페이지 뷰포트 크기 설정
    await page.setViewport({'width': 1200, 'height': 1000})

    # VexTab 코드를 HTML 페이지에 삽입합니다.
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vextab Example</title>
        <!-- Include the div.prod.js script -->
        <script src="https://unpkg.com/vextab@3.0.6/dist/div.prod.js" async></script>
    </head>
    <body>
    <div id="vex-tabdiv" class="vextab-auto" width=1080 scale=1.0 editor="false" editor-width=680 editor-height=330">{vextab_code}</div>
    </body>
    </html>
    """

    # HTML 콘텐츠를 페이지에 설정합니다.
    await page.setContent(html_content)

    # 렌더링된 결과를 캡처하기 전에 잠시 대기
    await asyncio.sleep(3)  # 필요에 따라 시간을 조정할 수 있습니다.

    # div의 위치와 크기를 계산하는 JavaScript 코드 실행
    clip = await page.evaluate('''
        () => {
            const rect = document.querySelector('#vex-tabdiv').getBoundingClientRect();
            return { x: rect.left, y: rect.top, width: rect.width, height: rect.height };
        }
    ''')

    # 특정 영역 스크린샷 캡처
    await page.screenshot({'path': output_image_path, 'clip': clip})
    print(f'Screenshot saved to {output_image_path}')

    # 브라우저를 종료합니다.
    await browser.close()
