// fetch('/gallery_edit', {
//     method: "POST", body: JSON.stringify({
//         "edit": firstGalleryList,
//     }), headers: {
//         'Content-type': 'application/json'
//     },
// })
let input = document.querySelector(".img");

function addClass(boxes) {
    boxes[0].classList.add("w2")
    boxes[4].classList.add("h2")
    boxes[5].classList.add("w2")
}

function updateGallery(response) {
    let big = document.querySelector('.big');
    big.innerHTML = ''
    console.log(response['gallery_list'])
    for (let img of response['gallery_list']) {
        big.innerHTML += `<div class="big_box" data-id="${img['id']}">
                    <img class="big_img" src="${img['img_url']}" alt="">
                </div>`
    }
    let boxes = document.querySelectorAll(".big_box");

    boxes.forEach(item => {
        item.addEventListener("click", async () => {


            input.click()
            input.setAttribute("data-id", item.dataset.id)
        })
    })
    console.log(boxes)
    addClass(boxes)
}

fetch('/get_gallery', {
    method: "GET",
})
    .then(function (response) {
        return response.json()
    })
    .then(function (response) {
        updateGallery(response)
    })

input.addEventListener("change", () => {
    console.log(input.dataset.id)
    const data = new FormData()

    data.append("file", input.files[0])
    console.log(input.files[0])
    fetch('/gallery_edit/' + input.dataset.id, {
        method: "POST", body: data
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (response) {
            updateGallery(response)
        })

})


