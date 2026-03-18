-- ====================================================================
-- M/S. SOTOTA MACHINERIES STORE — PostgreSQL Schema
-- Run this once to create all tables:
--   psql -U postgres -d sotota_machineries -f schema.sql
-- ====================================================================

-- Drop existing tables cleanly (order matters for FK constraints)

-- Set encoding for Bengali text support
SET client_encoding = 'UTF8';
DROP TABLE IF EXISTS reviews    CASCADE;
DROP TABLE IF EXISTS products   CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- ── CATEGORIES ────────────────────────────────────────────────────────
CREATE TABLE categories (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    slug        VARCHAR(120) NOT NULL UNIQUE,
    icon        VARCHAR(10),
    description TEXT,
    page_file   VARCHAR(80),        -- e.g. 'machines.html'
    sort_order  INTEGER      DEFAULT 0,
    is_active   BOOLEAN      DEFAULT TRUE,
    created_at  TIMESTAMP    DEFAULT NOW()
);

-- ── PRODUCTS ──────────────────────────────────────────────────────────
CREATE TABLE products (
    id              SERIAL        PRIMARY KEY,
    category_id     INTEGER       NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    name            VARCHAR(250)  NOT NULL,
    brand           VARCHAR(100),
    model_no        VARCHAR(100),
    description     TEXT,
    image_url       TEXT,          -- external URL (e.g. from cbmbd.com)
    image_file      VARCHAR(200),  -- uploaded file path (e.g. uploads/products/abc.jpg)
    badge           VARCHAR(20),   -- 'Hot' | 'New' | 'Sale' | 'Popular'
    is_featured     BOOLEAN       DEFAULT FALSE,
    is_new_arrival  BOOLEAN       DEFAULT FALSE,
    is_hot          BOOLEAN       DEFAULT FALSE,
    wa_message      TEXT,          -- custom WhatsApp message (optional)
    sort_order      INTEGER       DEFAULT 0,
    is_active       BOOLEAN       DEFAULT TRUE,
    created_at      TIMESTAMP     DEFAULT NOW(),
    updated_at      TIMESTAMP     DEFAULT NOW()
);

-- ── REVIEWS ───────────────────────────────────────────────────────────
CREATE TABLE reviews (
    id                SERIAL       PRIMARY KEY,
    reviewer_name     VARCHAR(150) NOT NULL,
    reviewer_location VARCHAR(150),
    rating            SMALLINT     CHECK (rating BETWEEN 1 AND 5),
    review_text       TEXT         NOT NULL,
    is_approved       BOOLEAN      DEFAULT FALSE,
    created_at        TIMESTAMP    DEFAULT NOW()
);

-- ── INDEXES ───────────────────────────────────────────────────────────
CREATE INDEX idx_products_category   ON products(category_id);
CREATE INDEX idx_products_badge      ON products(badge);
CREATE INDEX idx_products_active     ON products(is_active);
CREATE INDEX idx_products_featured   ON products(is_featured);
CREATE INDEX idx_reviews_approved    ON reviews(is_approved);

-- ── SEED: CATEGORIES ──────────────────────────────────────────────────
INSERT INTO categories (name, slug, icon, description, page_file, sort_order) VALUES
('Machines & Engines',    'machines',      '⚙️', 'Diesel engines, power tillers, harvesters',         'machines.html',      1),
('Generators & Power',    'generators',    '⚡', 'Generator sets, shallow machines, alternators',      'generators.html',    2),
('Oils & Lubricants',     'oils',          '🛢️', 'Engine oil (Mobil), gear oil for machines',          'oils.html',          3),
('Motors & Pumps',        'motors',        '🔧', 'Jet pumps, centrifugal, submersible, electric motors','motors.html',       4),
('Home & Kitchen',        'home-kitchen',  '🏠', 'Doors, bathtubs, basins, taps, gas stoves, tanks',   'home-kitchen.html',  5),
('Fittings',              'fittings',      '🔩', 'All plumbing and hardware fittings',                 'fittings.html',      6);

-- ── SEED: PRODUCTS (Machines category = id 1) ────────────────────────
INSERT INTO products (category_id, name, brand, model_no, description, image_url, badge, is_featured, is_hot, is_new_arrival) VALUES

