var options = {
    valueNames: ['user_id', 'username', 'gender', 'created', 'age', 'city', 'bio', 'active', 'group'],
    page: 12,
    pagination: true
};

const get_users = async (callback) => {
    let values = await fetch("/get_users").
        then(data => { return data.json() })
    console.log(values.response)
    let userList = new List('users', options, values.response);
}

get_users()

const add_user = async (callback) => {

    var userid = document.getElementById("userid").value;
    var username = document.getElementById("username").value;
    var gender = document.getElementById("gender").value;
    var age = document.getElementById("age").value;
    var city = document.getElementById("city").value;
    var bio = document.getElementById("bio").value;
    var active = document.getElementById("active").value;

    data = {
        "userid": userid,
        "username": username,
        "gender": gender,
        "age": age,
        "city": city,
        "bio": bio,
        "active": active
    }

    console.log(data.username)


    let response = await fetch("/add_user", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    }).then(response => { return response.json() })

    document.getElementById("json").textContent = JSON.stringify(response, undefined, 2)
    return false
}
