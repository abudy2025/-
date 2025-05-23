# Main application file for the Accounting App
# GUI Framework: Tkinter
# PDF Generation: ReportLab

import tkinter as tk
from tkinter import ttk # For better widget styling if needed later
from tkinter import messagebox # For error dialogs
import json
import os

# --- Constants for Data Files ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, "data") 
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")
INVOICES_FILE = os.path.join(DATA_DIR, "invoices.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")

# --- Helper Functions for JSON Data Persistence ---
def ensure_data_dir_exists():
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
            print(f"Data directory created at: {DATA_DIR}")
        except OSError as e:
            print(f"Error creating data directory {DATA_DIR}: {e}")
            return False
    return True

def save_data_to_json(data, filename):
    if not ensure_data_dir_exists():
        messagebox.showerror("خطأ في الحفظ", f"لم يتمكن من إنشاء مجلد البيانات. لن يتم حفظ الملف {os.path.basename(filename)}.")
        return False 
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data saved successfully to {filename}") 
        return True 
    except IOError as e:
        print(f"IOError saving data to {filename}: {e}")
        messagebox.showerror("خطأ في الحفظ", f"حدث خطأ أثناء حفظ الملف {os.path.basename(filename)}:\n{e}")
        return False
    except Exception as e: 
        print(f"Unexpected error saving data to {filename}: {e}")
        messagebox.showerror("خطأ غير متوقع", f"حدث خطأ غير متوقع أثناء حفظ الملف {os.path.basename(filename)}:\n{e}")
        return False

