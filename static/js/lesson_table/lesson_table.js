let select = document.querySelector('.select'),
    wednesday = document.querySelector('.wednesday'),
    monday = document.querySelector('.monday'),
    friday = document.querySelector('.friday'),
    thursday = document.querySelector('.thursday'),
    tuesday = document.querySelector('.tuesday'),
    main = document.querySelector('.main'),
    main_table = document.querySelectorAll('.main_table');


function start() {
    console.log(main_table)
    main_table[0].classList.add("active_table")
}

start()

function remove() {
    main_table.forEach(item => {
        item.classList.remove("active_table")
    })
}

select.addEventListener("change", () => {
    fetch(`/get_lesson_table/${select.value}`, {
        method: "GET",
        headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {
            console.log(resp)
            const main_table = document.createElement("div")
            main_table.classList.add("main_table")
            const table = document.createElement("table")
            const thead = document.createElement("thead")
            const daysTr = document.createElement("tr")
            const daysTitle = document.createElement("th")
            daysTitle.innerText = 'Xonalar nomi'
            daysTr.append(daysTitle)
            console.log(resp['lesson_list'])
            for (let t = 0; t < resp['lesson_list']['rooms'][0]['lessons'].length; t++) {
                const day = document.createElement("th")
                day.innerText = `${resp['lesson_list']['rooms'][0]['lessons'][t]['lesson_time']['start']} : ${resp['lesson_list']['rooms'][0]['lessons'][t]['lesson_time']['end']}`
                daysTr.append(day)
            }
            thead.append(daysTr)
            table.append(thead)
            const tbody = document.createElement("tbody")
            for (let l = 0; l < resp['lesson_list']['rooms'].length; l++) {
                const lessonsTr = document.createElement("tr")
                const lessonsClass = document.createElement("td")
                lessonsClass.innerText = resp['lesson_list']['rooms'][l]['class_info']
                lessonsTr.append(lessonsClass)
                for (let i = 0; i < resp['lesson_list']['rooms'][l]['lessons'].length; i++) {
                    if (resp['lesson_list']['rooms'][l]['lessons'][i]['flow'] && resp['lesson_list']['rooms'][l]['lessons'][i]['flow'] !== null) {
                        const lessonsItem = document.createElement("td")
                        lessonsItem.classList.add('flow_td')
                        console.log("true")
                        if (resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']) {
                            console.log(resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']['name'])
                            const flow_p = document.createElement("p")
                            flow_p.classList.add('flow_p')
                            flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']['name']} ${resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']['surname']}`
                            lessonsItem.append(flow_p)
                        }
                        if (resp['lesson_list']['rooms'][l]['lessons'][i]['subject']) {
                            const flow_p = document.createElement("p")
                            flow_p.classList.add('flow_p')
                            flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['subject']['name']}`
                            lessonsItem.append(flow_p)
                        }
                        if (resp['lesson_list']['rooms'][l]['lessons'][i]['flow']) {
                            const flow_p = document.createElement("p")
                            flow_p.classList.add('flow_p')
                            flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['flow']['name']}`
                            lessonsItem.append(flow_p)
                        }
                        if (resp['lesson_list']['rooms'][l]['lessons'][i]['room']) {
                            const flow_p = document.createElement("p")
                            flow_p.classList.add('flow_p')
                            flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['room']['name']}`
                            lessonsItem.append(flow_p)
                        }
                        lessonsTr.append(lessonsItem)
                    } else {
                        if (resp['lesson_list']['rooms'][l]['lessons'][i]['flow'] === null) {
                            const lessonsItem = document.createElement("td")
                            lessonsItem.classList.add('simple_td')
                            if (resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']) {
                                const flow_p = document.createElement("p")
                                flow_p.classList.add('simple_p')
                                flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']['name']} ${resp['lesson_list']['rooms'][l]['lessons'][i]['teacher']['surname']}`
                                lessonsItem.append(flow_p)
                            }
                            if (resp['lesson_list']['rooms'][l]['lessons'][i]['subject']) {
                                const flow_p = document.createElement("p")
                                flow_p.classList.add('simple_p')
                                flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['subject']['name']}`
                                lessonsItem.append(flow_p)
                            }
                            if (resp['lesson_list']['rooms'][l]['lessons'][i]['room']) {
                                const flow_p = document.createElement("p")
                                flow_p.classList.add('simple_p')
                                flow_p.innerText = `${resp['lesson_list']['rooms'][l]['lessons'][i]['room']['name']}`
                                lessonsItem.append(flow_p)
                            }
                            lessonsTr.append(lessonsItem)
                        } else {
                            const lessonsItem = document.createElement("td")
                            lessonsTr.append(lessonsItem)
                        }
                    }

                    tbody.append(lessonsTr)
                }
            }
            table.append(tbody)
            main_table.append(table)
            console.log(main)
            let main_tables = document.querySelectorAll('.main .main_table')
            main_tables.forEach(item => {
                item.remove()
            })
            main.append(main_table)

        })
})




