from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, MovieInfo, ActorInfo, MovieBox, MovieActorRelation


@app.route('/',methods=['GET','POST'])
def index():

    movie_info = None
    # 检查是否有查询参数
    movie_name = request.args.get('movie_name')
    if movie_name:
    # 查询电影信息
        movie_info = MovieInfo.query.filter_by(movie_name=movie_name).all()
        if movie_info:
            movie_id=movie_info[0].movie_id
            box_info=MovieBox.query.filter_by(movie_id=movie_id).first()
            # 查询与电影相关联的演员信息和关系类型
            actor_relations = MovieActorRelation.query.filter_by(movie_id=movie_id).all()
            actors_info=[]
            for relation in actor_relations:
                actor_id=relation.actor_id
                relation_type=relation.relation_type
                # 查询演员的姓名
                actor_info = ActorInfo.query.filter_by(actor_id=actor_id).first()

                if actor_info:
                    actor_name = actor_info.actor_name
                    actors_info.append({"actor_name": actor_name, "relation_type": relation_type})

            return render_template('index.html', movie_info=movie_info, actors_info=actors_info, box_info=box_info)
    #return render_template('index.html', movie_info=movie_info)
    actor_name = request.args.get('actor_name')
    if actor_name:
        actor_info=ActorInfo.query.filter_by(actor_name=actor_name).first()
        if actor_info:
            movies_info=[]
            actor_id=actor_info.actor_id
            movies_related = MovieActorRelation.query.filter_by(actor_id=actor_id).all()
            for movie_related in movies_related:
                movie_id=movie_related.movie_id
                relation_type=movie_related.relation_type
                movie=MovieInfo.query.filter_by(movie_id=movie_id).first()
                if movie:
                    movie_name=movie.movie_name
                    movies_info.append({"movie_name": movie_name, "relation_type": relation_type})
            return render_template('index.html', actor_info=actor_info, movies_info=movies_info)

    return render_template('index.html')
"""
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)
"""
"""
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))
"""

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/movie_info')
#@login_required
def movie_info():
    movies = MovieInfo.query.all()
    movies_box = MovieBox.query.all()
    actors=ActorInfo.query.all()
    relations= MovieActorRelation.query.all()
    return render_template('movie_info.html', actors=actors,relations=relations,movies=movies,movies_box=movies_box,)

@app.route('/actor_info')
def actor_info():
    actors=ActorInfo.query.all()
    return render_template('actor_info.html',actors=actors)

# 编辑 MovieInfo 的视图函数
@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
#@login_required
def edit_movie(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    movie_box = MovieBox.query.filter_by(movie_id=movie_id).first()
    #actors_info=ActorInfo.query.all()
    movie_actor_relations = MovieActorRelation.query.filter_by(movie_id=movie_id).all()
    actors=[]
    for relation in movie_actor_relations:
        actor_id=relation.actor_id
        actor=ActorInfo.query.get(actor_id)
        if actor and not any(a.actor_id == actor_id for a in actors):
            actors.append(actor)
    if request.method == 'POST':
        # 处理编辑表单的提交
        movie.movie_name = request.form['new_movie_name']
        release_date_str = request.form.get('new_release_date')
        movie.release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        movie.country = request.form['new_country']
        movie.type = request.form['new_type']
        movie.year = request.form['new_year']
        movie_box.box = request.form['new_box']
        for relation in movie_actor_relations:
            #actor_id=relation.actor_id
            actor_id=relation.actor_id
            actor=ActorInfo.query.get(actor_id)
            if actor:
                actor.actor_name = request.form.get(f'new_actor_name_{actor_id}')
                actor.gender = request.form.get(f'new_gender_{actor_id}')
                actor.country = request.form.get(f'new_country_{actor_id}')
                relation.relation_type=request.form.get(f'new_relation_type_{actor_id}')
        db.session.commit()
        flash('Movie information updated successfully', 'success')
        return redirect(url_for('movie_info'))

    return render_template('edit_movie.html', actors=actors, movie=movie, movie_box=movie_box, movie_actor_relations=movie_actor_relations)
# 删除 MovieInfo 的视图函数
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
#@login_required
def delete_movie(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully', 'success')
    return redirect(url_for('movie_info'))

'''@app.route('/create_movie', methods=['GET', 'POST'])
def create_movie():
    if request.method == 'POST':
        try:
            # 获取表单数据
            movie_id = request.form.get('movie_id')
            movie_name = request.form.get('movie_name')
            country = request.form.get('country')
            movie_type = request.form.get('type')
            movie_year = request.form.get('year')

            # 创建新的MovieInfo对象并添加到数据库
            new_movie = MovieInfo(movie_id=movie_id, movie_name=movie_name, country=country, type=movie_type, year=movie_year)
            db.session.add(new_movie)
            db.session.commit()

            # 重定向到MovieInfo页面，显示新添加的电影
            return redirect(url_for('movie_info'))
        except IntegrityError:
            # 主键冲突，回滚事务并显示错误消息给用户
            db.session.rollback()
            error_message = "Movie ID already exists. Please choose a different ID."
            return render_template('create_movie.html', error_message=error_message)
    # 如果是 GET 请求，渲染创建新MovieInfo的页面
    return render_template('create_movie.html')'''


from datetime import datetime

@app.route('/create_movie_info', methods=['GET', 'POST'])
def create_movie_info():
    if request.method == 'POST':
        # 从表单获取数据
        movie_name = request.form.get('movie_name')
        release_date_str = request.form.get('release_date')
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        country = request.form.get('country')
        type = request.form.get('type')
        year = request.form.get('year')
        box_office = request.form.get('box')

        # 检查电影是否已存在
        existing_movie = MovieInfo.query.filter_by(movie_name=movie_name).first()
        if existing_movie:
            flash('Movie already exists.')
            return redirect(url_for('create_movie_info'))

        # 添加电影信息到数据库
        new_movie = MovieInfo(movie_name=movie_name, release_date=release_date, country=country, type=type, year=year)
        db.session.add(new_movie)
        db.session.commit()

        # 添加票房信息
        new_movie_box = MovieBox(movie_id=new_movie.movie_id, box=box_office)
        db.session.add(new_movie_box)
        db.session.commit()

        # 添加演员信息
        for i in range(1, 3):  # 假设有两个演员字段
            actor_name = request.form.get(f'actor_name_{i}')
            relation_type = request.form.get(f'relation_type_{i}')
            gender=request.form.get(f'gender_{i}')
            country=request.form.get(f'country_{i}')
            if actor_name:
                # 检查演员是否存在
                actor = ActorInfo.query.filter_by(actor_name=actor_name).first()
                if not actor:
                    actor = ActorInfo(actor_name=actor_name, gender=gender, country=country)
                    db.session.add(actor)
                    db.session.commit()

                # 添加电影和演员的关系
                new_relation = MovieActorRelation(movie_id=new_movie.movie_id, actor_id=actor.actor_id, relation_type=relation_type)
                db.session.add(new_relation)
                db.session.commit()

        flash('Movie added successfully.')
        return redirect(url_for('index'))

    return render_template('create_movie_info.html')
