"""
app.py — M/S. Sotota Machineries Store
Flask backend with PostgreSQL via SQLAlchemy

Usage:
  python app.py          (development)
  gunicorn app:app       (production)
"""

import os
import uuid
from functools import wraps
from pathlib import Path

from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, jsonify, abort)
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image

from models import db, Category, Product, Review, Video, PreBooking, PreOrder, PreBookOffer

# ──────────────────────────────────────────────────────────────────────
# SETUP
# ──────────────────────────────────────────────────────────────────────
load_dotenv()

app = Flask(__name__)

# Config
app.config['SECRET_KEY']           = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    f"postgresql://{os.getenv('DB_USER','postgres')}:"
    f"{os.getenv('DB_PASSWORD','')}@"
    f"{os.getenv('DB_HOST','localhost')}:"
    f"{os.getenv('DB_PORT','5432')}/"
    f"{os.getenv('DB_NAME','sotota_machineries')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER']        = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH']   = 150 * 1024 * 1024  # 150MB for video uploads

ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
ADMIN_PASS  = os.getenv('ADMIN_PASSWORD', 'sotota2024')
WHATSAPP    = os.getenv('WHATSAPP_NUMBER', '8801771110646')
PHONE       = os.getenv('PHONE_NUMBER',   '+8801771110646')

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

# ──────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def save_uploaded_image(file):
    """Save uploaded image, resize to max 800px wide, return filename."""
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    img = Image.open(file)
    img.convert('RGB')                     # strip alpha for jpg compatibility
    if img.width > 800:
        ratio = 800 / img.width
        img = img.resize((800, int(img.height * ratio)), Image.LANCZOS)
    img.save(save_path, optimize=True, quality=85)
    return filename


def get_nav_categories():
    return Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


@app.context_processor
def inject_globals():
    return dict(
        nav_categories=get_nav_categories(),
        whatsapp=WHATSAPP,
        phone=PHONE,
        now=datetime.utcnow(),
    )


# ──────────────────────────────────────────────────────────────────────
# PUBLIC ROUTES
# ──────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    hot_products  = Product.query.filter_by(is_active=True, is_hot=True)\
                                 .order_by(Product.sort_order).limit(8).all()
    new_arrivals  = Product.query.filter_by(is_active=True, is_new_arrival=True)\
                                 .order_by(Product.created_at.desc()).limit(8).all()
    categories    = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    reviews       = Review.query.filter_by(is_approved=True)\
                                .order_by(Review.created_at.desc()).limit(6).all()
    prebook_offers_data = PreBookOffer.query.filter_by(is_active=True)\
                                           .order_by(PreBookOffer.sort_order).limit(6).all()
    return render_template('index.html',
                           hot_products=hot_products,
                           new_arrivals=new_arrivals,
                           categories=categories,
                           reviews=reviews,
                           prebook_offers_data=prebook_offers_data)


@app.route('/machines')
def machines():
    cat = Category.query.filter_by(slug='machines').first_or_404()
    all_products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('machines.html', cat=cat, products=all_products)


@app.route('/generators')
def generators():
    cat = Category.query.filter_by(slug='generators').first_or_404()
    products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('generators.html', cat=cat, products=products)


@app.route('/motors')
def motors():
    cat = Category.query.filter_by(slug='motors').first_or_404()
    products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('motors.html', cat=cat, products=products)


@app.route('/oils')
def oils():
    cat = Category.query.filter_by(slug='oils').first_or_404()
    products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('oils.html', cat=cat, products=products)


@app.route('/home-kitchen')
def home_kitchen():
    cat = Category.query.filter_by(slug='home-kitchen').first_or_404()
    products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('home_kitchen.html', cat=cat, products=products)


@app.route('/fittings')
def fittings():
    cat = Category.query.filter_by(slug='fittings').first_or_404()
    products = Product.query.filter_by(
        category_id=cat.id, is_active=True
    ).order_by(Product.sort_order).all()
    return render_template('fittings.html', cat=cat, products=products)


@app.route('/pipes')
def pipes():
    return render_template('pipes.html')


