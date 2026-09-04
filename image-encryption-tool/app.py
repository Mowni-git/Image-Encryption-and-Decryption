import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Image Encryption")
        self.root.geometry("1100x750")
        self.root.configure(bg="#10101a")
        self.root.minsize(900, 650)

        self.original_image = None
        self.processed_image = None
        self.original_photo = None
        self.processed_photo = None

        self.create_gui()

    def create_gui(self):
        # Header
        header = tk.Frame(self.root, bg="#17142d", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Pixel Image Encryption",
            font=("Arial", 27, "bold"),
            fg="white",
            bg="#17142d"
        ).pack(pady=(18, 2))

        tk.Label(
            header,
            text="Encrypt and decrypt images using pixel manipulation",
            font=("Arial", 11),
            fg="#aaa8c5",
            bg="#17142d"
        ).pack()

        # Controls
        controls = tk.Frame(self.root, bg="#10101a")
        controls.pack(fill="x", padx=25, pady=18)

        tk.Button(
            controls,
            text="Open Image",
            command=self.open_image,
            bg="#4c3cff",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10
        ).pack(side="left", padx=5)

        tk.Label(
            controls,
            text="Key:",
            bg="#10101a",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=(25, 5))

        self.key_entry = tk.Entry(
            controls,
            width=10,
            bg="#25243a",
            fg="white",
            insertbackground="white",
            font=("Arial", 12)
        )
        self.key_entry.insert(0, "123")
        self.key_entry.pack(side="left", padx=5, ipady=7)

        tk.Button(
            controls,
            text="Encrypt",
            command=self.encrypt_image,
            bg="#e04b7a",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10
        ).pack(side="left", padx=7)

        tk.Button(
            controls,
            text="Decrypt",
            command=self.decrypt_image,
            bg="#218c74",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10
        ).pack(side="left", padx=7)

        tk.Button(
            controls,
            text="Save Result",
            command=self.save_image,
            bg="#e09b36",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10
        ).pack(side="right", padx=5)

        # Status
        self.status = tk.Label(
            self.root,
            text="Select an image to begin",
            bg="#10101a",
            fg="#8e8ba8",
            font=("Arial", 10)
        )
        self.status.pack()

        # Image area
        image_area = tk.Frame(self.root, bg="#10101a")
        image_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        # Original image panel
        left = tk.Frame(
            image_area,
            bg="#1a1930",
            highlightbackground="#302d52",
            highlightthickness=1
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            left,
            text="ORIGINAL IMAGE",
            bg="#1a1930",
            fg="#aaa8c5",
            font=("Arial", 11, "bold")
        ).pack(pady=12)

        self.original_label = tk.Label(
            left,
            text="No image selected",
            bg="#1a1930",
            fg="#5f5c78",
            font=("Arial", 14)
        )
        self.original_label.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Processed image panel
        right = tk.Frame(
            image_area,
            bg="#1a1930",
            highlightbackground="#302d52",
            highlightthickness=1
        )
        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            right,
            text="ENCRYPTED / DECRYPTED",
            bg="#1a1930",
            fg="#aaa8c5",
            font=("Arial", 11, "bold")
        ).pack(pady=12)

        self.processed_label = tk.Label(
            right,
            text="Result will appear here",
            bg="#1a1930",
            fg="#5f5c78",
            font=("Arial", 14)
        )
        self.processed_label.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Footer
        tk.Label(
            self.root,
            text="RGB pixel values are transformed using XOR encryption",
            bg="#10101a",
            fg="#5e5b76",
            font=("Arial", 9)
        ).pack(pady=10)

    def get_key(self):
        try:
            key = int(self.key_entry.get())

            if key < 0 or key > 255:
                raise ValueError

            return key

        except ValueError:
            messagebox.showerror(
                "Invalid Key",
                "Enter a number between 0 and 255."
            )
            return None

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        try:
            image = Image.open(path)

            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")

            self.original_image = image
            self.processed_image = None

            self.display_image(
                image,
                self.original_label,
                "original"
            )

            self.processed_label.configure(
                image="",
                text="Result will appear here"
            )

            filename = os.path.basename(path)

            self.status.configure(
                text=f"Loaded: {filename} | "
                     f"Size: {image.width} x {image.height}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not open image:\n{error}"
            )

    def pixel_xor(self, image, key):
        result = image.copy()
        pixels = result.load()

        for y in range(result.height):
            for x in range(result.width):

                pixel = pixels[x, y]

                if result.mode == "RGBA":

                    r, g, b, a = pixel

                    pixels[x, y] = (
                        r ^ key,
                        g ^ key,
                        b ^ key,
                        a
                    )

                else:

                    r, g, b = pixel

                    pixels[x, y] = (
                        r ^ key,
                        g ^ key,
                        b ^ key
                    )

        return result

    def encrypt_image(self):

        if self.original_image is None:
            messagebox.showwarning(
                "No Image",
                "Please open an image first."
            )
            return

        key = self.get_key()

        if key is None:
            return

        self.processed_image = self.pixel_xor(
            self.original_image,
            key
        )

        self.display_image(
            self.processed_image,
            self.processed_label,
            "processed"
        )

        self.status.configure(
            text=f"Image encrypted successfully | Key: {key}"
        )

    def decrypt_image(self):

        if self.original_image is None:
            messagebox.showwarning(
                "No Image",
                "Please open an image first."
            )
            return

        key = self.get_key()

        if key is None:
            return

        self.processed_image = self.pixel_xor(
            self.original_image,
            key
        )

        self.display_image(
            self.processed_image,
            self.processed_label,
            "processed"
        )

        self.status.configure(
            text=f"Image decrypted successfully | Key: {key}"
        )

    def display_image(self, image, label, image_type):

        display = image.copy()

        display.thumbnail(
            (450, 450),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(display)

        label.configure(
            image=photo,
            text=""
        )

        if image_type == "original":
            self.original_photo = photo
        else:
            self.processed_photo = photo

    def save_image(self):

        if self.processed_image is None:
            messagebox.showwarning(
                "No Result",
                "Encrypt or decrypt an image first."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("BMP Image", "*.bmp")
            ]
        )

        if not path:
            return

        try:

            self.processed_image.save(path)

            self.status.configure(
                text=f"Saved: {os.path.basename(path)}"
            )

            messagebox.showinfo(
                "Success",
                "Image saved successfully!"
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )


# Start application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
