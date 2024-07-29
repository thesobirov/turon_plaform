from backend.models.basic_model import *
from app import *
from backend.models.settings import *
from backend.basics.settings import *


@app.route(f'{api}/info_exercise', methods=['POST', 'GET'])
def info_exercise():
    if request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        selected_level = get_json['selectedLevel']
        selected_subject = get_json['selectedSubject']
        name = get_json['title']
        exercise_type = get_json['typeEx']
        components = get_json['components']
        get_exercise_type = ExerciseTypes.query.filter(ExerciseTypes.id == exercise_type).first()
        get_level = SubjectLevel.query.filter(SubjectLevel.id == selected_level).first()
        get_subject = Subject.query.filter(Subject.id == selected_subject).first()
        add_exercise = Exercise(name=name, level_id=get_level.id,
                                type_id=get_exercise_type.id,
                                subject_id=get_subject.id)
        add_exercise.add_commit()

        for component in components:
            type_component = component['type']
            text = ''
            if 'text' in component:
                text = component['text']
            get_component = Component.query.filter(Component.name == type_component).first()
            if not get_component:
                get_component = Component(name=type_component)
                get_component.add_commit()
            audio_url = ''
            if type_component == "audio":
                audio = request.files.get(f'component-{component["index"]}-audio')
                audio_url = save_img(audio, app, type_file="audio")

            word_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if word_img:
                get_img = add_file(word_img, app, Images)
            inner_type = ''
            if 'innerType' in component:
                inner_type = component['innerType']
            clone = ''
            if 'clone' in component:
                clone = component['clone']
            add_exe = ExerciseBlock(desc=text, exercise_id=add_exercise.id, component_id=get_component.id,
                                    clone=clone, img_id=get_img, audio_url=audio_url,
                                    inner_type=inner_type)
            add_exe.add_commit()
            if 'words' in component:
                words = component['words']
                for word in words:
                    if 'active' in word:
                        get_img = None
                        type_img = ''
                        word_img = request.files.get(f'component-{component["index"]}-words-index-{word["id"]}')
                        if word_img:
                            get_img = add_file(word_img, app, Images)
                            block_img = ExerciseBlockImages(img_id=get_img, block_id=add_exe.id, order=word['id'],
                                                            type_image="word")
                            block_img.add_commit()
                        else:
                            answer_exercise = ExerciseAnswers(exercise_id=add_exercise.id, subject_id=get_subject.id,
                                                              level_id=get_level.id, desc=word['word'], img_id=get_img,
                                                              type_id=get_exercise_type.id, order=word['id'],
                                                              block_id=add_exe.id,
                                                              status=word['active'], type_img=type_img)
                            answer_exercise.add_commit()
            if 'variants' in component:
                type_img = ''
                if component['variants']['type'] == "select":
                    for option in component['variants']['options']:
                        if option['innerType'] == "text":
                            get_img = None
                            type_img = ''
                        else:
                            word_img = request.files.get(
                                f'component-{component["index"]}-variants-index-{option["index"]}')
                            get_img = add_file(word_img, app, Images)
                            type_img = 'variant_img'
                        answer_exercise = ExerciseAnswers(exercise_id=add_exercise.id, subject_id=get_subject.id,
                                                          level_id=get_level.id, desc=option['text'],
                                                          img_id=get_img, status=option['isTrue'],
                                                          type_id=get_exercise_type.id, order=option['index'],
                                                          type_img=type_img, block_id=add_exe.id)

                        answer_exercise.add_commit()
                else:
                    answer_exercise = ExerciseAnswers(exercise_id=add_exercise.id, subject_id=get_subject.id,
                                                      level_id=get_level.id, desc=component['variants']['answer'],
                                                      type_img=type_img,
                                                      type_id=get_exercise_type.id, status=True, block_id=add_exe.id)

                    answer_exercise.add_commit()
        return create_msg(name, True)
    exercises = Exercise.query.order_by(Exercise.id).all()

    return jsonify({
        "data": iterate_models(exercises, entire=True)
    })


