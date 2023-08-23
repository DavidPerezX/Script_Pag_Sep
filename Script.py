import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# tipos de libros
tag_books = ('LMP', 'MLA', 'PAA', 'PCA', 'PEA', 'SDA', 'TPA', 'CMA', 'SHA')

# URL bases para la descarga de las imagenes y la busqueda del libro
base_url = 'https://www.conaliteg.sep.gob.mx/2023/c/'
base2_url = 'https://www.conaliteg.sep.gob.mx/2023/'

async def download_image(session, img_url, img_path):
    try:
        async with session.get(img_url) as response:
            if response.status == 200:
                with open(img_path, 'wb') as img_file:
                    img_file.write(await response.read())
                print(f'Imagen descargada: {img_path}')
    except Exception as e:
        print(f'Error al descargar imagen {img_url}: {e}')

async def download_books():
    for i in range(0, 8):
        for le in range(0, len(tag_books)):
            try:
                # URL de los libros
                url = f'{base_url}P{i}{tag_books[le]}/'
                # url para buscar si existe el libro
                urlbusqueda = f'{base2_url}P{i}{tag_books[le]}.htm#page/2'

                async with aiohttp.ClientSession() as session:
                    response = await session.get(urlbusqueda)
                    response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    img_tags = soup.find_all('img')

                    output_folder = f'P{i}{tag_books[le]}'
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)

                    base = "000"

                    tasks = []
                    for img_cont in range(1, 400):
                        img_num = f"{base}{img_cont}"[-len(base):]
                        img_url = f'{url}{img_num}.jpg'
                        img_name = img_url.split('/')[-1]
                        img_path = os.path.join(output_folder, img_name)

                        task = download_image(session, img_url, img_path)
                        tasks.append(task)

                    await asyncio.gather(*tasks)

            except aiohttp.ClientError as e:
                print(f'No existe el libro {url}: {e}')
                continue

            print('Descarga completada.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_books())
