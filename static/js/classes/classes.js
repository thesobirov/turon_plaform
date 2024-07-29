let create = document.querySelector('.create'), x = document.querySelector('.x'),
    filter_btn = document.querySelector('.filter_btn'), double = document.querySelector('.double'),
    filter = document.querySelector('.filter'),
    add = document.querySelector('.add'),
    next = document.querySelector('.next'),
    filter_form = document.querySelector('.form_filter'),
    class_number = document.querySelector('.class_number'),
    select = document.querySelector('.select'),
    number = document.querySelector('.class_number'),
    tbody = document.querySelector('.tbody'),
    color = document.querySelector('.color'),
    coins = document.querySelectorAll('.coins'),
    coinsCount = document.querySelector('.coinsCount'),
    reason = document.querySelector('.reason'),
    addCoinModal = document.querySelector('.addCoin'),
    sendButton = document.querySelector('.addCoin_form_container button'),
    class_id,
    status,
    language_type = document.querySelector('.language_type');


coins.forEach((item, index) => {
    item.addEventListener("click", () => {
        addCoinModal.classList.add("activeModal")
        class_id = item.dataset.id
        status = item.dataset.status

    })
})
addCoinModal.addEventListener("click", (e) => {
    if (e.target === addCoinModal) {
        addCoinModal.classList.remove("activeModal")
    }
})
sendButton.addEventListener("click", () => {
    addCoinModal.classList.remove("activeModal")
    let info = {
        class_id,
        status,
        reason: reason.value,
        coins: coinsCount.value
    }
    reason.value = ""
    coinsCount.value = ""
    console.log(info)
    fetch('/change_coins_in_classes', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
})

filter_btn.addEventListener('click', () => {


    if (double.style.display === "none") {
        double.style.display = "flex"
        filter.classList.remove('active_filter')
    } else {
        double.style.display = "none"
        filter.classList.add('active_filter')
    }

})


filter_form.addEventListener('click', () => {
    const info = {
        class_number: number.value,
        color: color.value,
        language_type: language_type.value
    }
    fetch('/filter_classes', {
        method: "POST", body: JSON.stringify({
            "info": info
        }), headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resp => {

            tbody.innerHTML = ''
            for (const info of resp ['filter_classes']) {
                if (info.color === "green") {
                    tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/class_profile/${info.id}">
                             <div style="background-color: green; width: 5rem; height: 5rem; border-radius: 50%"></div></a></td>
                            <td>${info.name}</td>
                            <td>${info.teacher}</td>
                            <td>${info.student_number}</td>
                            <td>${info.class_number}</td>
                            <td>${info.color}</td>
                            <td>${info.language}</td>
                        </tr>`
                } else {
                    tbody.innerHTML += `<tr>
                            <td></td>
                            <td><a href="/class_profile/${info.id}">
                             <div style="background-color: blue; width: 5rem; height: 5rem; border-radius: 50%"></div></a></td>
                            <td>${info.name}</td>
                            <td>${info.teacher}</td>
                            <td>${info.student_number}</td>
                            <td>${info.class_number}</td>
                            <td>${info.color}</td>
                        </tr>`
                }

            }
        })
})