@app.route('/tubewell')
def tubewell():
    return render_template('tubewell.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ── VIDEOS ────────────────────────────────────────────────────────────

@app.route('/videos')
def videos():
    approved = Video.query.filter_by(is_approved=True)\
                          .order_by(Video.created_at.desc()).all()
    return render_template('videos.html', videos=approved)


@app.route('/submit-video', methods=['POST'])
def submit_video():
    title    = request.form.get('title', '').strip()
    name     = request.form.get('uploader_name', '').strip()
    phone    = request.form.get('uploader_phone', '').strip()
    location = request.form.get('uploader_location', '').strip()
    category = request.form.get('category', '').strip()
    desc     = request.form.get('description', '').strip()

    if not title or not name:
        flash('Please fill in title and your name.', 'warning')
        return redirect(url_for('videos'))

    video_file_name = None
    file = request.files.get('video_file')
    if file and file.filename:
        allowed_video = {'mp4', 'mov', 'avi', 'webm', '3gp'}
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in allowed_video:
            flash('Only MP4, MOV, AVI, WEBM or 3GP video files allowed.', 'danger')
            return redirect(url_for('videos') + '#submit')
        import uuid
        video_file_name = f"vid_{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file_name)
        file.save(save_path)
    else:
        flash('Please select a video file to upload.', 'warning')
        return redirect(url_for('videos') + '#submit')

    video = Video(
        title=title, description=desc,
        uploader_name=name, uploader_phone=phone,
        uploader_location=location,
        video_file=video_file_name,
        category=category, video_type='customer',
        is_approved=False
    )
    db.session.add(video)
    db.session.commit()
    flash('✅ Video submitted! It will appear after admin approval (usually within 24 hours).', 'success')
    return redirect(url_for('videos'))


# ── PRE-BOOK (Lock price for upcoming price rise) ─────────────────────

@app.route('/prebook', methods=['GET', 'POST'])
def prebook():
    offers = PreBookOffer.query.filter_by(is_active=True)\
                               .order_by(PreBookOffer.sort_order).all()
    if request.method == 'POST':
        import random, string
        year = datetime.utcnow().year
        rand = ''.join(random.choices(string.digits, k=4))
        order_num = f"PB-{year}-{rand}"
        while PreBooking.query.filter_by(order_number=order_num).first():
            rand = ''.join(random.choices(string.digits, k=4))
            order_num = f"PB-{year}-{rand}"

        booking = PreBooking(
            customer_name       = request.form.get('customer_name', '').strip(),
            customer_phone      = request.form.get('customer_phone', '').strip(),
            customer_district   = request.form.get('customer_district', '').strip(),
            customer_address    = request.form.get('customer_address', '').strip(),
            product_name        = request.form.get('product_name', '').strip(),
            product_category    = request.form.get('product_category', '').strip(),
            product_description = request.form.get('product_description', '').strip(),
            quantity            = int(request.form.get('quantity', 1) or 1),
            urgency             = request.form.get('urgency', 'normal'),
            preferred_delivery  = request.form.get('preferred_delivery', '').strip(),
            deposit_amount      = request.form.get('deposit_amount', '').strip(),
            special_notes       = request.form.get('special_notes', '').strip(),
            order_number        = order_num,
            status              = 'pending',
        )
        db.session.add(booking)
        db.session.commit()
        flash(f'✅ Pre-Book confirmed! Your booking number is <strong>{order_num}</strong>. We will contact you soon.', 'success')
        return redirect(url_for('prebook_confirm', order_num=order_num))

    return render_template('prebook.html', offers=offers)


@app.route('/prebook/confirm/<order_num>')
def prebook_confirm(order_num):
    booking = PreBooking.query.filter_by(order_number=order_num).first_or_404()
    return render_template('prebook_confirm.html', booking=booking)


@app.route('/prebook/track')
def prebook_track():
    order_num = request.args.get('order_number', '').strip().upper()
    booking = None
    if order_num:
        booking = PreBooking.query.filter_by(order_number=order_num).first()
        if not booking:
            flash('Booking not found. Please check your booking number.', 'danger')
    return render_template('prebook_track.html', booking=booking, order_num=order_num)


# ── PRE-ORDER (Products not in stock — source on demand) ──────────────

@app.route('/preorder', methods=['GET', 'POST'])
def preorder():
    if request.method == 'POST':
        import random, string
        year = datetime.utcnow().year
        rand = ''.join(random.choices(string.digits, k=4))
        order_num = f"PO-{year}-{rand}"
        while PreOrder.query.filter_by(order_number=order_num).first():
            rand = ''.join(random.choices(string.digits, k=4))
            order_num = f"PO-{year}-{rand}"

        po = PreOrder(
            customer_name       = request.form.get('customer_name', '').strip(),
            customer_phone      = request.form.get('customer_phone', '').strip(),
            customer_district   = request.form.get('customer_district', '').strip(),
            customer_address    = request.form.get('customer_address', '').strip(),
            product_name        = request.form.get('product_name', '').strip(),
            product_category    = request.form.get('product_category', '').strip(),
            product_description = request.form.get('product_description', '').strip(),
            quantity            = int(request.form.get('quantity', 1) or 1),
            urgency             = request.form.get('urgency', 'normal'),
            preferred_delivery  = request.form.get('preferred_delivery', '').strip(),
            deposit_amount      = request.form.get('deposit_amount', '').strip(),
            special_notes       = request.form.get('special_notes', '').strip(),
            order_number        = order_num,
            status              = 'pending',
        )
        db.session.add(po)
        db.session.commit()
        flash(f'✅ Pre-Order placed! Your order number is <strong>{order_num}</strong>. We will contact you within 24 hours.', 'success')
        return redirect(url_for('preorder_confirm', order_num=order_num))

    return render_template('preorder.html')


@app.route('/preorder/confirm/<order_num>')
def preorder_confirm(order_num):
    po = PreOrder.query.filter_by(order_number=order_num).first_or_404()
    return render_template('preorder_confirm.html', booking=po)


@app.route('/preorder/track')
def preorder_track():
    order_num = request.args.get('order_number', '').strip().upper()
    po = None
    if order_num:
        po = PreOrder.query.filter_by(order_number=order_num).first()
        if not po:
            flash('Order not found. Please check your order number.', 'danger')
    return render_template('preorder_track.html', booking=po, order_num=order_num)


# Review submission (public)
@app.route('/submit-review', methods=['POST'])
def submit_review():
    name     = request.form.get('name', '').strip()
    location = request.form.get('location', '').strip()
    text     = request.form.get('review', '').strip()
    rating   = int(request.form.get('rating', 5))

    if not name or not text:
        flash('Please fill in your name and review.', 'warning')
        return redirect(request.referrer or url_for('index'))

    review = Review(
        reviewer_name=name,
        reviewer_location=location,
        review_text=text,
        rating=min(max(rating, 1), 5),
        is_approved=False  # requires admin approval
    )
    db.session.add(review)
    db.session.commit()
    flash('Thank you! Your review will appear after approval.', 'success')
    return redirect(request.referrer or url_for('index'))


# ──────────────────────────────────────────────────────────────────────
# JSON API  (used by frontend JS for dynamic loading)
# ──────────────────────────────────────────────────────────────────────

@app.route('/api/products')
def api_products():
    """Return products filtered by category slug and/or badge."""
    cat_slug = request.args.get('category', '')
    badge    = request.args.get('badge', '')
    q        = request.args.get('q', '').strip()

    query = Product.query.filter_by(is_active=True)

    if cat_slug:
        cat = Category.query.filter_by(slug=cat_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    if badge:
        query = query.filter_by(badge=badge)

    if q:
        query = query.filter(
            (Product.name.ilike(f'%{q}%')) |
            (Product.brand.ilike(f'%{q}%')) |
            (Product.model_no.ilike(f'%{q}%'))
        )

    products = query.order_by(Product.sort_order).all()
    return jsonify([p.to_dict() for p in products])


@app.route('/api/categories')
def api_categories():
    cats = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return jsonify([c.to_dict() for c in cats])


# ──────────────────────────────────────────────────────────────────────
# ADMIN — Authentication
# ──────────────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Incorrect password.', 'danger')
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


# ──────────────────────────────────────────────────────────────────────
# ADMIN — Dashboard & Product Management
# ──────────────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'total_products':   Product.query.count(),
        'active_products':  Product.query.filter_by(is_active=True).count(),
        'hot_products':     Product.query.filter_by(badge='Hot').count(),
        'new_products':     Product.query.filter_by(badge='New').count(),
        'total_reviews':    Review.query.count(),
        'pending_reviews':  Review.query.filter_by(is_approved=False).count(),
        'total_orders':     PreBooking.query.count(),
        'pending_orders':   PreBooking.query.filter_by(status='pending').count(),
        'total_preorders':  PreOrder.query.count(),
        'pending_preorders':PreOrder.query.filter_by(status='pending').count(),
        'pending_videos':   Video.query.filter_by(is_approved=False).count(),
        'prebook_offers':   PreBookOffer.query.filter_by(is_active=True).count(),
    }
    recent = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent=recent, categories=categories)


