var options = {
    valueNames: ['groupkey'],
    page: 10,
    pagination: true
};

const list_groups = async (callback) => {
    let values = await fetch("/get_groups").
        then(data => { return data.json() })
    console.log(values.response)
    let groupList = new List('groups', options, values.response);
}

list_groups()

const create_group = async (callback) => {

    var user_id = document.getElementById("user_id").value;
    var new_group = document.getElementById("new_group").value;


    data = {
        "user_id": parseInt(user_id),
        "new_group": new_group
    }

    console.log(data.username)


    let response = await fetch("/add_group", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    }).then(response => { return response.json() })

    document.getElementById("json").textContent = JSON.stringify(response, undefined, 2)
    return false
}