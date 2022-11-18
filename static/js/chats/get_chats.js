var options = {
    valueNames: ['chat'],
    page: 10,
    pagination: true
};

const list_chats = async (callback) => {
    let values = await fetch("/get_chats").
        then(data => { return data.json() })
    console.log(values.response)
    let chatList = new List('chats', options, values.response);
}

list_chats()

const create_group = async (callback) => {

    var group = document.getElementById("group").value;
    var new_chat = document.getElementById("new_chat").value;


    data = {
        "group": group,
        "new_chat": new_chat
    }

    console.log(data.username)


    let response = await fetch("/add_chat", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    }).then(response => { return response.json() })

    document.getElementById("json").textContent = JSON.stringify(response, undefined, 2)
    return false
}