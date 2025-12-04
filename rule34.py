#                                 .-=+****+=-:                                                          #
#                              :+%@@@@@@@@@@@@@%*=.                 -+++++++++++.                       #
#                            :#@@@@@@@@@@@@@@@@@@@@%*=:            .%@@@@@@@@@@@.                       #
#                           =@@@@@@@@@@@@@@@@@@@@@@@@@@%*=:       .#@@@@@@@@@@@@                        #
#                          +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*++*#@@@@@@@@@@@@@#                        #
#                         =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                        #
#                        .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                         #
#                        +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.                         #
#                        %@@@@@@@@@@@@*-....-=*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:                          #
#                       .@@@@@@@@@@@@-          .=*%@@@@@@@@@@@@@@@@@@@@@@@*.                           #
#                       :@@@@@@@@@@@#               .=*%@@@@@@@@@@@@@@@@@*:                             #
#                                                       .-+*%@@@@@@@@#*-.                               #
#                                                             ......                                    #
#                                              by ~Tembul 2024                                          #

import requests
import os
import time
import re
import sys
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                          Rule34 Downloader v14.88                         ║")
    print("║                     Код говно. Так что обновлений не будет                ║")
    print("║                              furryfemboy.store                            ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")

def print_alert():
    print(f"{Colors.RED}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║             ИЗА ЗАЩИТЫ ОТ DDOS АТАКИ МОГУТ ПОЛЕЗТЬ ОШИБКИ                 ║")
    print("║             ТАКЖЕ МОГУТ БЫТЬ СКАЧЕНЫ ПОВРЕЖДЁНЫЕ ФОТОГРАФИИ               ║")
    print("║                     СТАВЬТЕ БОЛЬШЕ ЛИМИТ ФОТОГРАФИЙ                       ║")
    print("║                      МЕНЯЙТЕ IP ЕСЛИ БОЛЬШЕ ОШИБОК                        ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)


# Обрабатываемся часть скачивания, выгрузки, скорость и тд. Гы
def print_stats(success, failed, skipped, speed, elapsed, total):
    print(f"\n{Colors.BOLD}{Colors.CYAN}СТАТИСТИКА:{Colors.RESET}")
    print(f"  {Colors.GREEN}Успешно:{Colors.RESET} {success:4d} | {Colors.RED}Ошибок:{Colors.RESET} {failed:4d} | {Colors.YELLOW}Пропущено:{Colors.RESET} {skipped:4d}")
    print(f"  {Colors.BLUE}Скорость:{Colors.RESET} {speed:.2f} файлов/сек | {Colors.CYAN}Время:{Colors.RESET} {elapsed:.1f}с | {Colors.BOLD}Всего:{Colors.RESET} {total}")

# Спермотозоиды
def print_progress_bar(current, total, width=50):
    if total == 0:
        percent = 0
    else:
        percent = current / total
    
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    percentage = int(percent * 100)
    
    return f"[{bar}] {percentage}%"

# Ааааа вот тут мы вам покажем, откуда порнуха качается. Вот тут ээээээ, забыл. Ну там скрипт заходит как браузер в зависимости от ПО (Arch Linux user gay) и там качает хентай фурри гей порно
def download_images(tag, output_folder='downloaded_images', limit=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    base_url = 'https://rule34.xxx/index.php'
    page = 0
    success = 0
    failed = 0
    skipped = 0
    start_time = time.time()
    
    # хуйня после того как чел ввёл данные для выкачки сисек
    clear_screen()
    print_header()
    print_alert()
    
    print(f"{Colors.CYAN}Ищу по тегу:{Colors.RESET} {Colors.BOLD}{tag}{Colors.RESET}")
    print(f"{Colors.CYAN}Папка:{Colors.RESET} {Colors.BOLD}{output_folder}{Colors.RESET}")
    if limit:
        print(f"{Colors.CYAN}Лимит:{Colors.RESET} {Colors.BOLD}{limit}{Colors.RESET}")
    print()
    
    # ебатория
    while True:
        params = {
            'page': 'post',
            's': 'list',
            'tags': tag,
            'pid': page * 42
        }
        
        
        try:
            response = session.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            thumbnails = soup.find_all('a', class_='thumbnail')
            
            if not thumbnails:
                all_links = soup.find_all('a', href=re.compile(r'page=post&s=view&id='))
                if all_links:
                    thumbnails = all_links
            
            #Надеюсь, вы читать умеете, а то я заебался комментировать
            if not thumbnails:
                print(f"{Colors.YELLOW}Больше постов не найдено{Colors.RESET}\n")
                break
            
            for thumb in thumbnails:
                if limit and (success + failed) >= limit:
                    print(f"{Colors.YELLOW}Достигнут лимит!{Colors.RESET}\n")
                    break
                
                post_id = thumb.get('id')
                if not post_id:
                    href = thumb.get('href')
                    if href:
                        match = re.search(r'id=(\d+)', href)
                        if match:
                            post_id = match.group(1)
                    if not post_id:
                        continue
                else:
                    post_id = str(post_id).replace('p', '')
                
                post_url = f'https://rule34.xxx/index.php?page=post&s=view&id={post_id}'
                
                try:
                    post_response = session.get(post_url, timeout=10)
                    post_response.raise_for_status()
                    
                    post_soup = BeautifulSoup(post_response.text, 'html.parser')
                    
                    img_tag = post_soup.find('img', id='image')
                    video_tag = post_soup.find('video', id='image')
                    
                    file_url = None
                    if img_tag and img_tag.get('src'):
                        file_url = img_tag['src']
                    elif video_tag and video_tag.find('source'):
                        file_url = video_tag.find('source')['src']
                    
                    if not file_url:
                        continue
                    
                    if not file_url.startswith('http'):
                        file_url = 'https:' + file_url
                    
                    filename = os.path.basename(file_url.split('?')[0])
                    filepath = os.path.join(output_folder, filename)
                    
                    if os.path.exists(filepath):
                        skipped += 1
                        print(f"{Colors.YELLOW}Пропущено:{Colors.RESET} {filename}")
                        time.sleep(0.3)
                        continue
                    
                    file_response = session.get(file_url, timeout=30)
                    file_response.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        f.write(file_response.content)
                    
                    success += 1
                    elapsed = time.time() - start_time
                    speed = (success + failed) / elapsed if elapsed > 0 else 0
                    total = success + failed + skipped
                    
                    #Вывод всей ебатории
                    clear_screen()
                    print_header()
                    print_alert()
                    print(f"{Colors.CYAN}Ищу по тегу:{Colors.RESET} {Colors.BOLD}{tag}{Colors.RESET}")
                    print(f"{Colors.CYAN}Папка:{Colors.RESET} {Colors.BOLD}{output_folder}{Colors.RESET}\n")
                    
                    print_stats(success, failed, skipped, speed, elapsed, total)
                    
                    print(f"\n{Colors.CYAN}Прогресс:{Colors.RESET}")
                    print(f"  {print_progress_bar(success + failed, limit if limit else success + failed + 10)}")
                    
                    print(f"\n{Colors.GREEN}Последний:{Colors.RESET} {filename}")
                    print()
                    
                    time.sleep(0.8)
                    
                except Exception as e:
                    failed += 1
                    elapsed = time.time() - start_time
                    speed = (success + failed) / elapsed if elapsed > 0 else 0
                    total = success + failed + skipped
                    
                    print(f"{Colors.RED}Ошибка:{Colors.RESET} {str(e)[:50]}")
                    time.sleep(0.5)
            
            if limit and (success + failed) >= limit:
                break
            
            page += 1
            time.sleep(1)
            
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка при запросе: {e}{Colors.RESET}")
            break
    
    elapsed = time.time() - start_time
    speed = (success + failed) / elapsed if elapsed > 0 else 0
    total = success + failed + skipped
    
    # Я забыл, что тут было
    clear_screen()
    print_header()
    
    print(f"{Colors.BOLD}{Colors.GREEN}✨ СКАЧИВАНИЕ ЗАВЕРШЕНО!{Colors.RESET}\n")
    print_stats(success, failed, skipped, speed, elapsed, total)
    
    print(f"\n{Colors.CYAN}📁 Все файлы сохранены в:{Colors.RESET} {Colors.BOLD}{output_folder}{Colors.RESET}")
    print(f"{Colors.CYAN}⏱️  Общее время:{Colors.RESET} {Colors.BOLD}{elapsed:.1f} секунд{Colors.RESET}\n")
    
    # После завершения скачки, открываеться папка и отправляеться вашей маме на что вы дрочите 
    folder_path = os.path.abspath(output_folder)
    if os.name == 'nt':  # Windows
        os.startfile(folder_path)
    else:  # macOS и Linux
        subprocess.Popen(['open', folder_path])

# начало ебатории
if __name__ == '__main__':
    try:
        tag = input(f"{Colors.CYAN}Введи тег для поиска:{Colors.RESET} ").strip()
        if not tag:
            print(f"{Colors.RED}❌ Тег не может быть пустым!{Colors.RESET}")
            exit()
        
        folder = input(f"{Colors.CYAN}Папка для сохранения (Enter для 'downloaded_images'):{Colors.RESET} ").strip()
        if not folder:
            folder = 'downloaded_images'
        
        limit_input = input(f"{Colors.CYAN}Лимит изображений (Enter для всех):{Colors.RESET} ").strip()
        limit = int(limit_input) if limit_input.isdigit() else None
        
        download_images(tag, folder, limit)
    
     # Ааа пашёл нахуй
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⛔ Скачивание остановлено пользователем{Colors.RESET}")
        exit()
    except Exception as e:
        print(f"{Colors.RED}❌ Критическая ошибка: {e}{Colors.RESET}")


# Код был сгенерированый для того, чтобы выгрузить порнуху с e621.net во время отключения света в Украине. Так как плохая связь
# А ещё я учусь кодить на питоне изучая код и разбирая его. Чем учиться на нормальных туториалах, я учусь на говнокоде который сам же и пишу.
# А те кто изучают мой код, обосрите меня пж. Я дебил

#  http://wallera.furryfemboy.store/VS_prikol_1.jpg
#  http://wallera.furryfemboy.store/VS_prikol_2.jpg
#  http://wallera.furryfemboy.store/memes_1.png