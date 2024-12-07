from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 資料模型
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)  # 新增書籍內容欄位

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 初始化資料庫
with app.app_context():
    db.create_all()

    if not Book.query.first():
        books = [
            Book(
                book_name="To Kill a Mockingbird",
                author="Harper Lee",
                description="A novel about the serious issues of race and rape.",
                image_filename="book1.jpg",
                content="Voted America's Best-Loved Novel in PBS's The Great American Read.\nHarper Lee's Pulitzer Prize-winning masterwork of honor and injustice in the deep South--and the heroism of one man in the face of blind and violent hatred.\nOne of the most cherished stories of all time, To Kill a Mockingbird has been translated into more than forty languages, sold more than forty million copies worldwide, served as the basis for an enormously popular motion picture, and was voted one of the best novels of the twentieth century by librarians across the country. A gripping, heart-wrenching, and wholly remarkable tale of coming-of-age in a South poisoned by virulent prejudice, it views a world of great beauty and savage inequities through the eyes of a young girl, as her father--a crusading local lawyer--risks everything to defend a black man unjustly accused of a terrible crime."
            ),
            Book(
                book_name="1984",
                author="George Orwell",
                description="A dystopian novel set in a totalitarian society.",
                image_filename="book2.jpg",
                content="戰爭即和平  自由即奴役  無知即力量\n大洋國外戰頻繁，領導者老大哥監視人民生活，控制思想語言，吹噓整體昌盛和諧，但凡發現思想不正確者，隨時人間蒸發。\n負責篡改資訊、改寫歷史的小黨員溫斯頓對現實漸生懷疑，個人回憶不可信？狗臉的生活比以往幸福？有獨立思考就要改造？一團團的疑問，暗黑中的反抗行為，令他一步步走向黨的圏套，跌入無止的酷刑、洗腦和再教育之中。\n反烏托邦小說《1984》讓讀者直面極權統治的殘酷與扭曲，人民盲從、缺乏個人思辨和批判能力的危險。表面是井然有序、和諧安穩的社會，內裏卻是權力過大、箝制思想、剝奪自由的中央集權制度。小說中強大的預警都一一出現在現實世界，我們願意被喚醒去看清現實，嘗試改變未來嗎？"
            ),
            Book(
                book_name="The Great Gatsby",
                author="F. Scott Fitzgerald",
                description="A story of wealth, ambition, and love.",
                image_filename="book3.jpg",
                content="The only edition of the beloved classic that is authorized by Fitzgerald’s family and from his lifelong publisher.\nThis edition is the enduring original text, updated with the author’s own revisions, a foreword by his granddaughter, and with a new introduction by National Book Award winner Jesmyn Ward.\nThe Great Gatsby, F. Scott Fitzgerald’s third book, stands as the supreme achievement of his career. First published by Scribner in 1925, this quintessential novel of the Jazz Age has been acclaimed by generations of readers. The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan is an exquisitely crafted tale of America in the 1920s."
            ),
            Book(
                book_name="Pride and Prejudice",
                author="Jane Austen",
                description="A romantic novel about manners and matrimonial machinations.",
                image_filename="book4.jpg",
                content="因為自身條件的優越，加上對於環境人物的不熟悉，達西先生以冷漠傲然的態度作出人們與自己的區隔，卻也讓人們認定他的傲慢。直到目空一切的達西先生發現了伊莉莎白的魅力，並深陷其中……\n達西在舞會上的一席話，讓伊莉莎白認定了他的傲慢，加上旁人的挑撥，更是讓她深信兩人的不合，這種偏見讓伊莉莎白努力的拉開達西與自己的距離。可是種種的因緣際會和事件的發生，卻意外促進了兩人的愛情……\n一部最能改變女性對自己評價的文學作品，在傲慢與偏見之間，細細品味珍奧斯汀的理性與感性。\nNominated as one of America's best-loved novels by PBS's The Great American Read\nIt is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife. So begins Pride and Prejudice, Jane Austen's witty comedy of manners--one of the most popular novels of all time--that features splendidly civilized sparring between the proud Mr. Darcy and the prejudiced Elizabeth Bennet as they play out their spirited courtship in a series of eighteenth-century drawing-room intrigues. Renowned literary critic and historian George Saintsbury in 1894 declared it the most perfect, the most characteristic, the most eminently quintessential of its author's works, and Eudora Welty in the twentieth century described it as irresistible and as nearly flawless as any fiction could be."
            ),
            Book(
                book_name="Moby-Dick",
                author="Herman Melville",
                description="An epic tale of obsession and revenge.",
                image_filename="book5.jpg",
                content="Collector’s Edition Laminated Hardback with Jacket\nA restless sailor named Ishmael signs up for what he believes will be an adventurous whaling voyage, but quickly finds himself aboard the Pequod, a ship with a far darker purpose. Its captain, the grim and mysterious Ahab, is consumed by a burning desire to hunt down Moby Dick, the elusive white whale that once maimed him. As they journey deeper into the vast, unforgiving ocean, it becomes clear that Ahab’s obsession is dragging the crew into something far more dangerous than they imagined. The voyage turns into a gripping struggle between man, nature, and the consuming power of vengeance.\nMoby Dick holds a significant place in literary history as one of the greatest American novels, though it was largely unrecognized in its time. Melville’s exploration of themes like obsession, the human condition, and man’s relationship with nature reflected the changing tides of 19th-century thought. His innovative narrative structure, blending adventure with philosophical reflection, laid the groundwork for modernist literature. Over time, the novel has been rediscovered and celebrated for its profound depth and complexity, cementing its status as a cornerstone of American literary tradition."
            )
        ]
        db.session.add_all(books)
        db.session.commit()

# 路由定義

# 首頁
@app.route('/')
@login_required  # 確保登入後才能進入
def index():
    books = Book.query.limit(5).all()  # 顯示前五本書籍
    return render_template('index.html', books=books)

# 書籍詳細頁面
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)

    # 若是借閱按鈕被按下
    if request.method == 'POST':
        flash(f"已成功借閱《{book.book_name}》！", 'success')

    return render_template('book_detail.html', book=book)

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        # 檢查帳號是否已經註冊
        if User.query.filter_by(username=username).first():
            flash('帳號已經被註冊!', 'danger')
            return redirect('/register')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('註冊成功，請登入!', 'success')
        return redirect('/login')

    return render_template('register.html')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 嘗試從資料庫查找使用者
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('登入成功!', 'success')
            return redirect('/')  # 成功登入後導向到首頁

        flash('登入失敗，請檢查帳號或密碼!', 'danger')
        return redirect('/login')

    return render_template('login.html')

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    # 這裡可以處理借閱邏輯，現在簡單地顯示借閱成功訊息
    book = Book.query.get_or_404(book_id)
    
    # 這邊可以擴展邏輯，像是將借閱的書籍資訊存入資料庫、更新借閱狀態等
    
    flash(f'You have successfully borrowed《{book.book_name}》!', 'success')
    return redirect(url_for('book_detail', book_id=book_id))


# 登出處理
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出!', 'success')
    return redirect('/login')

# 取得所有書籍 (JSON 格式)
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_data = [
        {
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'description': book.description,
            'image_filename': book.image_filename
        }
        for book in books
    ]
    return jsonify(books_data)

# 運行應用
if __name__ == '__main__':
    app.run(debug=True, port=5000)