-- Diesel Engines
(1,'Changchai Diesel Engine ZS1110',    'Changchai','ZS1110',    'Reliable water-cooled diesel engine. Trusted by Jamalpur and Mymensingh Division farmers for irrigation and tillage.',                           'https://cbmbd.com/wp-content/uploads/2024/09/5.-Changchai-Diesel-ZS1110.jpg',                                                          'Popular', TRUE, FALSE, FALSE),
(1,'Changchai ZS1110 14.7KW',           'Changchai','ZS1110-14KW','14.7KW output diesel engine. High performance for demanding agricultural and irrigation tasks.',                                                 'https://cbmbd.com/wp-content/uploads/2024/09/9.-Changchai-ZS1110-14.7-kw-300x400.jpg',                                                'Hot',    TRUE, TRUE,  FALSE),
(1,'Changchai ZS1110N Diesel Engine',   'Changchai','ZS1110N',   'Enhanced ZS1110N with improved cooling. Dependable choice for Jamalpur and Mymensingh farmers.',                                                 'https://cbmbd.com/wp-content/uploads/2024/09/10.-Changchai-ZS1110N-Diesel-Engine-300x400.jpg',                                        'Popular',FALSE, FALSE, FALSE),
(1,'Changchai ZS1115 16.2KW',           'Changchai','ZS1115',    '16.2KW single-cylinder water-cooled diesel engine. High output for heavy-duty operations.',                                                      'https://cbmbd.com/wp-content/uploads/2024/09/18.-Changchai-ZS1115-16.2-kw-300x400.jpg',                                              'Hot',    TRUE, TRUE,  FALSE),
(1,'Changchai ZS1115nm Diesel Engine',  'Changchai','ZS1115nm',  'New ZS1115nm model with improved fuel efficiency. Latest arrival at Station Road Jamalpur.',                                                    'https://cbmbd.com/wp-content/uploads/2024/09/4.-Changchai-D.E-ZS1115nm_diesel_engine.jpg',                                           'New',    FALSE,FALSE, TRUE),
(1,'Changchai L28 Diesel Engine',       'Changchai','L28',       'Compact Changchai L28 engine suitable for small-scale farming and light industrial use.',                                                        'https://cbmbd.com/wp-content/uploads/2024/09/6.-Changchai-L28-300x400.jpg',                                                           NULL,     FALSE,FALSE, FALSE),
(1,'Changchai L32 Diesel Engine',       'Changchai','L32',       'Changchai L32 — compact and powerful, ideal for agricultural and light industrial operations.',                                                  'https://cbmbd.com/wp-content/uploads/2024/09/7.-Changchai-L32-300x400.jpg',                                                           NULL,     FALSE,FALSE, FALSE),
(1,'Changchai S1100A2 15HP',            'Changchai','S1100A2',   '15HP proven engine widely sold at Station Road Jamalpur for power tiller and irrigation use.',                                                   'https://cbmbd.com/wp-content/uploads/2024/09/15.-Changchai-S1100A2-15HP-300x400.jpg',                                                'Hot',    TRUE, TRUE,  FALSE),
(1,'Changchai R190N 10.5HP',            'Changchai','R190N',     '10.5HP R190N — compact and easy to maintain, ideal for smaller farms in Jamalpur district.',                                                    'https://cbmbd.com/wp-content/uploads/2024/09/2.-Changchai-D.E-R190N-10.5HP-300x400.jpg',                                             'New',    FALSE,FALSE, TRUE),
(1,'Changchai DL24M 22HP',              'Changchai','DL24M',     '22HP DL24M engine widely used across Mymensingh Division for heavy irrigation and tilling.',                                                    'https://cbmbd.com/wp-content/uploads/2024/09/1.-Changchai-D.E-DL24M-22HP-300x400.jpg',                                               'Popular',TRUE, FALSE, FALSE),
(1,'Changchai 13KW 17HP Water Cooling', 'Changchai','13KW-17HP', 'Water-cooled single cylinder, 13KW/17HP. New arrival — excellent for pump and tiller drive.',                                                   'https://cbmbd.com/wp-content/uploads/2024/09/16.-Changchai-D.E-13kw_17hp_water_cooling_single_cylinder_diesel_engine-300x400.jpg',   'New',    FALSE,FALSE, TRUE),
(1,'Changchai T35 24KW',                'Changchai','T35',       'Powerful T35 24KW engine for heavy-duty farm and industrial applications.',                                                                      'https://cbmbd.com/wp-content/uploads/2024/09/19.-Changchai-T35-24-kw-300x400.jpg',                                                   'Hot',    TRUE, TRUE,  FALSE),
(1,'Changchai D-HS400 40HP (Self Start)','Changchai','D-HS400',  '40HP self-start heavy-duty engine. Top of the range for industrial and large-scale farming.',                                                   'https://cbmbd.com/wp-content/uploads/2024/09/14.-Changchai-D-HS400-40HP-Self-Starter-300x400.jpg',                                   'Hot',    TRUE, TRUE,  FALSE),
(1,'Jiangdong JD-190-NL Diesel Engine', 'Jiangdong','JD-190-NL', 'Jiangdong JD-190-NL diesel engine. A solid choice for agricultural machinery applications.',                                                    'https://cbmbd.com/wp-content/uploads/2024/09/11.-JD-190-NL-300x400.png',                                                              NULL,     FALSE,FALSE, FALSE),
(1,'Jiangdong S195n Diesel Engine',     'Jiangdong','S195n',     'Jiangdong S195n — dependable engine widely used in Bangladesh agricultural sector.',                                                            'https://cbmbd.com/wp-content/uploads/2024/09/12.-Jiangdong-Diesel-Engine-S195n-300x400.jpg',                                         NULL,     FALSE,FALSE, FALSE),
(1,'Sifang Engine S195GN',              'Sifang',   'S195GN',    'Sifang S195GN diesel engine. New stock — excellent price-to-performance ratio.',                                                               'https://cbmbd.com/wp-content/uploads/2024/09/13.-Sifang-Engine-S195GN-300x384.jpeg',                                                'New',    FALSE,FALSE, TRUE),

