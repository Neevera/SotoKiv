from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout  # Untuk konten dialog
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ListProperty, NumericProperty, DictProperty, ColorProperty
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField  # Untuk input di dialog
import csv
from datetime import datetime
import os
import json

#backup data menu
makanan_data = {} #jika json data makanan hilang, bisa load menggunakan dictionary makanan biasa disini terlebih dahulu
minuman_data = {}


class MenuListItem(MDBoxLayout):
    item_data = DictProperty({})
    background_color = ColorProperty([1, 1, 1, 1])  # Default putih

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Struktur MenuListItem didefinisikan di file .kv
        pass


class CartItem(MDBoxLayout):
    item_data_ref = DictProperty({})
    background_color = ColorProperty([1, 1, 1, 1])  # Default putih


class MenuScreen(Screen):
    pass


class CartScreen(Screen):
    pass


class PaymentScreen(Screen):
    pass


class ReceiptScreen(Screen):
    pass


class Tab(MDBoxLayout, MDTabsBase):
    pass


class SotoKivApp(MDApp):
    cart = ListProperty([])
    total_cart_price = NumericProperty(0)
    nomor_meja = NumericProperty(1)
    TRANSACTIONS_FILE = "transactions.csv"
    MAKANAN_DATA_FILE = "makanan_data.json"
    MINUMAN_DATA_FILE = "minuman_data.json"
    add_item_dialog = None
    edit_item_dialog = None
    remove_item_dialog = None
    
    def load_menu_data(self): # Memuat data menu (makanan dan minuman) dari file JSON saat aplikasi dimulai
        global makanan_data, minuman_data
        try:
            if os.path.exists(self.MAKANAN_DATA_FILE):
                with open(self.MAKANAN_DATA_FILE, 'r') as f:
                    loaded_makanan = json.load(f)
                    # JSON menyimpan kunci sebagai string, konversi kembali ke integer
                    makanan_data = {int(k): v for k, v in loaded_makanan.items()}
            # Jika file tidak ada, makanan_data default akan digunakan

            if os.path.exists(self.MINUMAN_DATA_FILE):
                with open(self.MINUMAN_DATA_FILE, 'r') as f:
                    loaded_minuman = json.load(f)
                    minuman_data = {int(k): v for k, v in loaded_minuman.items()}
            # Jika file tidak ada, minuman_data default akan digunakan

        except Exception as e:
            print(f"Error loading menu data: {e}")
            # Jika ada error, gunakan data default yang sudah ada di skrip

    def save_menu_data(self): # Menyimpan data menu (makanan dan minuman) saat ini ke file JSON
        try:
            with open(self.MAKANAN_DATA_FILE, 'w') as f:
                json.dump(makanan_data, f, indent=4)
            with open(self.MINUMAN_DATA_FILE, 'w') as f:
                json.dump(minuman_data, f, indent=4)
        except Exception as e:
            print(f"Error saving menu data: {e}")
            self.show_message_popup("Error", f"Gagal menyimpan data menu: {e}")

    def on_stop(self): # Metode ini dipanggil saat aplikasi akan ditutup
        self.save_menu_data()

    def build(self): # Metode utama yang membangun antarmuka pengguna (UI) aplikasi saat pertama kali dijalankan
        self.title = "Soto Kwali Mbah Cipto"
        self.load_menu_data() #muat data menu saat aplikasi dimulai
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.sm = self.root # root diatur oleh Kivy saat memuat file .kv
        self.populate_menus()
        menu_screen = self.sm.get_screen('menu')
        menu_screen.ids.nomor_meja_input.text = str(self.nomor_meja)
        return self.sm

    def populate_menus(self): # Mengisi daftar menu makanan dan minuman di UI berdasarkan data yang ada
        menu_screen = self.sm.get_screen('menu')
        food_menu_layout = menu_screen.ids.food_menu_layout
        drink_menu_layout = menu_screen.ids.drink_menu_layout

        food_menu_layout.clear_widgets()
        for index, (key, item_details) in enumerate(makanan_data.items()):
            bg_color = (1, 1, 1, 1) if index % 2 == 0 else (0.88, 0.88, 0.88, 1)
            # 'id' dan 'type' ditambahkan ke item_data untuk digunakan oleh fungsi edit/hapus
            item_widget = MenuListItem(item_data={**item_details, 'id': key, 'type': 'food'},
                                       background_color=bg_color)
            food_menu_layout.add_widget(item_widget)

        drink_menu_layout.clear_widgets()
        for index, (key, item_details) in enumerate(minuman_data.items()):
            bg_color = (1, 1, 1, 1) if index % 2 == 0 else (0.88, 0.88, 0.88, 1)
            item_widget = MenuListItem(item_data={**item_details, 'id': key, 'type': 'drink'},
                                       background_color=bg_color)
            drink_menu_layout.add_widget(item_widget)

    def add_to_cart(self, item_data, quantity_input_widget): # Menambahkan item menu ke keranjang belanja
        quantity_str = quantity_input_widget.text
        if not quantity_str.isdigit() or int(quantity_str) <= 0:
            self.show_message_popup("Kesalahan Input", "Masukkan jumlah yang valid (angka > 0).")
            quantity_input_widget.text = ""
            return

        quantity = int(quantity_str)
        item_name = item_data['nama']

        existing_item = next((item for item in self.cart if item['nama'] == item_name), None)
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.cart.append({**item_data, 'quantity': quantity})

        self.update_cart_display()
        quantity_input_widget.text = "" # Kosongkan input setelah ditambahkan

    def remove_from_cart(self, item_to_remove_ref): # Menghapus item dari keranjang belanja
        if item_to_remove_ref in self.cart:
            self.cart.remove(item_to_remove_ref)
            self.update_cart_display()

    def update_cart_display(self): # Memperbarui tampilan keranjang belanja di UI (daftar item dan total harga)
        cart_screen = self.sm.get_screen('cart')
        cart_items_layout = cart_screen.ids.cart_items_layout
        cart_items_layout.clear_widgets()

        current_total = 0
        for index, cart_item_data in enumerate(self.cart):
            subtotal = cart_item_data['harga'] * cart_item_data['quantity']
            current_total += subtotal
            bg_color = (1, 1, 1, 1) if index % 2 == 0 else (0.88, 0.88, 0.88, 1)
            item_widget = CartItem(item_data_ref=cart_item_data, background_color=bg_color)
            cart_items_layout.add_widget(item_widget)

        self.total_cart_price = current_total
        cart_screen.ids.total_cart_label.text = f"Total: Rp. {self.total_cart_price:,}"

    def update_nomor_meja(self, text_input_value):# Memperbarui nomor meja berdasarkan input pengguna
        if text_input_value.isdigit():
            self.nomor_meja = int(text_input_value)
        else:
            # Jika input tidak valid, kembalikan ke nilai nomor meja sebelumnya
            menu_screen = self.sm.get_screen('menu')
            menu_screen.ids.nomor_meja_input.text = str(self.nomor_meja)
            self.show_message_popup("Info", "Nomor meja harus berupa angka.")

    def prepare_payment(self): # Mempersiapkan layar pembayaran, menampilkan total yang harus dibayar
        if not self.cart:
            self.show_message_popup("Info", "Keranjang belanja kosong. Silakan tambah item terlebih dahulu.")
            self.sm.current = 'menu' # Kembali ke menu jika keranjang kosong
            return

        payment_screen = self.sm.get_screen('payment')
        payment_screen.ids.payment_total_label.text = f"Total Bayar: Rp. {self.total_cart_price:,}"
        payment_screen.ids.amount_paid_input.text = "" # Kosongkan input pembayaran
        self.sm.current = 'payment'

    def process_payment(self, amount_paid_str): # Memproses pembayaran, menghitung kembalian, dan membuat struk
        if not amount_paid_str.isdigit():
            self.show_message_popup("Kesalahan Input", "Masukkan jumlah pembayaran yang valid.")
            return

        amount_paid = int(amount_paid_str)
        if amount_paid < self.total_cart_price:
            self.show_message_popup("Pembayaran Kurang", "Uang yang dibayarkan kurang dari total belanja.")
            return

        kembalian = amount_paid - self.total_cart_price
        self.generate_receipt(amount_paid, kembalian)
        self.sm.current = 'receipt'

    def _format_items_purchased(self): # Memformat detail item yang dibeli menjadi string untuk disimpan di CSV
        items_str_list = []
        for item in self.cart:
            nama = item['nama']
            quantity = item['quantity']
            harga_satuan = item['harga']
            subtotal = harga_satuan * quantity
            items_str_list.append(
                f"{nama} (Qty: {quantity}, Harga: {harga_satuan:,}, Subtotal: {subtotal:,})")
        return "; ".join(items_str_list)

    def save_transaction_to_csv(self, amount_paid, kembalian_value): # Menyimpan detail transaksi ke file CSV

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nomor_meja_val = self.nomor_meja
        total_belanja = self.total_cart_price
        items_purchased_str = self._format_items_purchased()

        data_row = [
            timestamp,
            nomor_meja_val,
            total_belanja,
            amount_paid,
            kembalian_value,
            items_purchased_str
        ]

        file_exists = os.path.exists(self.TRANSACTIONS_FILE)
        is_empty = file_exists and os.path.getsize(self.TRANSACTIONS_FILE) == 0

        try:
            with open(self.TRANSACTIONS_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists or is_empty:
                    header = ['Timestamp', 'NomorMeja', 'TotalBelanja', 'Dibayar', 'Kembalian', 'DetailPesanan']
                    writer.writerow(header)
                writer.writerow(data_row)
        except IOError as e:
            self.show_message_popup("Error Penyimpanan", f"Gagal menyimpan transaksi: {e}")

    def generate_receipt(self, amount_paid, kembalian): # Membuat dan menampilkan struk pembelian di UI
        receipt_screen = self.sm.get_screen('receipt')

        menu_screen = self.sm.get_screen('menu')
        nomor_meja_input_text = menu_screen.ids.nomor_meja_input.text
        if nomor_meja_input_text.isdigit(): # Pastikan nomor meja terbaru yang diambil
            self.nomor_meja = int(nomor_meja_input_text)

        self.save_transaction_to_csv(amount_paid, kembalian)

        header_line = f"{'Menu':<18} {'Qty':<5} {'Harga':>10} {'Subtotal':>12}"
        divider = "=" * len(header_line)

        receipt_lines = [
            divider,
            "          STRUK PEMBELIAN        ",
            divider,
            f"Nomor Meja: {self.nomor_meja}",
            divider,
            header_line,
            "-" * len(header_line)
        ]

        for item in self.cart:
            nama = item['nama']
            if len(nama) > 17:
                nama = nama[:15] + ".."
            harga_satuan = item['harga']
            subtotal_item = item['harga'] * item['quantity']
            receipt_lines.append(
                f"{nama:<18} {item['quantity']:<5} {harga_satuan:>10,} {subtotal_item:>12,}")

        receipt_lines.extend([
            divider,
            f"{'Total Harga:':<30} Rp.{self.total_cart_price:>12,}",
            f"{'Dibayar:':<30} Rp.{amount_paid:>12,}",
            f"{'Kembalian:':<30} Rp.{kembalian:>12,}",
            divider,
            "        Terima kasih atas kunjungan Anda!   ",
            divider
        ])
        receipt_screen.ids.receipt_text_label.text = "\n".join(receipt_lines)

    def start_new_order(self): # Memulai pesanan baru, mengosongkan keranjang dan mereset tampilan
        self.cart = []
        self.total_cart_price = 0
        self.update_cart_display()

        payment_screen = self.sm.get_screen('payment')
        if payment_screen and 'amount_paid_input' in payment_screen.ids:
            payment_screen.ids.amount_paid_input.text = ""

        self.sm.current = 'menu'

    def show_message_popup(self, title, message, on_dismiss_callback=None): # Menampilkan popup pesan kepada pengguna
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self._dismiss_dialog_and_callback(dialog, on_dismiss_callback))],
        )
        dialog.open()

    def _dismiss_dialog_and_callback(self, dialog_instance, callback): # Menutup dialog pesan dan menjalankan callback jika ada
        dialog_instance.dismiss()
        dialog_instance.dismiss()
        if callback:
            callback()

    def _get_next_id(self, data_dict): # Mendapatkan ID unik berikutnya untuk item menu baru
        if not data_dict:
            return 1
        return max(data_dict.keys()) + 1

    def open_add_item_dialog(self, item_type): # Membuka dialog untuk menambahkan item menu baru (makanan atau minuman) # item_type bisa 'food' atau 'drink'
        if self.add_item_dialog:
            self.add_item_dialog.dismiss()

        content_cls = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, adaptive_height=True)
        name_field = MDTextField(hint_text="Nama Item")
        price_field = MDTextField(hint_text="Harga Item", input_filter="int")
        content_cls.add_widget(name_field)
        content_cls.add_widget(price_field)

        self.add_item_dialog = MDDialog(
            title=f"Tambah Item Baru",
            type="custom",
            content_cls=content_cls,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.add_item_dialog.dismiss()),
                MDRaisedButton(text="TAMBAH",
                               on_release=lambda x: self._save_new_item(item_type, name_field.text, price_field.text)),
            ],
        )
        self.add_item_dialog.open()

    def _save_new_item(self, item_type, name, price_str): # Menyimpan item menu baru yang ditambahkan melalui dialog
        if not name or not price_str:
            self.show_message_popup("Error", "Nama dan Harga tidak boleh kosong.")
            return
        try:
            price = int(price_str)
            if price <= 0:
                self.show_message_popup("Error", "Harga harus angka positif.")
                return
        except ValueError:
            self.show_message_popup("Error", "Harga harus berupa angka.")
            return

        data_dict = makanan_data if item_type == 'food' else minuman_data
        new_id = self._get_next_id(data_dict)
        data_dict[new_id] = {'nama': name, 'harga': price}

        self.populate_menus()
        if self.add_item_dialog:
            self.add_item_dialog.dismiss()
            self.save_menu_data() #save perubahan
        self.show_message_popup("Sukses", f"Item '{name}' berhasil ditambahkan.")

    def open_edit_item_dialog(self, item_data): # Membuka dialog untuk mengedit item menu yang sudah ada
        if self.edit_item_dialog:
            self.edit_item_dialog.dismiss()

        content_cls = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, adaptive_height=True)
        name_field = MDTextField(text=item_data['nama'], hint_text="Nama Item")
        price_field = MDTextField(text=str(item_data['harga']), hint_text="Harga Item", input_filter="int")
        content_cls.add_widget(name_field)
        content_cls.add_widget(price_field)

        self.edit_item_dialog = MDDialog(
            title=f"Edit Item: {item_data['nama']}",
            type="custom",
            content_cls=content_cls,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.edit_item_dialog.dismiss()),
                MDRaisedButton(text="SIMPAN",
                               on_release=lambda x: self._save_edited_item(item_data, name_field.text, price_field.text)),
            ],
        )
        self.edit_item_dialog.open()

    def _save_edited_item(self, original_item_data, new_name, new_price_str): # Menyimpan perubahan pada item menu yang diedit
        if not new_name or not new_price_str:
            self.show_message_popup("Error", "Nama dan Harga tidak boleh kosong.")
            return
        try:
            new_price = int(new_price_str)
            if new_price <= 0:
                self.show_message_popup("Error", "Harga harus angka positif.")
                return
        except ValueError:
            self.show_message_popup("Error", "Harga harus berupa angka.")
            return

        item_id = original_item_data['id']
        item_type = original_item_data['type']

        data_dict = makanan_data if item_type == 'food' else minuman_data

        if item_id in data_dict:
            data_dict[item_id]['nama'] = new_name
            data_dict[item_id]['harga'] = new_price
            self.populate_menus()
            if self.edit_item_dialog:
                self.edit_item_dialog.dismiss()
                self.save_menu_data() #save perubahan
            self.show_message_popup("Sukses", f"Item '{original_item_data['nama']}' berhasil diupdate.")
        else:
            self.show_message_popup("Error", "Item tidak ditemukan untuk diedit.")

    def open_confirm_remove_dialog(self, item_data): # Membuka dialog konfirmasi sebelum menghapus item menu
        if self.remove_item_dialog:
            self.remove_item_dialog.dismiss()

        self.remove_item_dialog = MDDialog(
            title="Konfirmasi Hapus",
            text=f"Apakah Anda yakin ingin menghapus item '{item_data['nama']}'?",
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.remove_item_dialog.dismiss()),
                MDRaisedButton(text="HAPUS", md_bg_color=self.theme_cls.error_color,
                               on_release=lambda x: self._execute_remove_item(item_data)),
            ],
        )
        self.remove_item_dialog.open()

    def _execute_remove_item(self, item_data_to_remove): # Melakukan proses penghapusan item menu dari data dan UI
        item_id = item_data_to_remove['id']
        item_type = item_data_to_remove['type']
        item_name = item_data_to_remove['nama']

        data_dict = makanan_data if item_type == 'food' else minuman_data

        if item_id in data_dict:
            del data_dict[item_id]
            self.populate_menus()
            if self.remove_item_dialog:
                self.remove_item_dialog.dismiss()
                self.save_menu_data() #save perubahan
            self.show_message_popup("Sukses", f"Item '{item_name}' berhasil dihapus.")
        else:
            self.show_message_popup("Error", "Item tidak ditemukan untuk dihapus.")


if __name__ == '__main__':
    SotoKivApp().run()
