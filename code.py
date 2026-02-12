import os
def welcome(title):
    style = "=" * (len(title) + 8)
    print(style)
    print(f'=== {title} ===')
    print(style)

def menu(nomor_meja):
    daftar_makanan = []
    daftar_minuman = []
    daftar_harga_makanan = []
    daftar_harga_minuman = []
    daftar_jumlah_makanan = []
    daftar_jumlah_minuman = []
    total_harga_makanan = 0
    total_harga_minuman = 0
    
    
    
    makanan = {
    1: {'nama': "Soto Besar", 'harga': 6000},
    2: {'nama': "Soto Kecil", 'harga': 4000},
    3: {'nama': "Babat", 'harga': 5000},
    4: {'nama': "Paru", 'harga': 5000},
    5: {'nama': "Sundukan", 'harga': 3000},
    6: {'nama': "Bergedel", 'harga': 2000},
    7: {'nama': "Sosis Solo", 'harga': 3000},
    8: {'nama': "Tahu Bakso", 'harga': 2000},
    9: {'nama': "Pisang Goreng", 'harga': 2000},
    10: {'nama': "Bacem", 'harga': 2000},
    11: {'nama': "Tahu", 'harga': 1000},
    12: {'nama': "Tempe", 'harga': 1000},
    13: {'nama': "Bakwan", 'harga': 1000},
    14: {'nama': "Kerupuk", 'harga': 1000},
    15: {'nama': "Karak", 'harga': 1000},
    }
    minuman = {
    1: {'nama': "Es Teh", 'harga': 3000},
    2: {'nama': "Es Jeruk", 'harga': 4000},
    3: {'nama': "Teh Panas", 'harga': 3000},
    4: {'nama': "Jeruk Panas", 'harga': 4000},
    }
    print('===================================')
    print('======= Daftar Menu Makanan =======')
    print('===================================')
    for nomor, detail_makanan in makanan.items():
        print(f"{nomor}.{detail_makanan['nama']:<20} Rp. {detail_makanan['harga']:,}")
    print('===================================')

    
    while True:
        try:
            PILIHAN_MAKANAN =  int(input('Mau makanan apa? (1 - 15)\n--> '))
        except ValueError:
            print('Masukan angka')
            print('-------------')
            continue
        if  PILIHAN_MAKANAN > 15 or PILIHAN_MAKANAN < 1:
            print('Masukan nomor sesuai menu')   
            print('-------------------------')         
        if  PILIHAN_MAKANAN in makanan:
            ITEM_DIPILIH = makanan[PILIHAN_MAKANAN]
            MAKANAN_DIPILIH = ITEM_DIPILIH['nama']
            HARGA_DIPILIH_MAKANAN = ITEM_DIPILIH['harga']
            try:
                PORSI = int(input('Berapa porsi yang mau dibeli?\n--> '))
                if PORSI < 1:
                    print('Kamu tidak membeli makanan\n')
                    continue
            except ValueError:
                print('Masukan angka')
                print('-------------')
                continue
            HASIL_AKHIR_MAKANAN = HARGA_DIPILIH_MAKANAN * PORSI
            daftar_makanan.append(MAKANAN_DIPILIH)
            daftar_harga_makanan.append(HARGA_DIPILIH_MAKANAN)
            daftar_jumlah_makanan.append(PORSI)
            total_harga_makanan += HASIL_AKHIR_MAKANAN
            konfirm = input('Pengen nambah menu lagi? [y/n] ')
            if konfirm == 'y':
                print('-' * 30)
            elif konfirm == 'n':
                os.system('cls')
                print('===================================')
                print('======= Daftar Menu Minuman =======')
                print('===================================')
                for i, minuman_detail in minuman.items():
                    print(f"{i}.{minuman_detail['nama']:<20} Rp. {minuman_detail['harga']:,}")
                print('===================================')
                break
            else:
                print('Pilihan tidak valid')
    while True:
        try:
            PILIHAN_MINUMAN =  int(input('Mau minuman apa? (1 - 4)\n--> '))
        except ValueError:
            print('Masukan angka')
            print('-------------')
            continue
        if  PILIHAN_MINUMAN > 4 or PILIHAN_MINUMAN < 1:
            print('Masukan nomor sesuai menu')   
            print('-------------------------')
        if  PILIHAN_MINUMAN in minuman:
            ITEM2_DIPILIH = minuman[PILIHAN_MINUMAN]
            MINUMAN_DIPILIH = ITEM2_DIPILIH['nama']
            HARGA_DIPILIH_MINUMAN = ITEM2_DIPILIH['harga']
            try:
                PORSI_MINUMAN = int(input('Berapa minuman yang mau dibeli?\n--> '))
                if PORSI_MINUMAN < 1:
                    print('Kamu tidak membeli minuman\n')
                    continue
            except ValueError:
                print('Masukan angka')
                print('-------------')
                continue
            HASIL_AKHIR_MINUMAN = HARGA_DIPILIH_MINUMAN * PORSI_MINUMAN
            daftar_minuman.append(MINUMAN_DIPILIH)
            daftar_harga_minuman.append(HARGA_DIPILIH_MINUMAN)
            daftar_jumlah_minuman.append(PORSI_MINUMAN)
            total_harga_minuman += HASIL_AKHIR_MINUMAN
            confirm = input('Pengen nambah menu lagi? [y/n] ')
            if confirm == 'y':
                print('-' * 30)
            elif konfirm == 'n':
                print('-'*30)
                pembayaran = input('Mau lanjut ke pembayaran? [y/n] ')
                if pembayaran == 'n':
                    print('Pulang aja lu miskin')
                    break
                elif pembayaran == 'y':
                    try:
                        print('-'* 70)
                        QRIS_str = input('Pilih Metode Pembayaran (Saat ini layanan kami hanya menyediakan QRIS)\n1. QRIS\n--> ')
                        QRIS = int(QRIS_str)
                    except ValueError:
                        print('Masukan angka')
                        print('-------------')
                        continue
                    if QRIS == 1:
                        total_harga = total_harga_makanan + total_harga_minuman
                        print('-' * 60)
                        print(f'Total harga Rp.{total_harga:,}')
                        while True:
                            try:
                                jumlah_str = input('Masukan jumlah uangmu : ')
                                jumlah = int(jumlah_str)
                            except ValueError:
                                print('Masukan angka')
                                print('-------------')
                                continue
                            if jumlah >= total_harga:
                                os.system('cls')
                                kembalian = jumlah - total_harga
                                print('-' * 41)
                                print("\n\n=========================================")
                                print("============ STRUK PEMBELIAN ============")
                                print("=========================================")
                                print("- | Menu           | Jumlah |  Harga")
                                print("-----------------------------------------")
                                for i, (menumakan,menuminum, harga_makanan,harga_minuman ,jumlahbeli_makanan,jumlahbeli_minuman) in enumerate(zip(daftar_makanan,daftar_minuman, daftar_harga_makanan,daftar_harga_minuman, daftar_jumlah_makanan,daftar_jumlah_minuman), 1): 
                                    print(f'- {menumakan:15}{jumlahbeli_makanan:9}  x   Rp.{harga_makanan:,}')
                                    print(f'- {menuminum:15}{jumlahbeli_minuman:9}  x   Rp.{harga_minuman:,}')
                                print("=========================================")
                                print(f'Nomor Meja  : {nomor_meja}')
                                print(f'Total Harga : Rp.{total_harga:,}')
                                print(f'Dibayar     : Rp.{jumlah:,}')
                                print(f"Kembalian   : Rp.{kembalian:,}")
                                print("=========================================")
                                print("=== Terima kasih atas kunjungan Anda! ===")
                                print("=========================================\n\n")
                                print('-'* 41, '\n\n\n\n')
                                exit()
                            elif jumlah < total_harga:
                                print('Uangnya kurang kak, Mungkin salah input jumlahnya?')
            else:
                print('Pilihan tidak valid')

    
if __name__ == '__main__':
    menu(nomor_meja=50)
    
        
    