def load_data_from_json(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found. Returning empty list.") 
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Data loaded successfully from {filename}") 
            return data
    except FileNotFoundError: 
        print(f"FileNotFoundError: {filename}. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError loading data from {filename}: {e}. Returning empty list.")
        messagebox.showwarning("ملف تالف", f"الملف {os.path.basename(filename)} تالف أو لا يحتوي على بيانات JSON صالحة.\nسيتم البدء بقائمة فارغة.")
        return []
    except Exception as e: 
        print(f"Unexpected error loading data from {filename}: {e}. Returning empty list.")
        messagebox.showwarning("خطأ غير متوقع", f"حدث خطأ غير متوقع أثناء تحميل الملف {os.path.basename(filename)}.\nسيتم البدء بقائمة فارغة.")
        return []

class LoginWindow:
    # ... (LoginWindow class remains unchanged) ...
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        master.title("تسجيل الدخول")
        master.geometry("300x150")
        master.resizable(False, False) 

        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'{width}x{height}+{x}+{y}')

        self.frame = ttk.Frame(master, padding="10 10 10 10")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.username_label = ttk.Label(self.frame, text="اسم المستخدم:")
        self.username_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.username_entry = ttk.Entry(self.frame, justify=tk.RIGHT)
        self.username_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

        self.password_label = ttk.Label(self.frame, text="كلمة المرور:")
        self.password_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self.frame, show="*", justify=tk.RIGHT)
        self.password_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        self.login_button = ttk.Button(self.frame, text="دخول", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.frame.columnconfigure(0, weight=1)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Attempting login with Username: {username}, Password: {password}") 
        self.master.destroy() 
        self.on_login_success() 

def open_main_application():
    root = tk.Tk()
    root.title("برنامج المحاسبة الرئيسي")
    root.geometry("800x600")

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="جديد", command=lambda: print("Action: New")) 
    file_menu.add_separator()
    file_menu.add_command(label="خروج", command=root.quit)
    menubar.add_cascade(label="ملف", menu=file_menu)
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="تفضيلات", command=lambda: print("Action: Preferences")) 
    menubar.add_cascade(label="اعدادات", menu=settings_menu)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="حول البرنامج", command=lambda: print("Action: About")) 
    menubar.add_cascade(label="مساعده", menu=help_menu)
    
    button_frame = ttk.Frame(root, padding="20 20 20 20")
    main_content_frame = ttk.Frame(root)
    main_content_frame.pack(expand=True, fill=tk.BOTH)
    button_frame.pack(in_=main_content_frame, expand=True, fill=tk.BOTH) 

    new_invoice_frame = None
    add_stock_frame = None 
    view_report_frame = None 
    operations_archive_frame = None 
    
    inventory_treeview_widget = None 
    ensure_data_dir_exists() 
    inventory_products_list = load_data_from_json(INVENTORY_FILE)
    saved_invoices_list = load_data_from_json(INVOICES_FILE)
    customers_list = load_data_from_json(CUSTOMERS_FILE)
    
    invoice_items_treeview_widget_ref = None 
    subtotal_label_ref = None
    tax_label_ref = None
    grand_total_label_ref = None
    
    invoice_number_label_ref = None 
    customer_name_entry_ref = None
    customer_phone_entry_ref = None
    customer_tax_entry_ref = None
    company_details_entries_ref = {} 

    invoice_counter = 0 
    if saved_invoices_list:
        for inv in saved_invoices_list:
            if inv.get("invoice_number","").isdigit():
                num = int(inv["invoice_number"])
                if num > invoice_counter: invoice_counter = num
    
    product_barcode_counter = 0 
    if inventory_products_list:
        for prod in inventory_products_list:
            if prod.get("barcode","").startswith("AUTOGEN-"):
                try:
                    num = int(prod["barcode"].split("-")[-1])
                    if num > product_barcode_counter: product_barcode_counter = num
                except ValueError: pass 

    def validate_numeric_input(P): 
        if P == "" or P.isdigit(): return True
        return False
    vcmd_numeric_only = (root.register(validate_numeric_input), '%P')

    def validate_float_input(P): 
        if P == "": return True
        try:
            float(P)
            if P.count('.') > 1: return False
            return True
        except ValueError:
            if P == "." or (P.count('.') == 1 and P.replace('.', '').isdigit()): return True
            return False
    vcmd_float = (root.register(validate_float_input), '%P')

    def validate_integer_input(P): return validate_numeric_input(P)
    vcmd_integer = (root.register(validate_integer_input), '%P')

    def update_invoice_totals():
        nonlocal invoice_items_treeview_widget_ref, subtotal_label_ref, tax_label_ref, grand_total_label_ref
        total_before_tax = 0.0
        if invoice_items_treeview_widget_ref:
            for item_id in invoice_items_treeview_widget_ref.get_children(""):
                item_values = invoice_items_treeview_widget_ref.item(item_id, 'values')
                try: total_before_tax += float(item_values[0])
                except (IndexError, ValueError): print(f"Warning: Could not parse subtotal for item {item_id}. Values: {item_values}")
        tax_rate = 0.15; tax_amount = total_before_tax * tax_rate; grand_total = total_before_tax + tax_amount
        if subtotal_label_ref: subtotal_label_ref.config(text=f"{total_before_tax:.2f}")
        if tax_label_ref: tax_label_ref.config(text=f"{tax_amount:.2f}")
        if grand_total_label_ref: grand_total_label_ref.config(text=f"{grand_total:.2f}")

    def show_main_module_buttons():
        nonlocal new_invoice_frame, add_stock_frame, view_report_frame, operations_archive_frame
        if new_invoice_frame: new_invoice_frame.destroy(); new_invoice_frame = None
        if add_stock_frame: add_stock_frame.destroy(); add_stock_frame = None
        if view_report_frame: view_report_frame.destroy(); view_report_frame = None
        if operations_archive_frame: operations_archive_frame.destroy(); operations_archive_frame = None
        for child in main_content_frame.winfo_children():
            if child != button_frame : child.pack_forget()
        button_frame.pack(expand=True, fill=tk.BOTH) 
    
    def renumber_invoice_items(treeview):
        if not treeview: return
        all_item_ids = treeview.get_children("") 
        for idx, item_id in enumerate(all_item_ids):
            new_seq_no = idx + 1; current_values = list(treeview.item(item_id, 'values'))
            if len(current_values) == 5: current_values[4] = str(new_seq_no); treeview.item(item_id, values=tuple(current_values))

    def delete_selected_invoice_item(treeview):
        nonlocal new_invoice_frame 
        parent_window = new_invoice_frame if new_invoice_frame and new_invoice_frame.winfo_exists() else root
        if not treeview: messagebox.showerror("خطأ", "جدول الفاتورة غير متاح.", parent=parent_window); return
        selected_items = treeview.selection()
        if not selected_items: messagebox.showinfo("لا يوجد تحديد", "يرجى تحديد صنف لحذفه.", parent=parent_window); return
        item_to_delete = selected_items[0] 
        if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف الصنف المحدد؟", parent=parent_window): 
            treeview.delete(item_to_delete); renumber_invoice_items(treeview); update_invoice_totals() 
    
    def open_add_invoice_item_popup():
        nonlocal invoice_items_treeview_widget_ref, new_invoice_frame, inventory_products_list
        parent_window = new_invoice_frame if new_invoice_frame and new_invoice_frame.winfo_exists() else root

        if not invoice_items_treeview_widget_ref:
            messagebox.showerror("خطأ", "جدول الفاتورة غير متاح.", parent=parent_window)
            return

        popup_window = tk.Toplevel(root)
        popup_window.title("إضافة صنف للفاتورة")
        popup_window.resizable(False, False)
        popup_window.grab_set()

        popup_width = 350; popup_height = 220 # Adjusted for combobox
        x_cordinate = int((root.winfo_screenwidth()/2)-(popup_width/2)); y_cordinate = int((root.winfo_screenheight()/2)-(popup_height/2))
        popup_window.geometry(f"{popup_width}x{popup_height}+{x_cordinate}+{y_cordinate}")

        popup_frame = ttk.Frame(popup_window, padding="15 15 15 15"); popup_frame.pack(expand=True, fill=tk.BOTH)

        selected_product_barcode = tk.StringVar() # To store barcode of selected inventory item

        ttk.Label(popup_frame, text="الصنف/الخدمة:").grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        product_names = [p.get("name", "") for p in inventory_products_list]
        item_name_combobox = ttk.Combobox(popup_frame, values=product_names, state="readonly", justify=tk.RIGHT)
        item_name_combobox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        
        item_price_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float) # Define early for on_select

        def on_product_select(event):
            nonlocal selected_product_barcode # To store barcode of selected inventory item
            selected_name = item_name_combobox.get()
            for product in inventory_products_list:
                if product.get("name") == selected_name:
                    item_price_entry.delete(0, tk.END)
                    item_price_entry.insert(0, str(product.get("selling_price", "0.00")))
                    selected_product_barcode.set(product.get("barcode", "")) # Store barcode
                    return
            selected_product_barcode.set("") # Clear if not found (e.g. combobox cleared)
            item_price_entry.delete(0, tk.END)


        item_name_combobox.bind("<<ComboboxSelected>>", on_product_select)

        ttk.Label(popup_frame, text="الكمية:").grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        item_qty_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_integer)
        item_qty_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(popup_frame, text="سعر الوحدة:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        item_price_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        
        popup_frame.columnconfigure(0, weight=1)

        def submit_item():
            nonlocal selected_product_barcode
            name = item_name_combobox.get().strip()
            qty_str = item_qty_entry.get().strip()
            price_str = item_price_entry.get().strip()
            barcode = selected_product_barcode.get() if selected_product_barcode.get() else "N/A"


            if not all([name, qty_str, price_str]): messagebox.showerror("خطأ في الإدخال", "يرجى ملء جميع الحقول.", parent=popup_window); return
            try:
                qty = int(qty_str); price = float(price_str)
                if qty <= 0 or price < 0: messagebox.showerror("خطأ في الإدخال", "الكمية يجب أن تكون أكبر من صفر والسعر يجب أن يكون موجباً.", parent=popup_window); return
            except ValueError: messagebox.showerror("خطأ في الإدخال", "يرجى إدخال قيم رقمية صحيحة للكمية والسعر.", parent=popup_window); return
            
            subtotal = qty * price
            seq_no = len(invoice_items_treeview_widget_ref.get_children()) + 1
            
            # The values tuple for Treeview does not change, barcode is handled during save_invoice
            values = (f"{subtotal:.2f}", f"{price:.2f}", qty, name, seq_no)
            # Store barcode with the item, not directly in treeview columns but conceptually
            # This means save_invoice needs to be aware of how to get this barcode.
            # For now, we'll print it to show it's captured.
            print(f"Adding item to invoice: {values}, Barcode: {barcode}")
            
            # We need a way to associate the barcode with the treeview item if it's not a column
            # One simple way is to use item tags or a separate dictionary mapping treeview item ID to barcode
            # For now, the task is to capture it; actual storage strategy for save_invoice is next.
            # This item_id can be used to store more data if needed:
            item_tree_id = invoice_items_treeview_widget_ref.insert("", tk.END, values=values)
            # Example: invoice_items_treeview_widget_ref.item(item_tree_id, tags=(barcode,))
            # Or maintain a separate dict: item_barcodes[item_tree_id] = barcode

            update_invoice_totals(); popup_window.destroy()

        add_button = ttk.Button(popup_frame, text="إضافة", command=submit_item)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)
        popup_window.protocol("WM_DELETE_WINDOW", lambda: (popup_window.destroy()))
    
    def add_customer():
        nonlocal customers_list, customer_name_entry_ref, customer_phone_entry_ref, customer_tax_entry_ref, new_invoice_frame
        parent_window = new_invoice_frame if new_invoice_frame and new_invoice_frame.winfo_exists() else root
        customer_name = customer_name_entry_ref.get().strip() if customer_name_entry_ref else ""
        customer_phone = customer_phone_entry_ref.get().strip() if customer_phone_entry_ref else ""
        customer_tax = customer_tax_entry_ref.get().strip() if customer_tax_entry_ref else ""
        if not customer_name: messagebox.showwarning("بيانات ناقصة", "الرجاء إدخال اسم العميل.", parent=parent_window); return
        customer_data = {"name": customer_name, "phone": customer_phone, "tax_number": customer_tax}
        customers_list.append(customer_data); save_data_to_json(customers_list, CUSTOMERS_FILE) 
        print(f"Customer added: {customer_data}"); print(f"All customers: {customers_list}") 
        messagebox.showinfo("تمت الإضافة", f"تمت إضافة العميل: {customer_name}", parent=parent_window)

    def save_invoice():
        nonlocal saved_invoices_list, invoice_number_label_ref, customer_name_entry_ref, \
               customer_phone_entry_ref, customer_tax_entry_ref, company_details_entries_ref, \
               invoice_items_treeview_widget_ref, subtotal_label_ref, tax_label_ref, grand_total_label_ref, \
               new_invoice_frame 
        
        parent_window = new_invoice_frame if new_invoice_frame and new_invoice_frame.winfo_exists() else root
        if not invoice_items_treeview_widget_ref or not invoice_items_treeview_widget_ref.get_children(""):
            messagebox.showwarning("الفاتورة فارغة", "يرجى إضافة أصناف قبل حفظ الفاتورة.", parent=parent_window); return
        
        # TODO: Later, retrieve barcode associated with each treeview item for saving.
        # For now, the barcode is printed in submit_item but not yet structurally saved with the row for save_invoice.
        
        invoice_data = {
            "invoice_number": invoice_number_label_ref.cget("text") if invoice_number_label_ref else "N/A",
            "customer_details": {"name": customer_name_entry_ref.get() if customer_name_entry_ref else "", "phone": customer_phone_entry_ref.get() if customer_phone_entry_ref else "", "tax_number": customer_tax_entry_ref.get() if customer_tax_entry_ref else ""},
            "company_details": {key: entry.get() for key, entry in company_details_entries_ref.items()}, "items": [],
            "totals": {"subtotal": subtotal_label_ref.cget("text") if subtotal_label_ref else "0.00", "tax": tax_label_ref.cget("text") if tax_label_ref else "0.00", "grand_total": grand_total_label_ref.cget("text") if grand_total_label_ref else "0.00"}
        }
        for item_id in invoice_items_treeview_widget_ref.get_children(""):
            item_values = invoice_items_treeview_widget_ref.item(item_id, 'values')
            # This is where barcode would be retrieved if stored with item, e.g., using tags or a lookup dict
            invoice_data["items"].append({"subtotal": item_values[0], "unit_price": item_values[1], "quantity": item_values[2], "item_service": item_values[3], "seq_no": item_values[4], "barcode": "BARCODE_PLACEHOLDER"}) # Placeholder
        saved_invoices_list.append(invoice_data); save_data_to_json(saved_invoices_list, INVOICES_FILE) 
        print(f"Invoice Saved: {invoice_data['invoice_number']}"); print(f"All saved invoices: {len(saved_invoices_list)}") 
        messagebox.showinfo("تم الحفظ", f"تم حفظ الفاتورة رقم: {invoice_data['invoice_number']}", parent=parent_window)

    def show_new_invoice_page():
        nonlocal new_invoice_frame, invoice_counter, add_stock_frame, view_report_frame, operations_archive_frame, \
               invoice_items_treeview_widget_ref, subtotal_label_ref, tax_label_ref, grand_total_label_ref, \
               invoice_number_label_ref, customer_name_entry_ref, customer_phone_entry_ref, customer_tax_entry_ref, \
               company_details_entries_ref
        
        if add_stock_frame: add_stock_frame.destroy(); add_stock_frame = None
        if view_report_frame: view_report_frame.destroy(); view_report_frame = None
        if operations_archive_frame: operations_archive_frame.destroy(); operations_archive_frame = None
        if new_invoice_frame: new_invoice_frame.destroy() 
        button_frame.pack_forget()

        current_max_invoice_num = 0
        if saved_invoices_list:
            for inv in saved_invoices_list:
                if inv.get("invoice_number","").isdigit():
                    num = int(inv["invoice_number"])
                    if num > current_max_invoice_num:
                        current_max_invoice_num = num
        invoice_counter = current_max_invoice_num + 1 # Set to next available
        
        formatted_invoice_number = f"{invoice_counter:03d}"
        new_invoice_frame = ttk.Frame(main_content_frame, padding="10 10 10 10")
        new_invoice_frame.pack(expand=True, fill=tk.BOTH)
        new_invoice_frame.columnconfigure(0, weight=3); new_invoice_frame.columnconfigure(1, weight=1) 
        new_invoice_frame.rowconfigure(0, weight=1); new_invoice_frame.rowconfigure(1, weight=0); new_invoice_frame.rowconfigure(2, weight=0) 

        left_pane = ttk.Frame(new_invoice_frame); left_pane.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_pane.columnconfigure(0, weight=1) 
        ttk.Label(left_pane, text="فاتورة جديده", font=('Helvetica', 18, 'bold')).grid(row=0, column=0, pady=10, sticky="ne")
        company_details_frame = ttk.LabelFrame(left_pane, text="بيانات الشركة", padding="10 10 10 10")
        company_details_frame.grid(row=1, column=0, pady=10, padx=5, sticky="ew")
        company_details_frame.columnconfigure(0, weight=1); company_details_frame.columnconfigure(1, weight=0) 
        company_details_entries_ref.clear() 
        fields_data = [("name", "اسم الشركة:"), ("tax_no", "الرقم الضريبي للشركة:"), ("phone", "هاتف الشركة:"), ("email", "البريد الالكتروني للشركة:"), ("address", "عنوان الشركة:")]
        for i, (k, t) in enumerate(fields_data): 
            ttk.Label(company_details_frame, text=t).grid(row=i, column=1, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(company_details_frame, justify=tk.RIGHT); entry.grid(row=i, column=0, padx=5, pady=5, sticky=tk.EW)
            company_details_entries_ref[k] = entry
        def _pc(): print("--- Company Details ---"); [print(f"{k.replace('_',' ').title()}: {v.get()}") for k,v in company_details_entries_ref.items()]; print("---")
        ttk.Button(company_details_frame, text="حفظ بيانات الشركة", command=_pc).grid(row=len(fields_data), column=0, columnspan=2, pady=10)

        invoice_items_tree_frame = ttk.Frame(left_pane); invoice_items_tree_frame.grid(row=2, column=0, pady=(10,5), sticky="nsew") 
        invoice_items_tree_frame.columnconfigure(0, weight=1); invoice_items_tree_frame.rowconfigure(0, weight=1) 
        invoice_columns = ("col_item_subtotal", "col_unit_price", "col_qty", "col_item_service", "col_seq")
        invoice_items_treeview_widget_ref = ttk.Treeview(invoice_items_tree_frame, columns=invoice_columns, show="headings")
        hds = [("col_seq", "م"), ("col_item_service", "الصنف/الخدمة"), ("col_qty", "الكمية"), ("col_unit_price", "سعر الوحدة"), ("col_item_subtotal", "الإجمالي الفرعي")]
        w_a_s = [("col_seq", 50, tk.CENTER, tk.NO), ("col_item_service", 250, tk.E, tk.YES), ("col_qty", 80, tk.CENTER, tk.YES), ("col_unit_price", 100, tk.CENTER, tk.YES), ("col_item_subtotal", 120, tk.CENTER, tk.YES)]
        for c, t in hds: invoice_items_treeview_widget_ref.heading(c, text=t)
        for c, w, a, s in w_a_s: invoice_items_treeview_widget_ref.column(c, width=w, anchor=a, stretch=s)
        inv_v_scrl = ttk.Scrollbar(invoice_items_tree_frame, orient=tk.VERTICAL, command=invoice_items_treeview_widget_ref.yview); invoice_items_treeview_widget_ref.configure(yscrollcommand=inv_v_scrl.set)
        inv_h_scrl = ttk.Scrollbar(invoice_items_tree_frame, orient=tk.HORIZONTAL, command=invoice_items_treeview_widget_ref.xview); invoice_items_treeview_widget_ref.configure(xscrollcommand=inv_h_scrl.set)
        inv_v_scrl.grid(row=0, column=1, sticky="ns"); inv_h_scrl.grid(row=1, column=0, sticky="ew"); invoice_items_treeview_widget_ref.grid(row=0, column=0, sticky="nsew")
        
        invoice_items_buttons_frame = ttk.Frame(left_pane); invoice_items_buttons_frame.grid(row=3, column=0, pady=5, sticky="e") 
        ttk.Button(invoice_items_buttons_frame, text="إضافة صنف", command=open_add_invoice_item_popup).pack(side=tk.RIGHT, padx=5)
        ttk.Button(invoice_items_buttons_frame, text="حذف الصنف", command=lambda: delete_selected_invoice_item(invoice_items_treeview_widget_ref)).pack(side=tk.RIGHT, padx=5)
        left_pane.rowconfigure(0, weight=0); left_pane.rowconfigure(1, weight=0); left_pane.rowconfigure(2, weight=1); left_pane.rowconfigure(3, weight=0) 

        customer_info_frame = ttk.LabelFrame(new_invoice_frame, text="بيانات العميل", padding="10 10 10 10")
        customer_info_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ttk.Label(customer_info_frame, text="الرقم التسلسلي:").grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        invoice_number_label_ref = ttk.Label(customer_info_frame, text=formatted_invoice_number) 
        invoice_number_label_ref.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(customer_info_frame, text="اسم العميل:").grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        customer_name_entry_ref = ttk.Entry(customer_info_frame, justify=tk.RIGHT) 
        customer_name_entry_ref.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(customer_info_frame, text="رقم هاتف:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        customer_phone_entry_ref = ttk.Entry(customer_info_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_numeric_only) 
        customer_phone_entry_ref.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(customer_info_frame, text="الرقم الضريبي:").grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        customer_tax_entry_ref = ttk.Entry(customer_info_frame, justify=tk.RIGHT) 
        customer_tax_entry_ref.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(customer_info_frame, text="إضافة عميل", command=add_customer).grid(row=4, column=0, columnspan=2, pady=10) 
        customer_info_frame.columnconfigure(0, weight=1); customer_info_frame.rowconfigure(5, weight=1) 

        totals_frame = ttk.LabelFrame(new_invoice_frame, text="الإجماليات", padding="10 10 10 10")
        totals_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10) 
        totals_frame.columnconfigure(0, weight=1); totals_frame.columnconfigure(1, weight=0) 
        ttk.Label(totals_frame, text="الإجمالي من غير الضريبة:").grid(row=0, column=1, padx=5, pady=2, sticky=tk.E)
        subtotal_label_ref = ttk.Label(totals_frame, text="0.00"); subtotal_label_ref.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(totals_frame, text="الضريبة:").grid(row=1, column=1, padx=5, pady=2, sticky=tk.E)
        tax_label_ref = ttk.Label(totals_frame, text="0.00"); tax_label_ref.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(totals_frame, text="الإجمالي مع الضريبة:").grid(row=2, column=1, padx=5, pady=2, sticky=tk.E)
        grand_total_label_ref = ttk.Label(totals_frame, text="0.00"); grand_total_label_ref.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)

        bottom_actions_frame = ttk.Frame(new_invoice_frame, padding="5 5 5 5")
        bottom_actions_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        for i in [0,5]: bottom_actions_frame.columnconfigure(i, weight=1) 
        for i in range(1,5): bottom_actions_frame.columnconfigure(i, weight=0) 
        ttk.Button(bottom_actions_frame, text="طباعة", command=lambda: print("Action: Print Invoice")).grid(row=0, column=1, padx=5)
        ttk.Button(bottom_actions_frame, text="حفظ PDF", command=lambda: print("Action: Save as PDF")).grid(row=0, column=2, padx=5)
        ttk.Button(bottom_actions_frame, text="حفظ الفاتورة", command=save_invoice).grid(row=0, column=3, padx=5) 
        ttk.Button(bottom_actions_frame, text="رجوع", command=show_main_module_buttons).grid(row=0, column=4, padx=15) 
        
        if invoice_items_treeview_widget_ref: 
            for item in invoice_items_treeview_widget_ref.get_children(""):
                invoice_items_treeview_widget_ref.delete(item)
        update_invoice_totals() 


    def refresh_inventory_treeview():
        nonlocal inventory_treeview_widget, inventory_products_list
        if not inventory_treeview_widget: return
        for item in inventory_treeview_widget.get_children(): inventory_treeview_widget.delete(item)
        for product in inventory_products_list:
            try:
                quantity = float(product["quantity"]); selling_price = float(product["selling_price"])
                total_price = quantity * selling_price
            except ValueError: total_price = 0.0 
            values_tuple = (f"{product.get('tax_percent', 0.0):.2f}%", f"{total_price:.2f}", f"{product.get('selling_price', 0.0):.2f}", product.get("quantity", 0), product.get("name", ""), product.get("barcode", ""))
            inventory_treeview_widget.insert("", tk.END, values=values_tuple)

    def open_add_product_popup():
        nonlocal product_barcode_counter, inventory_products_list, new_invoice_frame
        parent_window = new_invoice_frame if new_invoice_frame and new_invoice_frame.winfo_exists() else root
        popup_window = tk.Toplevel(root); popup_window.title("إضافة منتج جديد")
        popup_window.resizable(False, False); popup_window.grab_set() 
        popup_width = 350; popup_height = 280 
        x_cordinate = int((root.winfo_screenwidth() / 2) - (popup_width / 2))
        y_cordinate = int((root.winfo_screenheight() / 2) - (popup_height / 2))
        popup_window.geometry(f"{popup_width}x{popup_height}+{x_cordinate}+{y_cordinate}")
        popup_frame = ttk.Frame(popup_window, padding="15 15 15 15"); popup_frame.pack(expand=True, fill=tk.BOTH)
        product_barcode_counter += 1; barcode_value = f"AUTOGEN-{product_barcode_counter:04d}"
        ttk.Label(popup_frame, text="باركود:").grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Label(popup_frame, text=barcode_value).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(popup_frame, text="اسم المنتج:").grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        product_name_entry = ttk.Entry(popup_frame, justify=tk.RIGHT)
        product_name_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(popup_frame, text="سعر الشراء:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        purchase_price_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        purchase_price_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(popup_frame, text="سعر البيع:").grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        selling_price_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        selling_price_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(popup_frame, text="الكميه:").grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        quantity_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_integer)
        quantity_entry.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(popup_frame, text="الضريبة (%):").grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)
        tax_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        tax_entry.insert(0, "15"); tax_entry.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW)
        popup_frame.columnconfigure(0, weight=1) 
        def submit_new_product():
            nonlocal inventory_products_list 
            name = product_name_entry.get().strip(); purchase_price_str = purchase_price_entry.get().strip()
            selling_price_str = selling_price_entry.get().strip(); quantity_str = quantity_entry.get().strip()
            tax_str = tax_entry.get().strip()
            if not all([name, purchase_price_str, selling_price_str, quantity_str, tax_str]):
                messagebox.showerror("خطأ في الإدخال", "يرجى ملء جميع الحقول.", parent=popup_window); return
            try:
                purchase_price = float(purchase_price_str); selling_price = float(selling_price_str)
                quantity = int(quantity_str); tax_percent = float(tax_str)
                if purchase_price < 0 or selling_price < 0 or quantity < 0 or tax_percent < 0:
                    messagebox.showerror("خطأ في الإدخال", "القيم الرقمية يجب أن تكون موجبة.", parent=popup_window); return
            except ValueError:
                messagebox.showerror("خطأ في الإدخال", "يرجى إدخال قيم رقمية صحيحة للأسعار والكمية والضريبة.", parent=popup_window); return
            product_data = {"barcode": barcode_value, "name": name, "purchase_price": purchase_price, "selling_price": selling_price, "quantity": quantity, "tax_percent": tax_percent}
            inventory_products_list.append(product_data)
            save_data_to_json(inventory_products_list, INVENTORY_FILE) 
            print(f"Product added: {product_data}") 
            refresh_inventory_treeview(); popup_window.destroy()
        submit_button = ttk.Button(popup_frame, text="إدخال", command=submit_new_product)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)
        popup_window.protocol("WM_DELETE_WINDOW", lambda: (popup_window.destroy())) 

    def open_modify_product_popup():
        nonlocal inventory_treeview_widget, inventory_products_list, add_stock_frame 
        parent_window = add_stock_frame if add_stock_frame and add_stock_frame.winfo_exists() else root

        if not inventory_treeview_widget:
            messagebox.showerror("خطأ", "جدول المخزون غير متاح.", parent=parent_window)
            return

        selected_items = inventory_treeview_widget.selection()
        if not selected_items:
            messagebox.showinfo("لا يوجد تحديد", "الرجاء اختيار منتج لتعديله.", parent=parent_window)
            return
        
        item_id = selected_items[0]
        item_values = inventory_treeview_widget.item(item_id, 'values')
        selected_barcode = item_values[5] 

        product_to_modify = None
        product_index = -1
        for index, product in enumerate(inventory_products_list):
            if product.get("barcode") == selected_barcode:
                product_to_modify = product
                product_index = index
                break
        
        if not product_to_modify:
            messagebox.showerror("خطأ", "لم يتم العثور على المنتج المحدد في البيانات.", parent=parent_window)
            return

        popup_window = tk.Toplevel(root)
        popup_window.title("تعديل منتج")
        popup_window.resizable(False, False)
        popup_window.grab_set()

        popup_width = 350; popup_height = 280
        x_cordinate = int((root.winfo_screenwidth() / 2) - (popup_width / 2))
        y_cordinate = int((root.winfo_screenheight() / 2) - (popup_height / 2))
        popup_window.geometry(f"{popup_width}x{popup_height}+{x_cordinate}+{y_cordinate}")

        popup_frame = ttk.Frame(popup_window, padding="15 15 15 15")
        popup_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(popup_frame, text="باركود:").grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Label(popup_frame, text=product_to_modify.get("barcode", "")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Label(popup_frame, text="اسم المنتج:").grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        mod_product_name_entry = ttk.Entry(popup_frame, justify=tk.RIGHT)
        mod_product_name_entry.insert(0, product_to_modify.get("name", ""))
        mod_product_name_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(popup_frame, text="سعر الشراء:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        mod_purchase_price_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        mod_purchase_price_entry.insert(0, str(product_to_modify.get("purchase_price", "")))
        mod_purchase_price_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(popup_frame, text="سعر البيع:").grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        mod_selling_price_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        mod_selling_price_entry.insert(0, str(product_to_modify.get("selling_price", "")))
        mod_selling_price_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(popup_frame, text="الكميه:").grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        mod_quantity_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_integer)
        mod_quantity_entry.insert(0, str(product_to_modify.get("quantity", "")))
        mod_quantity_entry.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(popup_frame, text="الضريبة (%):").grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)
        mod_tax_entry = ttk.Entry(popup_frame, justify=tk.RIGHT, validate="key", validatecommand=vcmd_float)
        mod_tax_entry.insert(0, str(product_to_modify.get("tax_percent", "")))
        mod_tax_entry.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW)
        
        popup_frame.columnconfigure(0, weight=1)

        def save_product_modifications():
            nonlocal inventory_products_list 
            
            name = mod_product_name_entry.get().strip()
            purchase_price_str = mod_purchase_price_entry.get().strip()
            selling_price_str = mod_selling_price_entry.get().strip()
            quantity_str = mod_quantity_entry.get().strip()
            tax_str = mod_tax_entry.get().strip()

            if not all([name, purchase_price_str, selling_price_str, quantity_str, tax_str]):
                messagebox.showerror("خطأ في الإدخال", "يرجى ملء جميع الحقول.", parent=popup_window); return
            try:
                purchase_price = float(purchase_price_str); selling_price = float(selling_price_str)
                quantity = int(quantity_str); tax_percent = float(tax_str)
                if purchase_price < 0 or selling_price < 0 or quantity < 0 or tax_percent < 0:
                    messagebox.showerror("خطأ في الإدخال", "القيم الرقمية يجب أن تكون موجبة.", parent=popup_window); return
            except ValueError:
                messagebox.showerror("خطأ في الإدخال", "يرجى إدخال قيم رقمية صحيحة.", parent=popup_window); return

            inventory_products_list[product_index]["name"] = name
            inventory_products_list[product_index]["purchase_price"] = purchase_price
            inventory_products_list[product_index]["selling_price"] = selling_price
            inventory_products_list[product_index]["quantity"] = quantity
            inventory_products_list[product_index]["tax_percent"] = tax_percent
            
            save_data_to_json(inventory_products_list, INVENTORY_FILE) 
            print(f"Product modified: {inventory_products_list[product_index]}") 
            refresh_inventory_treeview()
            popup_window.destroy()

        save_button = ttk.Button(popup_frame, text="حفظ التعديلات", command=save_product_modifications)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)
        popup_window.protocol("WM_DELETE_WINDOW", lambda: (popup_window.destroy()))

    def delete_selected_product():
        nonlocal inventory_treeview_widget, inventory_products_list, add_stock_frame
        parent_window = add_stock_frame if add_stock_frame and add_stock_frame.winfo_exists() else root

        if not inventory_treeview_widget:
            messagebox.showerror("خطأ", "جدول المخزون غير متاح.", parent=parent_window)
            return

        selected_items = inventory_treeview_widget.selection()
        if not selected_items:
            messagebox.showinfo("لا يوجد تحديد", "الرجاء اختيار منتج لحذفه.", parent=parent_window)
            return
        
        item_id = selected_items[0]
        item_values = inventory_treeview_widget.item(item_id, 'values')
        selected_barcode = item_values[5] 

        if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف المنتج المحدد؟", parent=parent_window):
            product_found_and_removed = False
            for i, product in enumerate(inventory_products_list):
                if product.get("barcode") == selected_barcode:
                    inventory_products_list.pop(i)
                    product_found_and_removed = True
                    break
            
            if product_found_and_removed:
                save_data_to_json(inventory_products_list, INVENTORY_FILE) 
                refresh_inventory_treeview()
                messagebox.showinfo("تم الحذف", "تم حذف المنتج بنجاح.", parent=parent_window)
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على المنتج في القائمة الداخلية.", parent=parent_window)


    def show_add_stock_page():
        nonlocal add_stock_frame, new_invoice_frame, inventory_treeview_widget, view_report_frame, operations_archive_frame
        if new_invoice_frame: new_invoice_frame.destroy(); new_invoice_frame = None
        if view_report_frame: view_report_frame.destroy(); view_report_frame = None
        if operations_archive_frame: operations_archive_frame.destroy(); operations_archive_frame = None
            
        if add_stock_frame: add_stock_frame.destroy()
        button_frame.pack_forget()
        add_stock_frame = ttk.Frame(main_content_frame, padding="10 10 10 10")
        add_stock_frame.pack(expand=True, fill=tk.BOTH)
        title_label = ttk.Label(add_stock_frame, text="إضافة مخزون", font=('Helvetica', 18, 'bold'))
        title_label.pack(side=tk.TOP, pady=(0, 10)) 
        action_buttons_stock_frame = ttk.Frame(add_stock_frame)
        action_buttons_stock_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        add_product_button = ttk.Button(action_buttons_stock_frame, text="إضافة منتج", command=open_add_product_popup)
        add_product_button.pack(side=tk.RIGHT, padx=5)
        modify_product_button = ttk.Button(action_buttons_stock_frame, text="تعديل منتج", command=open_modify_product_popup) 
        modify_product_button.pack(side=tk.RIGHT, padx=5)
        delete_product_button = ttk.Button(action_buttons_stock_frame, text="حذف منتج", command=delete_selected_product) 
        delete_product_button.pack(side=tk.RIGHT, padx=5)
        treeview_frame = ttk.Frame(add_stock_frame)
        treeview_frame.pack(side=tk.TOP, pady=(10,0), expand=True, fill=tk.BOTH) 
        columns = ("col_tax", "col_total_price", "col_price", "col_quantity", "col_item_name", "col_serial")
        inventory_treeview_widget = ttk.Treeview(treeview_frame, columns=columns, show="headings") 
        headings_stock = [("col_serial", "الرقم التسلسلي"), ("col_item_name", "الصنف"), ("col_quantity", "الكميه"), 
                          ("col_price", "السعر"), ("col_total_price", "اجمالي السعر"), ("col_tax", "الضريبة")]
        widths_anchors_stock = [("col_serial", 100, tk.E), ("col_item_name", 250, tk.E), 
                                ("col_quantity", 80, tk.CENTER), ("col_price", 100, tk.CENTER), 
                                ("col_total_price", 120, tk.CENTER), ("col_tax", 80, tk.CENTER)]
        for col, text in headings_stock: inventory_treeview_widget.heading(col, text=text)
        for col, w, anc in widths_anchors_stock: inventory_treeview_widget.column(col, width=w, anchor=anc)
        v_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=inventory_treeview_widget.yview)
        inventory_treeview_widget.configure(yscrollcommand=v_scrollbar.set)
        h_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL, command=inventory_treeview_widget.xview)
        inventory_treeview_widget.configure(xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.LEFT, fill=tk.Y); h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        inventory_treeview_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        refresh_inventory_treeview() 
        back_button = ttk.Button(add_stock_frame, text="رجوع", command=show_main_module_buttons)
        back_button.pack(side=tk.BOTTOM, pady=10)

    def show_view_report_page(report_type):
        nonlocal view_report_frame, new_invoice_frame, add_stock_frame, operations_archive_frame
        if new_invoice_frame: new_invoice_frame.destroy(); new_invoice_frame = None
        if add_stock_frame: add_stock_frame.destroy(); add_stock_frame = None
        if operations_archive_frame: operations_archive_frame.destroy(); operations_archive_frame = None
        
        if view_report_frame: view_report_frame.destroy()
        button_frame.pack_forget()
        view_report_frame = ttk.Frame(main_content_frame, padding="20 20 20 20")
        view_report_frame.pack(expand=True, fill=tk.BOTH)
        title_label = ttk.Label(view_report_frame, text="عرض التقرير", font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)
        report_type_label = ttk.Label(view_report_frame, text=f"التقرير المطلوب: {report_type}", font=('Helvetica', 14))
        report_type_label.pack(pady=5)
        pdf_feature_label = ttk.Label(view_report_frame, text="ميزة إنشاء ملفات PDF للتقارير قيد التطوير.", font=('Helvetica', 12))
        pdf_feature_label.pack(pady=20)
        report_bottom_buttons_frame = ttk.Frame(view_report_frame)
        report_bottom_buttons_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        export_pdf_button = ttk.Button(report_bottom_buttons_frame, text="تصدير إلى PDF", command=lambda: print("Export to PDF clicked - functionality pending"))
        export_pdf_button.pack(side=tk.RIGHT, padx=10) 
        back_button = ttk.Button(report_bottom_buttons_frame, text="رجوع", command=show_main_module_buttons)
        back_button.pack(side=tk.RIGHT, padx=10) 

    def show_operations_archive_page():
        nonlocal operations_archive_frame, new_invoice_frame, add_stock_frame, view_report_frame
        if new_invoice_frame: new_invoice_frame.destroy(); new_invoice_frame = None
        if add_stock_frame: add_stock_frame.destroy(); add_stock_frame = None
        if view_report_frame: view_report_frame.destroy(); view_report_frame = None

        if operations_archive_frame: operations_archive_frame.destroy()
        button_frame.pack_forget()
        operations_archive_frame = ttk.Frame(main_content_frame, padding="10 10 10 10")
        operations_archive_frame.pack(expand=True, fill=tk.BOTH)
        title_label = ttk.Label(operations_archive_frame, text="أرشيف العمليات", font=('Helvetica', 18, 'bold'))
        title_label.pack(side=tk.TOP, pady=10)
        search_area_frame = ttk.Frame(operations_archive_frame)
        search_area_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=10)
        search_label = ttk.Label(search_area_frame, text=":بحث") 
        search_label.pack(side=tk.RIGHT, padx=(0,5)) 
        search_entry = ttk.Entry(search_area_frame, justify=tk.RIGHT)
        search_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(0,5)) 
        search_button = ttk.Button(search_area_frame, text="بحث", command=lambda: print(f"Search for: {search_entry.get()}"))
        search_button.pack(side=tk.RIGHT, padx=(5,0)) 
        placeholder_label = ttk.Label(operations_archive_frame, text="سيتم هنا عرض قائمة بالعمليات المحفوظة (مثل الفواتير).")
        placeholder_label.pack(side=tk.TOP, pady=20, expand=True, fill=tk.BOTH)
        back_button = ttk.Button(operations_archive_frame, text="رجوع", command=show_main_module_buttons)
        back_button.pack(side=tk.BOTTOM, pady=10)

    button_style = ttk.Style()
    button_style.configure("MainModule.TButton", font=('Helvetica', 14, 'bold'), padding=20)
    button_style.configure("MainModule.TMenubutton", font=('Helvetica', 14, 'bold'), padding=20) 

    invoices_menubutton_style_name = "Invoices.MainModule.TMenubutton"
    button_style.configure(invoices_menubutton_style_name, background="light steel blue", foreground='black')
    invoices_menubutton = ttk.Menubutton(button_frame, text="الفواتير", style=invoices_menubutton_style_name, width=25, direction="below")
    invoices_menu = tk.Menu(invoices_menubutton, tearoff=0)
    invoices_menubutton["menu"] = invoices_menu
    invoices_menu.add_command(label="فاتورة جديده", command=show_new_invoice_page)
    invoices_menu.add_command(label="تعديل فاتورة", command=lambda: print("Action: Modify Invoice"))
    invoices_menu.add_command(label="استدعاء فاتورة", command=show_operations_archive_page) 
    invoices_menubutton.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    inventory_menubutton_style_name = "Inventory.MainModule.TMenubutton"
    button_style.configure(inventory_menubutton_style_name, background="pale green", foreground='black')
    inventory_menubutton = ttk.Menubutton(button_frame, text="المخزون", style=inventory_menubutton_style_name, width=25, direction="below")
    inventory_menu = tk.Menu(inventory_menubutton, tearoff=0)
    inventory_menubutton["menu"] = inventory_menu
    inventory_menu.add_command(label="(إضافة مخزون) Add Stock", command=show_add_stock_page)
    inventory_menubutton.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    reports_menubutton_style_name = "Reports.MainModule.TMenubutton"
    button_style.configure(reports_menubutton_style_name, background="light coral", foreground='black')
    reports_menubutton = ttk.Menubutton(button_frame, text="التقارير", style=reports_menubutton_style_name, width=25, direction="below")
    reports_menu = tk.Menu(reports_menubutton, tearoff=0)
    reports_menubutton["menu"] = reports_menu
    report_types = ["تقارير يوميه", "تقارير اسبوعي", "تقارير شهرية", "تقارير سنوية"]
    for rt in report_types: reports_menu.add_command(label=rt, command=lambda r=rt: show_view_report_page(r))
    reports_menubutton.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    operations_archive_text = "ملف حفظ العمليات"; operations_archive_color = "light slate gray"; operations_archive_grid_pos = (1,1)
    style_name_ops_archive = f"{operations_archive_text.replace(' ', '')}.MainModule.TButton"
    button_style.configure(style_name_ops_archive, background=operations_archive_color, foreground='black')
    operations_archive_button = ttk.Button(button_frame, text=operations_archive_text, command=show_operations_archive_page, style=style_name_ops_archive, width=25)
    operations_archive_button.grid(row=operations_archive_grid_pos[0], column=operations_archive_grid_pos[1], padx=20, pady=20, sticky="nsew")
    
    for i in range(2): button_frame.grid_columnconfigure(i, weight=1); button_frame.grid_rowconfigure(i, weight=1)
    
    show_main_module_buttons()
    root.mainloop()

def main():
    login_root = tk.Tk()
    LoginWindow(login_root, open_main_application)
    login_root.mainloop()

if __name__ == "__main__":
    main()
