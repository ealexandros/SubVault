const getLogFile = async () => {
    const logs = await eel.get_visited_datetimes()();
    const table = document.getElementById('vault_table_body');
    console.log(logs);

    table.innerHTML = '';
    if(logs.lenght == 0) {
        table.innerHTML = `<tr>
                            <td class="w-1/2 pb-3 pt-3 font-bold">-</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">-</td>
                            <td class="w-1/4 pb-3 pt-3 text-center">-</td>
                            </tr>`
        return;
    }

    index = 1;
    logs.forEach(log => {
        table.innerHTML += `<tr style="border-bottom: 3px solid red;">
                            <td class="w-1/2 pb-3 pt-3 text-white text-opacity-90">Number <span class="font-bold">${index++}</span></td>
                            <td class="w-1/4 pb-3 pt-3 text-white text-opacity-90 text-center">${log[0]}</td>
                            <td class="w-1/4 pb-3 pt-3 text-white text-opacity-90 text-center">${log[1]}</td>
                        </tr>`
    });
}