@app.route('/admin/products')
@login_required
def admin_products():
    page     = request.args.get('page', 1, type=int)
    cat_id   = request.args.get('cat', 0, type=int)
    q        = request.args.get('q', '').strip()
    per_page = 20

    query = Product.query
    if cat_id:
        query = query.filter_by(category_id=cat_id)
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%') |
                             Product.brand.ilike(f'%{q}%'))

    products   = query.order_by(Product.created_at.desc()).paginate(
                     page=page, per_page=per_page, error_out=False)
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('admin/products.html',
                           products=products,
                           categories=categories,
                           current_cat=cat_id, q=q)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        brand       = request.form.get('brand', '').strip()
        model_no    = request.form.get('model_no', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id', type=int)
        badge       = request.form.get('badge', '') or None
        is_hot      = bool(request.form.get('is_hot'))
        is_new      = bool(request.form.get('is_new_arrival'))
        is_featured = bool(request.form.get('is_featured'))
        image_url   = request.form.get('image_url', '').strip() or None
        wa_message  = request.form.get('wa_message', '').strip() or None

        if not name or not category_id:
            flash('Product name and category are required.', 'danger')
            return render_template('admin/product_form.html', categories=categories, product=None)

        image_file = None
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            try:
                image_file = save_uploaded_image(file)
            except Exception as e:
                flash(f'Image upload failed: {e}', 'warning')

        product = Product(
            name=name, brand=brand, model_no=model_no,
            description=description, category_id=category_id,
            badge=badge, is_hot=is_hot, is_new_arrival=is_new,
            is_featured=is_featured, image_url=image_url,
            image_file=image_file, wa_message=wa_message,
        )
        db.session.add(product)
        db.session.commit()
        flash(f'✅ "{name}" added successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', categories=categories, product=None)


@app.route('/admin/products/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(pid):
    product    = Product.query.get_or_404(pid)
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()

    if request.method == 'POST':
        product.name        = request.form.get('name', '').strip()
        product.brand       = request.form.get('brand', '').strip()
        product.model_no    = request.form.get('model_no', '').strip()
        product.description = request.form.get('description', '').strip()
        product.category_id = request.form.get('category_id', type=int)
        product.badge       = request.form.get('badge', '') or None
        product.is_hot      = bool(request.form.get('is_hot'))
        product.is_new_arrival = bool(request.form.get('is_new_arrival'))
        product.is_featured = bool(request.form.get('is_featured'))
        product.is_active   = bool(request.form.get('is_active'))
        product.image_url   = request.form.get('image_url', '').strip() or None
        product.wa_message  = request.form.get('wa_message', '').strip() or None

        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            try:
                # Delete old uploaded file if exists
                if product.image_file:
                    old = os.path.join(app.config['UPLOAD_FOLDER'], product.image_file)
                    if os.path.exists(old):
                        os.remove(old)
                product.image_file = save_uploaded_image(file)
            except Exception as e:
                flash(f'Image upload failed: {e}', 'warning')

        db.session.commit()
        flash(f'✅ "{product.name}" updated successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', categories=categories, product=product)


@app.route('/admin/products/delete/<int:pid>', methods=['POST'])
@login_required
def admin_delete_product(pid):
    product = Product.query.get_or_404(pid)
    # Remove uploaded image file if exists
    if product.image_file:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_file)
        if os.path.exists(img_path):
            os.remove(img_path)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'🗑️ "{name}" deleted.', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/products/toggle/<int:pid>', methods=['POST'])
@login_required
def admin_toggle_product(pid):
    product = Product.query.get_or_404(pid)
    product.is_active = not product.is_active
    db.session.commit()
    state = 'shown' if product.is_active else 'hidden'
    return jsonify({'ok': True, 'is_active': product.is_active, 'state': state})


# ──────────────────────────────────────────────────────────────────────
# ADMIN — Reviews
# ──────────────────────────────────────────────────────────────────────

@app.route('/admin/reviews')
@login_required
def admin_reviews():
    pending  = Review.query.filter_by(is_approved=False).order_by(Review.created_at.desc()).all()
    approved = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', pending=pending, approved=approved)


@app.route('/admin/reviews/approve/<int:rid>', methods=['POST'])
@login_required
def admin_approve_review(rid):
    review = Review.query.get_or_404(rid)
    review.is_approved = True
    db.session.commit()
    flash('✅ Review approved.', 'success')
    return redirect(url_for('admin_reviews'))


@app.route('/admin/reviews/delete/<int:rid>', methods=['POST'])
@login_required
def admin_delete_review(rid):
    review = Review.query.get_or_404(rid)
    db.session.delete(review)
    db.session.commit()
    flash('🗑️ Review deleted.', 'success')
    return redirect(url_for('admin_reviews'))


# ── ADMIN — Videos ────────────────────────────────────────────────────

@app.route('/admin/videos')
@login_required
def admin_videos():
    pending  = Video.query.filter_by(is_approved=False).order_by(Video.created_at.desc()).all()
    approved = Video.query.filter_by(is_approved=True).order_by(Video.created_at.desc()).all()
    return render_template('admin/videos.html', pending=pending, approved=approved)


@app.route('/admin/videos/add', methods=['GET', 'POST'])
@login_required
def admin_add_video():
    if request.method == 'POST':
        video = Video(
            title             = request.form.get('title', '').strip(),
            description       = request.form.get('description', '').strip(),
            uploader_name     = 'Sotota Machineries (Admin)',
            uploader_location = 'Station Road, Jamalpur',
            video_url         = request.form.get('video_url', '').strip(),
            category          = request.form.get('category', '').strip(),
            video_type        = 'admin',
            is_approved       = True,
        )
        db.session.add(video)
        db.session.commit()
        flash('✅ Video added and published.', 'success')
        return redirect(url_for('admin_videos'))
    return render_template('admin/video_form.html')


@app.route('/admin/videos/approve/<int:vid>', methods=['POST'])
@login_required
def admin_approve_video(vid):
    video = Video.query.get_or_404(vid)
    video.is_approved = True
    db.session.commit()
    flash('✅ Video approved and published.', 'success')
    return redirect(url_for('admin_videos'))


@app.route('/admin/videos/delete/<int:vid>', methods=['POST'])
@login_required
def admin_delete_video(vid):
    video = Video.query.get_or_404(vid)
    db.session.delete(video)
    db.session.commit()
    flash('🗑️ Video deleted.', 'success')
    return redirect(url_for('admin_videos'))


# ── ADMIN — Pre-Bookings / Orders ─────────────────────────────────────

@app.route('/admin/orders')
@login_required
def admin_orders():
    status_filter = request.args.get('status', '')
    query = PreBooking.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(PreBooking.created_at.desc()).all()
    stats = {
        'total':     PreBooking.query.count(),
        'pending':   PreBooking.query.filter_by(status='pending').count(),
        'confirmed': PreBooking.query.filter_by(status='confirmed').count(),
        'delivered': PreBooking.query.filter_by(status='delivered').count(),
    }
    return render_template('admin/orders.html', orders=orders, stats=stats,
                           status_filter=status_filter)


@app.route('/admin/orders/update/<int:oid>', methods=['POST'])
@login_required
def admin_update_order(oid):
    order = PreBooking.query.get_or_404(oid)
    order.status          = request.form.get('status', order.status)
    order.admin_notes     = request.form.get('admin_notes', '').strip()
    order.estimated_price = request.form.get('estimated_price', '').strip()
    db.session.commit()
    flash(f'✅ Pre-Book {order.order_number} updated to {order.status}.', 'success')
    return redirect(url_for('admin_orders'))


# ── ADMIN — Pre-Orders ────────────────────────────────────────────────

@app.route('/admin/preorders')
@login_required
def admin_preorders():
    status_filter = request.args.get('status', '')
    query = PreOrder.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(PreOrder.created_at.desc()).all()
    stats = {
        'total':   PreOrder.query.count(),
        'pending': PreOrder.query.filter_by(status='pending').count(),
        'sourcing':PreOrder.query.filter_by(status='sourcing').count(),
        'delivered':PreOrder.query.filter_by(status='delivered').count(),
    }
    return render_template('admin/preorders.html', orders=orders,
                           stats=stats, status_filter=status_filter)


@app.route('/admin/preorders/update/<int:oid>', methods=['POST'])
@login_required
def admin_update_preorder(oid):
    po = PreOrder.query.get_or_404(oid)
    po.status          = request.form.get('status', po.status)
    po.admin_notes     = request.form.get('admin_notes', '').strip()
    po.estimated_price = request.form.get('estimated_price', '').strip()
    db.session.commit()
    flash(f'✅ Pre-Order {po.order_number} updated.', 'success')
    return redirect(url_for('admin_preorders'))


# ── ADMIN — Pre-Book Offers ───────────────────────────────────────────

@app.route('/admin/prebook-offers')
@login_required
def admin_prebook_offers():
    offers = PreBookOffer.query.order_by(PreBookOffer.sort_order).all()
    return render_template('admin/prebook_offers.html', offers=offers)


@app.route('/admin/prebook-offers/add', methods=['GET', 'POST'])
@login_required
def admin_add_prebook_offer():
    if request.method == 'POST':
        image_file = None
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            try: image_file = save_uploaded_image(file)
            except Exception as e: flash(f'Image error: {e}', 'warning')

        offer = PreBookOffer(
            product_name     = request.form.get('product_name', '').strip(),
            product_brand    = request.form.get('product_brand', '').strip(),
            product_model    = request.form.get('product_model', '').strip(),
            category         = request.form.get('category', '').strip(),
            description      = request.form.get('description', '').strip(),
            current_price    = request.form.get('current_price', '').strip(),
            expected_price   = request.form.get('expected_price', '').strip(),
            image_url        = request.form.get('image_url', '').strip() or None,
            image_file       = image_file,
            offer_deadline   = request.form.get('offer_deadline', '').strip(),
            reason           = request.form.get('reason', '').strip(),
            deposit_required = request.form.get('deposit_required', '').strip(),
            is_active        = bool(request.form.get('is_active')),
        )
        db.session.add(offer)
        db.session.commit()
        flash(f'✅ Pre-Book offer "{offer.product_name}" added.', 'success')
        return redirect(url_for('admin_prebook_offers'))
    return render_template('admin/prebook_offer_form.html', offer=None)


@app.route('/admin/prebook-offers/edit/<int:oid>', methods=['GET', 'POST'])
@login_required
def admin_edit_prebook_offer(oid):
    offer = PreBookOffer.query.get_or_404(oid)
    if request.method == 'POST':
        offer.product_name    = request.form.get('product_name', '').strip()
        offer.product_brand   = request.form.get('product_brand', '').strip()
        offer.product_model   = request.form.get('product_model', '').strip()
        offer.category        = request.form.get('category', '').strip()
        offer.description     = request.form.get('description', '').strip()
        offer.current_price   = request.form.get('current_price', '').strip()
        offer.expected_price  = request.form.get('expected_price', '').strip()
        offer.image_url       = request.form.get('image_url', '').strip() or None
        offer.offer_deadline  = request.form.get('offer_deadline', '').strip()
        offer.reason          = request.form.get('reason', '').strip()
        offer.deposit_required= request.form.get('deposit_required', '').strip()
        offer.is_active       = bool(request.form.get('is_active'))
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            try: offer.image_file = save_uploaded_image(file)
            except Exception as e: flash(f'Image error: {e}', 'warning')
        db.session.commit()
        flash('✅ Offer updated.', 'success')
        return redirect(url_for('admin_prebook_offers'))
    return render_template('admin/prebook_offer_form.html', offer=offer)


@app.route('/admin/prebook-offers/delete/<int:oid>', methods=['POST'])
@login_required
def admin_delete_prebook_offer(oid):
    offer = PreBookOffer.query.get_or_404(oid)
    db.session.delete(offer)
    db.session.commit()
    flash('🗑️ Offer deleted.', 'success')
    return redirect(url_for('admin_prebook_offers'))


# ──────────────────────────────────────────────────────────────────────
# ERROR HANDLERS
# ──────────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(413)
def too_large(e):
    flash('Image file is too large. Maximum size is 5MB.', 'danger')
    return redirect(request.referrer or url_for('admin_dashboard'))


# ──────────────────────────────────────────────────────────────────────
# RUN
# ──────────────────────────────────────────────────────────────────────

# ── BACKWARD COMPATIBILITY — old /order routes redirect to new ones ───
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        return preorder()
    return redirect(url_for('preorder'))

@app.route('/order/confirm/<order_num>')
def order_confirm(order_num):
    return redirect(url_for('preorder_confirm', order_num=order_num))

@app.route('/order/track')
def order_track():
    order_num = request.args.get('order_number', '')
    return redirect(url_for('preorder_track', order_number=order_num))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # creates all tables including videos and prebookings
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True',
        host='0.0.0.0',
        port=5000
    )