@app.route(f'{api}/exercise_profile/<int:exercise_id>', methods=['POST', 'GET', 'DELETE'])
def exercise_profile(exercise_id):
    if request.method == "GET":
        exercise = Exercise.query.filter(Exercise.id == exercise_id).first()

        return jsonify({
            "data": exercise.convert_json(entire=True)
        })
    elif request.method == "DELETE":
        exercise = Exercise.query.filter(Exercise.id == exercise_id).first()
        name = exercise.name
        blocks = ExerciseBlock.query.filter(ExerciseBlock.exercise_id == exercise_id).all()
        for block in blocks:
            block_img = ExerciseBlockImages.query.filter(ExerciseBlockImages.block_id == block.id).all()
            for img in block_img:
                check_img_remove(img.img_id, Images)
                img.delete_commit()
        exercise_answers = ExerciseAnswers.query.filter(ExerciseAnswers.exercise_id == exercise_id).all()
        donelessons = StudentExercise.query.filter(StudentExercise.exercise_id == exercise_id).all()

        try:
            delete_list_models(blocks, Images)
            delete_list_models(exercise_answers, Images)
            delete_list_models(donelessons, Images)
            exercise.delete_commit()
            return del_msg(item=name, status=True)
        except:
            return del_msg(item=name, status=False)
    elif request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        selected_level = get_json['selectedLevel']
        selected_subject = get_json['selectedSubject']
        name = get_json['title']
        exercise_type = get_json['typeEx']
        components = get_json['components']
        get_exercise_type = ExerciseTypes.query.filter(ExerciseTypes.id == exercise_type).first()
        get_level = SubjectLevel.query.filter(SubjectLevel.id == selected_level).first()
        get_subject = Subject.query.filter(Subject.id == selected_subject).first()
        Exercise.query.filter(Exercise.id == exercise_id).update({
            "subject_id": get_subject.id,
            "type_id": get_exercise_type.id,
            "level_id": get_level.id,
            "name": name
        })
        db.session.commit()
        exercise = Exercise.query.filter(Exercise.id == exercise_id).first()
        for component in components:
            type_component = component['type']
            get_component = Component.query.filter(Component.name == type_component).first()
            if not get_component:
                get_component = Component(name=type_component)
                get_component.add_commit()
            text = ''
            if 'text' in component:
                text = component['text']
            audio_url = ''
            if type_component == "audio":
                audio = request.files.get(f'component-{component["index"]}-audio')
                if audio:
                    audio_url = save_img(audio, app, type_file="audio")

            word_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if word_img:
                get_img = add_file(word_img, app, Images)
            inner_type = ''
            if 'innerType' in component:
                inner_type = component['innerType']
            if 'block_id' not in component:

                block = ExerciseBlock(desc=text, exercise_id=exercise.id, component_id=get_component.id,
                                      clone=component, img_id=get_img, audio_url=audio_url,
                                      inner_type=inner_type)
                block.add_commit()
            else:
                block = ExerciseBlock.query.filter(ExerciseBlock.id == component['block_id']).first()
                if not audio_url:
                    audio_url = block.audio_url
                else:
                    if block.audio_url:
                        check_audio_remove(block.id, ExerciseBlock)
                if not get_img:
                    get_img = block.img_id
                else:
                    if block.img_id:
                        check_img_remove(block.img_id, Images)
                block.desc = text
                block.audio_url = audio_url
                block.img_id = get_img
                block.component_id = get_component.id
                block.inner_type = component['innerType']
                block.clone = component['clone']
                db.session.commit()

            if 'block_id' not in component:
                if 'words' in component:
                    words = component['words']

                    for word in words:

                        if 'active' in word and word['active'] == True:
                            get_img = None
                            type_img = ''
                            # if component['type'] == "question" and component['innerType'] == ""
                            word_img = request.files.get(f'component-{component["index"]}-words-index-{word["id"]}')
                            if word_img:
                                get_img = add_file(word_img, app, Images)
                                block_img = ExerciseBlockImages(img_id=get_img, block_id=block.id, order=word['id'],
                                                                type_image="word")
                                block_img.add_commit()
                            else:

                                answer_exercise = ExerciseAnswers(exercise_id=exercise.id, subject_id=get_subject.id,
                                                                  level_id=get_level.id, desc=word['word'],
                                                                  img_id=get_img,
                                                                  type_id=get_exercise_type.id, order=word['id'],
                                                                  block_id=block.id,
                                                                  status=word['active'], type_img=type_img)
                                answer_exercise.add_commit()
                if 'variants' in component:

                    if component['variants']['type'] == "select":
                        for option in component['variants']['options']:
                            if option['innerType'] == "text":
                                get_img = None
                                type_img = ''
                            else:
                                word_img = request.files.get(
                                    f'component-{component["index"]}-variants-index-{option["index"]}')
                                if word_img:
                                    print('variants_img')
                                    get_img = add_file(word_img, app, Images)
                                type_img = 'variant_img'
                            answer_exercise = ExerciseAnswers(exercise_id=exercise.id, subject_id=get_subject.id,
                                                              level_id=get_level.id, desc=option['text'],
                                                              img_id=get_img, status=option['isTrue'],
                                                              type_id=get_exercise_type.id, order=option['index'],
                                                              type_img=type_img, block_id=block.id)

                            answer_exercise.add_commit()
                    else:
                        type_img = ''
                        answer_exercise = ExerciseAnswers(exercise_id=exercise.id, subject_id=get_subject.id,
                                                          level_id=get_level.id, desc=component['variants']['answer'],
                                                          type_img=type_img, order=0,
                                                          type_id=get_exercise_type.id, status=True, block_id=block.id)

                        answer_exercise.add_commit()
            else:
                if 'words' in component:
                    for word in component['words']:

                        if 'active' in word and word['active'] == True:
                            exercise_answer = ExerciseAnswers.query.filter(
                                ExerciseAnswers.block_id == component['block_id'],
                                ExerciseAnswers.order == word['id']).first()

                            word_img = request.files.get(f'component-{component["index"]}-words-index-{word["id"]}')
                            block_img = ExerciseBlockImages.query.filter(
                                ExerciseBlockImages.block_id == block.id).first()
                            if word_img:
                                get_img = add_file(word_img, app, Images)
                                type_img = "question_img"
                                print('question_img')
                            else:
                                type_img = "question_img"
                                if block_img:
                                    type_img = block_img.type_image
                                    get_img = block_img.img_id
                                print('not question_img')
                            if block_img:
                                block_img.img_id = get_img
                                block_img.type_image = type_img
                            if exercise_answer:
                                exercise_answer.desc = word['word']
                                exercise_answer.status = word['active']
                                exercise_answer.subject_id = get_subject.id
                                exercise_answer.order = word['id']
                                exercise_answer.block_id = block.id
                                exercise_answer.type_id = get_exercise_type.id
                                exercise_answer.level_id = get_level.id
                                exercise_answer.exercise_id = exercise.id
                            db.session.commit()
                if 'variants' in component:

                    if component['variants']['type'] == "select":
                        for option in component['variants']['options']:
                            exercise_answer = ExerciseAnswers.query.filter(
                                ExerciseAnswers.block_id == component['block_id'],
                                ExerciseAnswers.order == option['index']).first()
                            if option['innerType'] == "text":
                                get_img = None
                                type_img = ''
                            else:
                                word_img = request.files.get(
                                    f'component-{component["index"]}-variants-index-{option["index"]}')
                                if word_img:
                                    print('variants_img')
                                    get_img = add_file(word_img, app, Images)
                                else:
                                    get_img = exercise_answer.img_id
                                type_img = 'variant_img'
                            exercise_answer.img_id = get_img
                            exercise_answer.type_img = type_img
                            exercise_answer.subject_id = get_subject.id
                            exercise_answer.order = option['index']
                            exercise_answer.block_id = block.id
                            exercise_answer.type_id = get_exercise_type.id
                            exercise_answer.level_id = get_level.id
                            exercise_answer.exercise_id = exercise.id
                            exercise_answer.desc = option['text']
                            exercise_answer.status = option['isTrue']
                            db.session.commit()
                # else:
                #     exercise_answer = ExerciseAnswers.query.filter(
                #         ExerciseAnswers.block_id == component['block_id'],
                #         ExerciseAnswers.order == 0).first()
                #     type_img = ''
                #
                #     exercise_answer.type_img = type_img
                #     exercise_answer.subject_id = get_subject.id
                #     exercise_answer.block_id = block.id
                #     exercise_answer.type_id = get_exercise_type.id
                #     exercise_answer.level_id = get_level.id
                #     exercise_answer.exercise_id = exercise.id
                #     exercise_answer.desc = component['variants']['answer']
                #     exercise_answer.status = True
                #     db.session.commit()
        return edit_msg(exercise.name, status=True, data=exercise.convert_json(entire=True))


@app.route(f'{api}/delete_block/<int:block_id>', methods=['DELETE'])
def delete_block(block_id):
    block = ExerciseBlock.query.filter(ExerciseBlock.id == block_id).first()
    exercise_answers = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == block_id).all()
    delete_list_models(exercise_answers, Images)
    if block.img_id:
        check_img_remove(block.img_id, Images)
    block_img = ExerciseBlockImages.query.filter(ExerciseBlockImages.block_id == block_id).all()
    for img in block_img:
        check_img_remove(img.img_id, Images)
        img.delete_commit()
    block.delete_commit()

    return del_msg(item="block", status=True)
