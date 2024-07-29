from app import *
from backend.settings.settings import *
from backend.student import *

from datetime import datetime
from backend.models.basic_model import *


@app.route('/change_coin', methods=["POST", "GET"])
def change_coin():
    info = request.get_json()['info']
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    filtered_year = Years.query.filter(Years.year == int(year)).first()
    filtered_month = Month.query.filter(Month.month_number == int(month), Month.years_id == filtered_year.id).first()
    filtered_day = Day.query.filter(Day.day_number == int(day), Day.month_id == filtered_month.id,
                                    Day.year_id == filtered_year.id).first()
    filtered_coin = ClassCoins.query.filter(ClassCoins.class_id == info["class_id"],
                                            ClassCoins.year_id == filtered_year.id,
                                            ClassCoins.month_id == filtered_month.id).first()
    overhead = 0

    if info["type"] == "true":
        if not filtered_coin:
            add_coin = ClassCoins(class_id=info["class_id"], year_id=filtered_year.id, month_id=filtered_month.id,
                                  coins=0,
                                  given_coins=0, rest_coins=info["count"])
            db.session.add(add_coin)
            db.session.commit()
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=add_coin.id, coins=info["count"], type=True,
                                                  day_id=filtered_day.id, reason=info["reason"])
            db.session.add(add_coin_by_month)
            db.session.commit()
            fl_coin = ClassCoins.query.filter(ClassCoins.id == add_coin.id).first()
            coins = 0
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins

            ClassCoins.query.filter(ClassCoins.id == add_coin.id).update({
                "coins": coins
            })
            db.session.commit()
            update_overall_coins()
        else:
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=filtered_coin.id, coins=info["count"], type=True,
                                                  day_id=filtered_day.id, reason=info["reason"])
            db.session.add(add_coin_by_month)
            db.session.commit()
            fl_coin = ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).first()
            coins = 0
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins
            for coin_by_month in filtered_coin.class_coins_by_month:
                if coin_by_month.type == False:
                    overhead += coin_by_month.coins
            rest_coin = 0
            rest_coin = coins - overhead
            ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).update({
                "coins": coins,
                "given_coins": overhead,
                "rest_coins": rest_coin
            })
            db.session.commit()
            update_overall_coins()
    else:
        add_coin_by_month = ClassCoinsByMonth(class_coins_id=filtered_coin.id, coins=info["count"], type=False,
                                              day_id=filtered_day.id, reason=info["reason"])
        db.session.add(add_coin_by_month)
        db.session.commit()
        coins = 0
        fl_coin = ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).first()
        for coins_by_month in fl_coin.class_coins_by_month:
            if coins_by_month.type == True:
                coins += coins_by_month.coins
        for coin_by_month in filtered_coin.class_coins_by_month:
            if coin_by_month.type == False:
                overhead += coin_by_month.coins
        rest_coin = 0
        rest_coin = coins - overhead
        ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).update({
            "coins": coins,
            "given_coins": overhead,
            "rest_coins": rest_coin
        })
        db.session.commit()
        update_overall_coins()
    return jsonify()