-- Power Tillers
(1,'ACI Power Tiller (Changchai Engine)','ACI Motors','Power Tiller','Premium ACI Power Tiller with Changchai diesel engine. Ideal for paddy cultivation in Jamalpur and surrounding districts.',              'https://cbmbd.com/wp-content/uploads/2024/09/Power-tiller-multi-function-vst-parts-name-300x400.jpg',                                 'Hot',    TRUE, TRUE,  FALSE),
(1,'CBM Power Tiller Multi Function',   'CBM Builders','Multi Function','CBM multi-function power tiller — robust frame designed for Bangladesh farming conditions.',                                            'https://cbmbd.com/wp-content/uploads/2024/09/Power-tiller-multi-function-vst-parts-name-300x400.jpg',                                 'Popular',TRUE, FALSE, FALSE),

-- Harvesters
(1,'4LBZ-150 Harvester',                'CBM','4LBZ-150',        'Compact 150cm cutting width paddy harvester for Jamalpur and Mymensingh region.',                                                              'https://cbmbd.com/wp-content/uploads/2024/09/4LBZ-150-Harvester-300x309.png',                                                         NULL,     FALSE,FALSE, FALSE),
(1,'4LBZ-150B Harvester',               'CBM','4LBZ-150B',       'Updated 4LBZ-150B harvester with improved efficiency. New stock arrived.',                                                                     'https://cbmbd.com/wp-content/uploads/2024/09/4LBZ-150B-Harvester-300x304.png',                                                        'New',    FALSE,FALSE, TRUE),

-- Generators
(2,'Changchai Generator 25HP Self-Start','Changchai','25HP Self-Start','Complete diesel generator set. 25HP self-start engine + alternator. For farms, mills across Mymensingh Division.',                      'https://cbmbd.com/wp-content/uploads/2024/09/14.-Changchai-D-HS400-40HP-Self-Starter-300x400.jpg',                                    'Hot',    TRUE, TRUE,  FALSE),
(2,'Changchai Generator 36HP / 25KW',   'Changchai','36HP/25KW', 'Heavy-duty 36HP/25KW self-start generator. Industrial and large-farm power supply. RPM: 2200.',                                              'https://cbmbd.com/wp-content/uploads/2024/09/14.-Changchai-D-HS400-40HP-Self-Starter-300x400.jpg',                                    'Hot',    TRUE, TRUE,  FALSE),
(2,'Shallow Machine (সেলো মেশিন)',      'Various',  'Shallow/Selo','Traditional shallow machine for efficient paddy field irrigation. Essential for Jamalpur, Tangail, Netrokona farmers.',                     'https://cbmbd.com/wp-content/uploads/2024/09/5.-Changchai-Diesel-ZS1110.jpg',                                                          'Popular',TRUE, FALSE, FALSE),
(2,'Mingdong 3KW Alternator ISO 9002',  'Mingdong', '3KW',       'ISO 9002 certified 3KW alternator with 100% copper wire. Compatible with standard diesel engines.',                                          'https://cbmbd.com/wp-content/uploads/2024/09/19.-Changchai-T35-24-kw-300x400.jpg',                                                    NULL,     FALSE,FALSE, FALSE),

-- Oils
(3,'Mobil Delvac Engine Oil',           'Mobil',    'Delvac Series','Genuine Mobil Delvac engine oil for diesel engines and power tillers. All SAE grades available.',                                          NULL,                                                                                                                                   'Hot',    TRUE, TRUE,  FALSE),
(3,'Gear Oil for Machines & Tillers',   'Various',  'Gear Oil',  'High-quality gear oil for power tillers and agricultural machines. Multiple grades available.',                                               NULL,                                                                                                                                   NULL,     FALSE,FALSE, FALSE),

