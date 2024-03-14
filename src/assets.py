from aiogram.types import FSInputFile

header = FSInputFile('assets/images/header.jpg')
bypass = FSInputFile('assets/images/bypass.gif')
with open('assets/code.js', 'r', encoding='utf-8') as f:
    code = f.read()
