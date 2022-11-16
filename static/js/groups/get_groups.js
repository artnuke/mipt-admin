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