import click
from datetime import datetime
from watchlist import app, db
from watchlist.models import User, MovieInfo, MovieBox, ActorInfo, MovieActorRelation


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Hejiong Cai'
    #MovieInfo
    movies = [
        {'movie_id': 1001, 'movie_name': '战狼2', 'release_date': datetime.strptime('2017/7/27', '%Y/%m/%d'), 'country': '中国', 'type': '战争', 'year': 2017},
        {'movie_id': 1002, 'movie_name': '哪吒之魔童降世', 'release_date': datetime.strptime('2019/7/26', '%Y/%m/%d'),'country': '中国', 'type': '动画', 'year': 2019},
        {'movie_id': 1003, 'movie_name': '流浪地球', 'release_date': datetime.strptime('2019/2/5', '%Y/%m/%d'),'country': '中国', 'type': '科幻', 'year': 2019},
        {'movie_id': 1004, 'movie_name': '复仇者联盟4', 'release_date': datetime.strptime('2019/4/24', '%Y/%m/%d'),'country': '美国', 'type': '科幻', 'year': 2019},
        {'movie_id': 1005, 'movie_name': '红海行动', 'release_date': datetime.strptime('2018/2/16', '%Y/%m/%d'),'country': '中国', 'type': '战争', 'year': 2018},
        {'movie_id': 1006, 'movie_name': '唐人街探案2', 'release_date': datetime.strptime('2018/2/16', '%Y/%m/%d'),'country': '中国', 'type': '喜剧', 'year': 2018},
        {'movie_id': 1007, 'movie_name': '我不是药神', 'release_date': datetime.strptime('2018/7/5', '%Y/%m/%d'),'country': '中国', 'type': '喜剧', 'year': 2018},
        {'movie_id': 1008, 'movie_name': '中国机长', 'release_date': datetime.strptime('2019/9/30', '%Y/%m/%d'),'country': '中国', 'type': '剧情', 'year': 2019},
        {'movie_id': 1009, 'movie_name': '速度与激情8', 'release_date': datetime.strptime('2017/4/14', '%Y/%m/%d'),'country': '美国', 'type': '动作', 'year': 2017},
        {'movie_id': 1010, 'movie_name': '西虹市首富', 'release_date': datetime.strptime('2018/7/27', '%Y/%m/%d'),'country': '中国', 'type': '喜剧', 'year': 2018},
        {'movie_id': 1011, 'movie_name': '复仇者联盟3', 'release_date': datetime.strptime('2018/5/11', '%Y/%m/%d'),'country': '美国', 'type': '科幻', 'year': 2018},
        {'movie_id': 1012, 'movie_name': '捉妖记2', 'release_date': datetime.strptime('2018/2/16', '%Y/%m/%d'),'country': '中国', 'type': '喜剧', 'year': 2018},
        {'movie_id': 1013, 'movie_name': '八佰', 'release_date': datetime.strptime('2020/08/21', '%Y/%m/%d'),'country': '中国', 'type': '战争', 'year': 2020},
        {'movie_id': 1014, 'movie_name': '姜子牙', 'release_date': datetime.strptime('2020/10/01', '%Y/%m/%d'),'country': '中国', 'type': '战争', 'year': 2021},
        {'movie_id': 1015, 'movie_name': '我和我的家乡', 'release_date': datetime.strptime('2020/10/01', '%Y/%m/%d'), 'country': '中国', 'type': '剧情', 'year': 2020},
        {'movie_id': 1016, 'movie_name': '你好，李焕英', 'release_date': datetime.strptime('2021/02/12', '%Y/%m/%d'), 'country': '中国', 'type': '喜剧', 'year': 2021},
        {'movie_id': 1017, 'movie_name': '长津湖', 'release_date': datetime.strptime('2021/09/30', '%Y/%m/%d'), 'country': '中国', 'type': '战争', 'year': 2021},
        {'movie_id': 1018, 'movie_name': '速度与激情9', 'release_date': datetime.strptime('2021/05/21', '%Y/%m/%d'), 'country': '中国', 'type': '动作', 'year': 2021},
        ]

    for movie_data in movies:
        movie = MovieInfo(
            movie_id=movie_data['movie_id'],
            movie_name=movie_data['movie_name'],
            release_date=movie_data['release_date'],
            country=movie_data['country'],
            type=movie_data['type'],
            year=movie_data['year']
        )
        db.session.add(movie)

    #MovieBox
    movie_boxes = [
    {'movie_id': 1001, 'box': 56.84},
    {'movie_id': 1002, 'box': 50.15},
    {'movie_id': 1003, 'box': 46.86},
    {'movie_id': 1004, 'box': 42.5},
    {'movie_id': 1005, 'box': 36.5},
    {'movie_id': 1006, 'box': 33.97},
    {'movie_id': 1007, 'box': 31},
    {'movie_id': 1008, 'box': 29.12},
    {'movie_id': 1009, 'box': 26.7},
    {'movie_id': 1010, 'box': 25.47},
    {'movie_id': 1011, 'box': 23.9},
    {'movie_id': 1012, 'box': 22.37},
    {'movie_id': 1013, 'box': 30.10},
    {'movie_id': 1014, 'box': 16.02},
    {'movie_id': 1015, 'box': 28.29},
    {'movie_id': 1016, 'box': 54.13},
    {'movie_id': 1017, 'box': 53.48},
    {'movie_id': 1018, 'box': 13.92},
]
    for box_data in movie_boxes:
        box = MovieBox(
            movie_id=box_data['movie_id'],
            box=box_data['box']
        )
        db.session.add(box)

    #ActorInfo
    actor_info = [
    {'actor_id': 2001, 'actor_name': '吴京', 'gender': '男', 'country': '中国'},
    {'actor_id': 2002, 'actor_name': '饺子', 'gender': '男', 'country': '中国'},
    {'actor_id': 2003, 'actor_name': '屈楚萧', 'gender': '男', 'country': '中国'},
    {'actor_id': 2004, 'actor_name': '郭帆', 'gender': '男', 'country': '中国'},
    {'actor_id': 2005, 'actor_name': '乔罗素', 'gender': '男', 'country': '美国'},
    {'actor_id': 2006, 'actor_name': '小罗伯特·唐尼', 'gender': '男', 'country': '美国'},
    {'actor_id': 2007, 'actor_name': '克里斯·埃文斯', 'gender': '男', 'country': '美国'},
    {'actor_id': 2008, 'actor_name': '林超贤', 'gender': '男', 'country': '中国'},
    {'actor_id': 2009, 'actor_name': '张译', 'gender': '男', 'country': '中国'},
    {'actor_id': 2010, 'actor_name': '黄景瑜', 'gender': '男', 'country': '中国'},
    {'actor_id': 2011, 'actor_name': '陈思诚', 'gender': '男', 'country': '中国'},
    {'actor_id': 2012, 'actor_name': '王宝强', 'gender': '男', 'country': '中国'},
    {'actor_id': 2013, 'actor_name': '刘昊然', 'gender': '男', 'country': '中国'},
    {'actor_id': 2014, 'actor_name': '文牧野', 'gender': '男', 'country': '中国'},
    {'actor_id': 2015, 'actor_name': '徐峥', 'gender': '男', 'country': '中国'},
    {'actor_id': 2016, 'actor_name': '刘伟强', 'gender': '男', 'country': '中国'},
    {'actor_id': 2017, 'actor_name': '张涵予', 'gender': '男', 'country': '中国'},
    {'actor_id': 2018, 'actor_name': 'F·加里·格雷', 'gender': '男', 'country': '美国'},
    {'actor_id': 2019, 'actor_name': '范·迪塞尔', 'gender': '男', 'country': '美国'},
    {'actor_id': 2020, 'actor_name': '杰森·斯坦森', 'gender': '男', 'country': '美国'},
    {'actor_id': 2021, 'actor_name': '闫非', 'gender': '男', 'country': '中国'},
    {'actor_id': 2022, 'actor_name': '沈腾', 'gender': '男', 'country': '中国'},
    {'actor_id': 2023, 'actor_name': '安东尼·罗素', 'gender': '男', 'country': '美国'},
    {'actor_id': 2024, 'actor_name': '克里斯·海姆斯沃斯', 'gender': '男', 'country': '美国'},
    {'actor_id': 2025, 'actor_name': '许诚毅', 'gender': '男', 'country': '中国'},
    {'actor_id': 2026, 'actor_name': '梁朝伟', 'gender': '男', 'country': '中国'},
    {'actor_id': 2027, 'actor_name': '白百何', 'gender': '女', 'country': '中国'},
    {'actor_id': 2028, 'actor_name': '井柏然', 'gender': '男', 'country': '中国'},
    {'actor_id': 2029, 'actor_name': '管虎', 'gender': '男', 'country': '中国'},
    {'actor_id': 2030, 'actor_name': '王千源', 'gender': '男', 'country': '中国'},
    {'actor_id': 2031, 'actor_name': '姜武', 'gender': '男', 'country': '中国'},
    {'actor_id': 2032, 'actor_name': '宁浩', 'gender': '男', 'country': '中国'},
    {'actor_id': 2033, 'actor_name': '葛优', 'gender': '男', 'country': '中国'},
    {'actor_id': 2034, 'actor_name': '范伟', 'gender': '男', 'country': '中国'},
    {'actor_id': 2035, 'actor_name': '贾玲', 'gender': '女', 'country': '中国'},
    {'actor_id': 2036, 'actor_name': '张小斐', 'gender': '女', 'country': '中国'},
    {'actor_id': 2037, 'actor_name': '陈凯歌', 'gender': '男', 'country': '中国'},
    {'actor_id': 2038, 'actor_name': '徐克', 'gender': '男', 'country': '中国'},
    {'actor_id': 2039, 'actor_name': '易烊千玺', 'gender': '男', 'country': '中国'},
    {'actor_id': 2040, 'actor_name': '林诣彬', 'gender': '男', 'country': '美国'},
    {'actor_id': 2041, 'actor_name': '米歇尔·罗德里格兹', 'gender': '女', 'country': '美国'},
]

    for actor_data in actor_info:
        actor = ActorInfo(
            actor_id=actor_data['actor_id'],
            actor_name=actor_data['actor_name'],
            gender=actor_data['gender'],
            country=actor_data['country']
        )
        db.session.add(actor)

    #MovieActorRelation
    movie_actor_relation = [
    {'movie_id': 1001, 'actor_id': 2001, 'relation_type': '主演'},
    {'movie_id': 1001, 'actor_id': 2001, 'relation_type': '导演'},
    {'movie_id': 1002, 'actor_id': 2002, 'relation_type': '导演'},
    {'movie_id': 1003, 'actor_id': 2001, 'relation_type': '主演'},
    {'movie_id': 1003, 'actor_id': 2003, 'relation_type': '主演'},
    {'movie_id': 1003, 'actor_id': 2004, 'relation_type': '导演'},
    {'movie_id': 1004, 'actor_id': 2005, 'relation_type': '导演'},
    {'movie_id': 1004, 'actor_id': 2006, 'relation_type': '主演'},
    {'movie_id': 1004, 'actor_id': 2007, 'relation_type': '主演'},
    {'movie_id': 1005, 'actor_id': 2008, 'relation_type': '导演'},
    {'movie_id': 1005, 'actor_id': 2009, 'relation_type': '主演'},
    {'movie_id': 1005, 'actor_id': 2010, 'relation_type': '主演'},
    {'movie_id': 1006, 'actor_id': 2011, 'relation_type': '导演'},
    {'movie_id': 1006, 'actor_id': 2012, 'relation_type': '主演'},
    {'movie_id': 1006, 'actor_id': 2013, 'relation_type': '主演'},
    {'movie_id': 1007, 'actor_id': 2014, 'relation_type': '导演'},
    {'movie_id': 1007, 'actor_id': 2015, 'relation_type': '主演'},
    {'movie_id': 1008, 'actor_id': 2016, 'relation_type': '导演'},
    {'movie_id': 1008, 'actor_id': 2017, 'relation_type': '主演'},
    {'movie_id': 1009, 'actor_id': 2018, 'relation_type': '导演'},
    {'movie_id': 1009, 'actor_id': 2019, 'relation_type': '主演'},
    {'movie_id': 1009, 'actor_id': 2020, 'relation_type': '主演'},
    {'movie_id': 1010, 'actor_id': 2021, 'relation_type': '导演'},
    {'movie_id': 1010, 'actor_id': 2022, 'relation_type': '主演'},
    {'movie_id': 1011, 'actor_id': 2023, 'relation_type': '导演'},
    {'movie_id': 1011, 'actor_id': 2006, 'relation_type': '主演'},
    {'movie_id': 1011, 'actor_id': 2024, 'relation_type': '主演'},
    {'movie_id': 1012, 'actor_id': 2025, 'relation_type': '导演'},
    {'movie_id': 1012, 'actor_id': 2026, 'relation_type': '主演'},
    {'movie_id': 1012, 'actor_id': 2027, 'relation_type': '主演'},
    {'movie_id': 1012, 'actor_id': 2028, 'relation_type': '主演'},
    {'movie_id': 1013, 'actor_id': 2029, 'relation_type': '导演'},
    {'movie_id': 1013, 'actor_id': 2030, 'relation_type': '主演'},
    {'movie_id': 1013, 'actor_id': 2009, 'relation_type': '主演'},
    {'movie_id': 1013, 'actor_id': 2031, 'relation_type': '主演'},
    {'movie_id': 1015, 'actor_id': 2032, 'relation_type': '导演'},
    {'movie_id': 1015, 'actor_id': 2015, 'relation_type': '导演'},
    {'movie_id': 1015, 'actor_id': 2011, 'relation_type': '导演'},
    {'movie_id': 1015, 'actor_id': 2015, 'relation_type': '主演'},
    {'movie_id': 1015, 'actor_id': 2033, 'relation_type': '主演'},
    {'movie_id': 1015, 'actor_id': 2034, 'relation_type': '主演'},
    {'movie_id': 1016, 'actor_id': 2035, 'relation_type': '导演'},
    {'movie_id': 1016, 'actor_id': 2035, 'relation_type': '主演'},
    {'movie_id': 1016, 'actor_id': 2036, 'relation_type': '主演'},
    {'movie_id': 1016, 'actor_id': 2022, 'relation_type': '主演'},
    {'movie_id': 1017, 'actor_id': 2037, 'relation_type': '导演'},
    {'movie_id': 1017, 'actor_id': 2038, 'relation_type': '导演'},
    {'movie_id': 1017, 'actor_id': 2008, 'relation_type': '导演'},
    {'movie_id': 1017, 'actor_id': 2001, 'relation_type': '主演'},
    {'movie_id': 1017, 'actor_id': 2039, 'relation_type': '主演'},
    {'movie_id': 1018, 'actor_id': 2040, 'relation_type': '导演'},
    {'movie_id': 1018, 'actor_id': 2019, 'relation_type': '主演'},
    {'movie_id': 1018, 'actor_id': 2041, 'relation_type': '主演'},
]

    for relation_data in movie_actor_relation:
        relation = MovieActorRelation(
            movie_id=relation_data['movie_id'],
            actor_id=relation_data['actor_id'],
            relation_type=relation_data['relation_type']
        )
        db.session.add(relation)

    user = User(name=name)
    db.session.add(user)


    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
