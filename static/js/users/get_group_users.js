var options = {
    valueNames: ['user_id', 'username', 'gender', 'created', 'age', 'city', 'bio', 'active', 'group'],
    page: 12,
    pagination: true
};

const get_users = async (callback) => {
    let values = await fetch("/groups/{{group_data}}").
        then(data => { return data.json() })
    console.log(values.response)
    let userList = new List('users', options, values.response);
}

get_users()