-- Motors & Pumps
(4,'Gazi Jet Pump 1.0HP',               'Gazi',     'JSW-1HP',   'Popular Gazi 1HP jet pump. Reliable domestic and small-farm water supply pump.',                                                              NULL,                                                                                                                                   'Hot',    TRUE, TRUE,  FALSE),
(4,'LEO Jet Pump AJm Self-Priming',     'LEO Pump', 'AJm',       'Premium LEO AJm self-priming jet pump. AISI304 stainless impeller, anti-rust, 24-month warranty.',                                           NULL,                                                                                                                                   'New',    TRUE, FALSE, TRUE),
(4,'ACI Jet Pump 1HP JSW10m',           'ACI Motors','JSW10m',   'ACI Motors copper-wound coil jet pump. 1HP, 0.75KW. Trusted Bangladesh agricultural brand.',                                                 NULL,                                                                                                                                   'Popular',TRUE, FALSE, FALSE),
(4,'Marquis Jet Pump MJm/10M',          'Marquis',  'MJm/10M',   'Marquis premium jet pump — silent, reliable, long-lasting.',                                                                                 NULL,                                                                                                                                   NULL,     FALSE,FALSE, FALSE),
(4,'Walton Jet Pump 1HP Exclusive',     'Walton',   'JSW10M-X',  'Walton Exclusive Edition. 0.75KW, 2-year warranty, ISO 9001. Bangladesh brand.',                                                             NULL,                                                                                                                                   'New',    FALSE,FALSE, TRUE),
(4,'ACI Centrifugal Pump 3HP 4"x4"',    'ACI Motors','3HP 4x4',  'Heavy-duty ACI 3HP centrifugal pump for large-scale paddy irrigation. High flow 4x4 inch.',                                                  NULL,                                                                                                                                   'Hot',    TRUE, TRUE,  FALSE),
(4,'Pedrollo JSW Self-Priming (Italy)', 'Pedrollo', 'JSW',       'Premium Italian-made Pedrollo JSW self-priming pump. Made in Italy — exceptional quality.',                                                   NULL,                                                                                                                                   'Hot',    FALSE,TRUE,  FALSE),
(4,'BG Electric Motor 4P 5HP',          'BG',       '4P 5HP',    'BG brand 4-pole 5HP electric motor with aluminum casing. Drive for machines and pumps.',                                                     NULL,                                                                                                                                   NULL,     FALSE,FALSE, FALSE);

-- ── SEED: REVIEWS ────────────────────────────────────────────────────
INSERT INTO reviews (reviewer_name, reviewer_location, rating, review_text, is_approved) VALUES
('Md. Karim Hossain',    'Jamalpur Sadar',        5, 'সততা মেশিনারিজ স্টোর থেকে Changchai ইঞ্জিন কিনেছি। দাম নেগোশিয়েবল এবং সার্ভিস অনেক ভালো। স্টেশন রোডে সবচেয়ে ভালো দোকান!', TRUE),
('Rahim Uddin',          'Islampur, Jamalpur',    5, 'I bought an ACI Power Tiller from Sotota Machineries. The price was fair and delivery was fast. Highly recommend to all farmers in Mymensingh Division.', TRUE),
('Nur Mohammad',         'Sarishabari, Jamalpur', 5, 'LEO jet pump কিনেছিলাম। ওয়ারেন্টি সহ পেয়েছি এবং দোকানের মালিক অনেক হেল্পফুল। WhatsApp-এ দ্রুত রেসপন্স পাই।', TRUE),
('Abdul Mannan',         'Dewanganj, Jamalpur',   4, 'Great collection of diesel engines. Got the Changfa CF30M at a very reasonable price. Staff was very helpful and knowledgeable.', TRUE),
('Md. Shahidul Islam',   'Madarganj, Jamalpur',   5, 'সততা মেশিনারিজ থেকে Marquis পাম্প কিনে অনেক খুশি। হোম ডেলিভারি পেয়েছি।', TRUE),
('Sohel Rana',           'Netrokona',             5, 'Came from Netrokona for a Leo pump. Worth every kilometre! Best collection of motors and pumps in the entire Mymensingh region.', TRUE),
('Khairul Alam',         'Bhuapur, Tangail',      4, 'আমি ট্যাঙ্গাইল থেকে এসে Changchai জেনারেটর কিনেছি। পণ্যের মান অনেক ভালো।', TRUE),
('Farida Begum',         'Melandaha, Jamalpur',   5, 'Best shop in Jamalpur for home and kitchen accessories. Got all bathroom fittings at one place. Very satisfied.', TRUE);
