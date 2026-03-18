"""
models.py — SQLAlchemy database models
M/S. Sotota Machineries Store
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ── NEW: Video Model ──────────────────────────────────────────────────
class Video(db.Model):
    __tablename__ = 'videos'

    id                = db.Column(db.Integer,     primary_key=True)
    title             = db.Column(db.String(250), nullable=False)
    description       = db.Column(db.Text)
    uploader_name     = db.Column(db.String(150), nullable=False)
    uploader_phone    = db.Column(db.String(20))
    uploader_location = db.Column(db.String(150))
    video_type        = db.Column(db.String(20),  default='customer')  # 'customer' or 'admin'
    video_url         = db.Column(db.Text)        # YouTube / Facebook link
    video_file        = db.Column(db.String(200)) # uploaded file
    thumbnail_url     = db.Column(db.Text)
    category          = db.Column(db.String(100))
    is_approved       = db.Column(db.Boolean,     default=False)
    views             = db.Column(db.Integer,     default=0)
    created_at        = db.Column(db.DateTime,    default=datetime.utcnow)

    def get_embed_url(self):
        url = self.video_url or ''
        if 'youtube.com/watch' in url:
            vid_id = url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{vid_id}"
        if 'youtu.be/' in url:
            vid_id = url.split('youtu.be/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{vid_id}"
        return url


# ── NEW: Pre-Order Model (products NOT in stock) ──────────────────────
class PreOrder(db.Model):
    __tablename__ = 'preorders'

    id                  = db.Column(db.Integer,     primary_key=True)
    customer_name       = db.Column(db.String(150), nullable=False)
    customer_phone      = db.Column(db.String(20),  nullable=False)
    customer_district   = db.Column(db.String(100))
    customer_address    = db.Column(db.Text)
    product_name        = db.Column(db.String(250), nullable=False)
    product_category    = db.Column(db.String(100))
    product_description = db.Column(db.Text)
    quantity            = db.Column(db.Integer,     default=1)
    urgency             = db.Column(db.String(20),  default='normal')
    preferred_delivery  = db.Column(db.String(100))
    deposit_amount      = db.Column(db.String(50))
    special_notes       = db.Column(db.Text)
    order_number        = db.Column(db.String(20),  unique=True)
    status              = db.Column(db.String(30),  default='pending')
    admin_notes         = db.Column(db.Text)
    estimated_price     = db.Column(db.String(100))
    created_at          = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime,    default=datetime.utcnow,
                                                    onupdate=datetime.utcnow)

    STATUS_LABELS = {
        'pending':    ('⏳ Pending Review',   'warning'),
        'confirmed':  ('✅ Confirmed',         'success'),
        'sourcing':   ('🔍 Sourcing Product',  'info'),
        'ready':      ('📦 Ready / Available', 'success'),
        'delivered':  ('🎉 Delivered',         'success'),
        'cancelled':  ('❌ Cancelled',         'danger'),
    }

    def status_label(self):
        return self.STATUS_LABELS.get(self.status, ('Unknown', 'secondary'))


# ── NEW: Pre-Book Offer (admin posts offers customers can book early) ─
class PreBookOffer(db.Model):
    __tablename__ = 'prebook_offers'

    id              = db.Column(db.Integer,     primary_key=True)
    product_name    = db.Column(db.String(250), nullable=False)
    product_brand   = db.Column(db.String(100))
    product_model   = db.Column(db.String(100))
    category        = db.Column(db.String(100))
    description     = db.Column(db.Text)
    current_price   = db.Column(db.String(100))   # today's price
    expected_price  = db.Column(db.String(100))   # expected future price
    image_url       = db.Column(db.Text)
    image_file      = db.Column(db.String(200))
    offer_deadline  = db.Column(db.String(100))   # e.g. "Valid until 31 Dec 2024"
    reason          = db.Column(db.Text)           # why price will increase
    deposit_required= db.Column(db.String(100))   # e.g. "৳500 deposit"
    is_active       = db.Column(db.Boolean,       default=True)
    sort_order      = db.Column(db.Integer,       default=0)
    created_at      = db.Column(db.DateTime,      default=datetime.utcnow)

    def image(self):
        if self.image_file:
            return f"/static/uploads/{self.image_file}"
        return self.image_url or ""


# ── NEW: Pre-Book Booking (customer books a PreBookOffer) ─────────────
class PreBooking(db.Model):
    __tablename__ = 'prebookings'

    id                  = db.Column(db.Integer,     primary_key=True)
    customer_name       = db.Column(db.String(150), nullable=False)
    customer_phone      = db.Column(db.String(20),  nullable=False)
    customer_district   = db.Column(db.String(100))
    customer_address    = db.Column(db.Text)
    product_name        = db.Column(db.String(250), nullable=False)
    product_category    = db.Column(db.String(100))
    product_description = db.Column(db.Text)
    quantity            = db.Column(db.Integer,     default=1)
    urgency             = db.Column(db.String(20),  default='normal')
    preferred_delivery  = db.Column(db.String(100))
    deposit_amount      = db.Column(db.String(50))
    special_notes       = db.Column(db.Text)
    order_number        = db.Column(db.String(20),  unique=True)
    status              = db.Column(db.String(30),  default='pending')
    admin_notes         = db.Column(db.Text)
    estimated_price     = db.Column(db.String(100))
    created_at          = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime,    default=datetime.utcnow,
                                                    onupdate=datetime.utcnow)

    STATUS_LABELS = {
        'pending':    ('⏳ Pending Review',   'warning'),
        'confirmed':  ('✅ Confirmed',         'success'),
        'processing': ('🔄 Processing',        'info'),
        'ready':      ('📦 Ready / Available', 'success'),
        'delivered':  ('🎉 Delivered',         'success'),
        'cancelled':  ('❌ Cancelled',         'danger'),
    }

    def status_label(self):
        return self.STATUS_LABELS.get(self.status, ('Unknown', 'secondary'))


class Category(db.Model):
    __tablename__ = 'categories'

    id          = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    slug        = db.Column(db.String(120), nullable=False, unique=True)
    icon        = db.Column(db.String(10))
    description = db.Column(db.Text)
    page_file   = db.Column(db.String(80))   # e.g. 'machines.html'
    sort_order  = db.Column(db.Integer,     default=0)
    is_active   = db.Column(db.Boolean,     default=True)
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)

    products = db.relationship('Product', backref='category', lazy=True,
                               order_by='Product.sort_order')

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'slug':        self.slug,
            'icon':        self.icon,
            'description': self.description,
            'page_file':   self.page_file,
        }


class Product(db.Model):
    __tablename__ = 'products'

    id             = db.Column(db.Integer,     primary_key=True)
    category_id    = db.Column(db.Integer,     db.ForeignKey('categories.id'), nullable=False)
    name           = db.Column(db.String(250), nullable=False)
    brand          = db.Column(db.String(100))
    model_no       = db.Column(db.String(100))
    description    = db.Column(db.Text)
    image_url      = db.Column(db.Text)        # external image URL
    image_file     = db.Column(db.String(200)) # uploaded file path
    image_url_2    = db.Column(db.Text)        # extra image 2 (URL)
    image_file_2   = db.Column(db.String(200)) # extra image 2 (uploaded)
    image_url_3    = db.Column(db.Text)        # extra image 3 (URL)
    image_file_3   = db.Column(db.String(200)) # extra image 3 (uploaded)
    badge          = db.Column(db.String(20))  # Hot | New | Sale | Popular
    is_featured    = db.Column(db.Boolean,     default=False)
    is_new_arrival = db.Column(db.Boolean,     default=False)
    is_hot         = db.Column(db.Boolean,     default=False)
    wa_message     = db.Column(db.Text)        # custom WhatsApp message
    sort_order     = db.Column(db.Integer,     default=0)
    is_active      = db.Column(db.Boolean,     default=True)
    created_at     = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime,    default=datetime.utcnow,
                                               onupdate=datetime.utcnow)

    def image(self):
        """Return the best available image source."""
        if self.image_file:
            return f"/static/uploads/{self.image_file}"
        return self.image_url or ""

    def all_images(self):
        """Return list of all available image URLs (up to 3)."""
        imgs = []
        main = self.image()
        if main: imgs.append(main)
        img2 = f"/static/uploads/{self.image_file_2}" if self.image_file_2 else (self.image_url_2 or "")
        if img2: imgs.append(img2)
        img3 = f"/static/uploads/{self.image_file_3}" if self.image_file_3 else (self.image_url_3 or "")
        if img3: imgs.append(img3)
        return imgs

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'brand':       self.brand,
            'model':       self.model_no,
            'description': self.description,
            'image':       self.image(),
            'images':      self.all_images(),
            'badge':       self.badge,
            'category':    self.category.name if self.category else '',
            'wa_message':  self.wa_message or f"{self.name} সম্পর্কে দাম ও স্টক জানতে চাই।",
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id                = db.Column(db.Integer,     primary_key=True)
    reviewer_name     = db.Column(db.String(150), nullable=False)
    reviewer_location = db.Column(db.String(150))
    rating            = db.Column(db.SmallInteger)
    review_text       = db.Column(db.Text,        nullable=False)
    is_approved       = db.Column(db.Boolean,     default=False)
    created_at        = db.Column(db.DateTime,    default=datetime.utcnow)
