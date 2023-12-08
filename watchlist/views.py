from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, MovieInfo, ActorInfo, MovieBox, MovieActorRelation


@app.route('/',methods=['GET','POST'])
def index():

    return render_template('index.html')


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
    search = request.args.get('search')
    search_found = False  # 添加标志
    if search:
        movies_search = MovieInfo.query.filter(MovieInfo.movie_name.like(f'%{search}%')).all()
        if movies_search:
            search_found = True
        return render_template('movie_info.html', actors=actors,relations=relations,movies=movies,movies_box=movies_box,movies_search=movies_search,search_found=search_found)
    return render_template('movie_info.html', actors=actors,relations=relations,movies=movies,movies_box=movies_box)



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
        # 处理新增的演员信息
        for i in range(1, 11):  # 假设最多可以添加10个新演员
            if f'new_actor_name_{i}' in request.form:
                new_actor_name = request.form.get(f'new_actor_name_{i}')
                new_actor_gender = request.form.get(f'new_gender_{i}')
                new_actor_country = request.form.get(f'new_country_{i}')
                new_relation_type = request.form.get(f'new_relation_type_{i}')

                # 检查 ActorInfo 表中是否已存在该演员
                actor = ActorInfo.query.filter_by(actor_name=new_actor_name).first()
                if not actor:
                    # 如果不存在，创建新的 ActorInfo 记录
                    actor = ActorInfo(actor_name=new_actor_name, gender=new_actor_gender, country=new_actor_country)
                    db.session.add(actor)
                    db.session.flush()  # 生成 actor 的 ID

                # 创建新的 MovieActorRelation 记录
                new_relation = MovieActorRelation(movie_id=movie_id, actor_id=actor.actor_id, relation_type=new_relation_type)
                db.session.add(new_relation)
        for relation in movie_actor_relations:
            if request.form.get(f'delete_actor_{relation.actor_id}'):
                db.session.delete(relation)

        db.session.commit()
        flash('Movie information updated successfully', 'success')
        return redirect(url_for('movie_info'))

    return render_template('edit_movie.html', actors=actors, movie=movie, movie_box=movie_box, movie_actor_relations=movie_actor_relations)
# 删除 MovieInfo 的视图函数
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
#@login_required
def delete_movie(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    # 删除与电影相关的票房信息
    MovieBox.query.filter_by(movie_id=movie_id).delete()

    # 删除与电影相关的所有演员关系
    MovieActorRelation.query.filter_by(movie_id=movie_id).delete()
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully', 'success')
    return redirect(url_for('movie_info'))

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    movie_actor_relations = MovieActorRelation.query.filter_by(movie_id=movie_id).all()
    movie_box = MovieBox.query.filter_by(movie_id=movie_id).first()
    actors_info=[]
    for relation in movie_actor_relations:
        actor_id=relation.actor_id
        relation_type=relation.relation_type
        # 查询演员的姓名
        actor_info = ActorInfo.query.filter_by(actor_id=actor_id).first()

        if actor_info:
            actor_name = actor_info.actor_name
            actors_info.append({"actor_name": actor_name, "relation_type": relation_type})
    return render_template('movie_detail.html', movie=movie, movie_box=movie_box, actors_info = actors_info)

@app.route('/actor_info')
def actor_info():
    actors=ActorInfo.query.all()
    search = request.args.get('search')
    search_found = False  # 添加标志
    if search:
        actors_search = ActorInfo.query.filter(ActorInfo.actor_name.like(f'%{search}%')).all()
        if actors_search:
            search_found = True
        return render_template('actor_info.html', actors=actors,actors_search=actors_search,search_found=search_found)
    return render_template('actor_info.html',actors=actors)

@app.route('/actor/<int:actor_id>')
def actor_detail(actor_id):
    actor = ActorInfo.query.get_or_404(actor_id)
    movie_actor_relations = MovieActorRelation.query.filter_by(actor_id=actor_id).all()
    movies_info=[]
    for relation in movie_actor_relations:
        movie_id=relation.movie_id
        relation_type=relation.relation_type
        # 查询演员的姓名
        movie_info = MovieInfo.query.filter_by(movie_id=movie_id).first()
        if movie_info:
            movie_name = movie_info.movie_name
            movies_info.append({"movie_name": movie_name, "relation_type": relation_type})
    return render_template('actor_detail.html', actor=actor, movies_info = movies_info)

@app.route('/delete_actor/<int:actor_id>', methods=['POST'])
#@login_required
def delete_actor(actor_id):
    actor = ActorInfo.query.get_or_404(actor_id)
    # 删除与电影相关的所有演员关系
    MovieActorRelation.query.filter_by(actor_id=actor_id).delete()
    db.session.delete(actor)
    db.session.commit()
    flash('Actor deleted successfully', 'success')
    return redirect(url_for('actor_info'))

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
        for i in range(1, 6):  # 假设有两个演员字段
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




@app.route('/box_office')
def box_office():
    top_boxes = MovieBox.query.order_by(MovieBox.box.desc()).limit(10).all()
    top_movies = []
    for box in top_boxes:
        movie = MovieInfo.query.filter_by(movie_id=box.movie_id).first()
        if movie:
            top_movies.append({'movie_name': movie.movie_name, 'box': box.box})
    # 按电影类别统计票房总和
    type_box_office = db.session.query(
        MovieInfo.type, db.func.sum(MovieBox.box).label('total_box')
    ).join(MovieBox, MovieInfo.movie_id == MovieBox.movie_id)\
     .group_by(MovieInfo.type)\
     .all()

    # 按电影年份统计票房总和
    year_box_office = db.session.query(
        MovieInfo.year, db.func.sum(MovieBox.box).label('total_box')
    ).join(MovieBox, MovieInfo.movie_id == MovieBox.movie_id)\
     .group_by(MovieInfo.year)\
     .all()
    return render_template('box_office.html', top_movies=top_movies,type_box_office=type_box_office,year_box_office=year_box_office)