@app.route('/change_coins_in_classes', methods=["POST", "GET"])
def change_coins_in_classes():
    user = current_user()
    info = request.get_json()['info']
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    filtered_year = Years.query.filter(Years.year == int(year)).first()
    filtered_month = Month.query.filter(Month.month_number == int(month), Month.years_id == filtered_year.id).first()
    filtered_day = Day.query.filter(Day.day_number == int(day), Day.month_id == filtered_month.id,
                                    Day.year_id == filtered_year.id).first()
    filtered_coin = ClassCoins.query.filter(ClassCoins.class_id == info["class_id"],
                                            ClassCoins.year_id == filtered_year.id,
                                            ClassCoins.month_id == filtered_month.id).first()
    overhead = 0

    if info["status"] == "plus":
        if not filtered_coin:
            add_coin = ClassCoins(class_id=info["class_id"], year_id=filtered_year.id, month_id=filtered_month.id,
                                  coins=0,
                                  given_coins=0, rest_coins=info["coins"])
            db.session.add(add_coin)
            db.session.commit()
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=add_coin.id, coins=info["coins"], type=True,
                                                  day_id=filtered_day.id, reason=info["reason"], user_id=user.id)
            db.session.add(add_coin_by_month)
            db.session.commit()
            fl_coin = ClassCoins.query.filter(ClassCoins.id == add_coin.id).first()
            coins = 0
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins

            ClassCoins.query.filter(ClassCoins.id == add_coin.id).update({
                "coins": coins
            })
            db.session.commit()
            update_overall_coins()
        else:
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=filtered_coin.id, coins=info["coins"], type=True,
                                                  day_id=filtered_day.id, reason=info["reason"], user_id=user.id)
            db.session.add(add_coin_by_month)
            db.session.commit()
            fl_coin = ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).first()
            coins = 0
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins
            for coin_by_month in filtered_coin.class_coins_by_month:
                if coin_by_month.type == False:
                    overhead += coin_by_month.coins
            rest_coin = 0
            rest_coin = coins - overhead
            ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).update({
                "coins": coins,
                "given_coins": overhead,
                "rest_coins": rest_coin
            })
            db.session.commit()
            update_overall_coins()
    else:
        if filtered_coin:
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=filtered_coin.id, coins=info["coins"], type=False,
                                                  day_id=filtered_day.id, reason=info["reason"], user_id=user.id)
            db.session.add(add_coin_by_month)
            db.session.commit()
            coins = 0
            fl_coin = ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).first()
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins
            for coin_by_month in filtered_coin.class_coins_by_month:
                if coin_by_month.type == False:
                    overhead += coin_by_month.coins
            rest_coin = 0
            rest_coin = coins - overhead
            ClassCoins.query.filter(ClassCoins.id == filtered_coin.id).update({
                "coins": coins,
                "given_coins": overhead,
                "rest_coins": rest_coin
            })
            db.session.commit()
            update_overall_coins()
        else:
            month2 = month - 1
            filtered_month2 = Month.query.filter(Month.month_number == int(month2), Month.years_id == filtered_year.id).first()
            filtered_coin2 = ClassCoins.query.filter(ClassCoins.class_id == info["class_id"],
                                                    ClassCoins.year_id == filtered_year.id,
                                                    ClassCoins.month_id == filtered_month2.id).first()
            add_coin_by_month = ClassCoinsByMonth(class_coins_id=filtered_coin2.id, coins=info["coins"], type=False,
                                                  day_id=filtered_day.id, reason=info["reason"], user_id=user.id)
            db.session.add(add_coin_by_month)
            db.session.commit()
            coins = 0
            fl_coin = ClassCoins.query.filter(ClassCoins.id == filtered_coin2.id).first()
            for coins_by_month in fl_coin.class_coins_by_month:
                if coins_by_month.type == True:
                    coins += coins_by_month.coins
            for coin_by_month in filtered_coin2.class_coins_by_month:
                if coin_by_month.type == False:
                    overhead += coin_by_month.coins
            rest_coin = 0
            rest_coin = coins - overhead
            ClassCoins.query.filter(ClassCoins.id == filtered_coin2.id).update({
                "coins": coins,
                "given_coins": overhead,
                "rest_coins": rest_coin
            })
            db.session.commit()
            update_overall_coins()
    return jsonify({})


def update_overall_coins():
    classes = Class.query.all()
    overall = 0
    for classs in classes:
        if classs.class_coins:
            for coins in classs.class_coins:
                overall += coins.rest_coins
            Class.query.filter(Class.id == classs.id).update({
                'overall_coins': overall
            })
            db.session.commit()
            overall = 0
        else:
            Class.query.filter(Class.id == classs.id).update({
                'overall_coins': 0
            })
            db.session.commit()
