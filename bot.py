import requests
import names
import time
import random
import json
import os
from colorama import init, Fore, Style

# Inisialisasi colorama untuk warna di terminal
init()

# URL endpoint
url = "https://api.getwaitlist.com/api/v1/waiter"

# Headers
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://pumppals.fun",
    "referer": "https://pumppals.fun/",
    "sec-ch-ua": '"Chromium";v="130", "Mises";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
}

# Fungsi untuk menghasilkan email acak
def generate_random_email():
    first_name = names.get_first_name().lower()
    last_name = names.get_last_name().lower()
    random_num = random.randint(1, 9999)
    return f"{first_name}{last_name}{random_num}@gmail.com"

# Fungsi untuk menyimpan email ke accounts.json
def save_email(email):
    file_path = "accounts.json"
    try:
        # Baca file jika sudah ada
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []
        # Tambahkan email baru
        data.append({"email": email})
        # Simpan kembali ke file
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"{Fore.RED}Gagal menyimpan email: {e}{Style.RESET_ALL}")

# Banner
print(f"{Fore.CYAN}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
print(f"{Fore.CYAN}║       🌟 Waitlist Blaster - Mass Signup      ║{Style.RESET_ALL}")
print(f"{Fore.CYAN}║ Automate waitlist signups with random emails!║{Style.RESET_ALL}")
print(f"{Fore.CYAN}║  Developed by: https://t.me/sentineldiscus   ║{Style.RESET_ALL}")
print(f"{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}\n")

# Input kode referral (wajib)
while True:
    ref_id = input(f"{Fore.YELLOW}Masukkan kode referral (wajib): {Style.RESET_ALL}").strip()
    if ref_id:
        break
    print(f"{Fore.RED}Kode referral tidak boleh kosong!{Style.RESET_ALL}")

# Input jumlah referral
while True:
    try:
        num_requests = int(input(f"{Fore.YELLOW}Masukkan jumlah referral: {Style.RESET_ALL}"))
        if num_requests > 0:
            break
        print(f"{Fore.RED}Jumlah referral harus lebih dari 0!{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Masukkan angka yang valid!{Style.RESET_ALL}")

# Payload
payload_template = {
    "answers": [],
    "email": "",
    "heartbeat_uuid": "",
    "referral_link": f"https://pumppals.fun/?ref_id={ref_id}",
    "waitlist_id": 24630,
    "widget_type": "WIDGET_1"
}

# Delay antar request
delay = 3

# Loop untuk mengirim request
for i in range(num_requests):
    try:
        # Generate payload
        payload = payload_template.copy()
        email = generate_random_email()
        payload["email"] = email

        # Log email
        print(f"{Fore.BLUE}Request {i+1}/{num_requests}: {email}{Style.RESET_ALL}")

        # Kirim POST request
        response = requests.post(url, json=payload, headers=headers)

        # Cek status code
        if response.status_code == 200:
            print(f"{Fore.GREEN}Berhasil{Style.RESET_ALL}")
            save_email(email)
        else:
            print(f"{Fore.RED}Gagal{Style.RESET_ALL}")

        # Delay antar request
        time.sleep(delay)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        time.sleep(delay)

print(f"\n{Fore.CYAN}Selesai mengirim {num_requests} request.{Style.RESET_ALL}")
